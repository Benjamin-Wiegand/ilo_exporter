from prometheus_client import start_http_server, Counter
from prometheus_client.core import REGISTRY, GaugeMetricFamily
from prometheus_client.registry import Collector

from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi import CommunityData, UdpTransportTarget, ContextData

from snmp import SnmpConfiguration, snmp_get
import scrape

from snmp_groups import BulkValues, BulkDummyValue
from targets.temp import *
from targets.fan import *
from targets.cpu import *
from targets.drive import *
from targets.memory import *
from targets.power import *

import argparse

NAMESPACE = 'ilo'

arg_parser = argparse.ArgumentParser(
    'ilo_exporter',
    description='A fast(er) prometheus exporter for applicable HP servers using SNMP via the ILO controller.',
)

arg_parser.add_argument('-i', '--ilo-address', help='ILO IP address to scan.', required=True)
arg_parser.add_argument('-a', '--server-address', default='0.0.0.0', help='Address to bind for hosting the metrics endpoint.')
arg_parser.add_argument('-p', '--server-port', default=6969, help='Port to bind for the metrics endpoint.')
arg_parser.add_argument('-c', '--snmp-community', default='public', help='SNMP community to read.')
arg_parser.add_argument('--snmp-port', default=161, help='SNMP port to use.')
arg_parser.add_argument('-o', '--scan-once', action='store_true', help='Only scan for SNMP variables on init, instead of on each collection (except hard drives, see --scan-drives-once). This is a small optimizaion that can be used if your sever configuration never changes.')
arg_parser.add_argument('--scan-drives-once', action='store_true', help='When combined with --scan-once, this also prevents hard drives from being rescanned on collection. This is not recommeded.')
arg_parser.add_argument('-v', '--verbose', action='store_true', help='Increases verbosity.')
arg_parser.add_argument('-q', '--quiet', action='store_true', help='Tells the exporter to stfu under normal operation unless there is an error/warning.')

args = arg_parser.parse_args()
if args.quiet and args.verbose:
    print('stop it. (--quiet and --verbose do not mix)')
    exit(1)

SCAN_FAIL_COUNTER = Counter('scrape_failures', 'Number of times scraping the iLO for SNMP variables has failed.', namespace=NAMESPACE, subsystem='exporter')


def noisy(*a, **kwa):
    if not args.quiet:
        print(*a, **kwa)


def verbose(*a, **kwa):
    if args.verbose:
        print(*a, **kwa)


class BulkCollector(Collector):
    def __init__(self, snmp_config: SnmpConfiguration, index_oid_template: str, target_name: str, scan_on_collect: bool, *metrics_groups: tuple[str, BulkValues, list[BulkEnums]], scan_method: any = scrape.detect_things):
        self._snmp_config = snmp_config
        self._metrics_groups = metrics_groups
        self._target_name = target_name
        self._name_template = '%s_%s_' % (NAMESPACE, target_name) + '%s'
        self._ids = []
        self._index_oid_template = index_oid_template
        self._scan_on_collect = scan_on_collect
        self._scan_method = scan_method

        if not scan_on_collect:
            self.scan()

    def scan(self):
        verbose('scanning target', self._target_name)
        self._ids = self._scan_method(self._snmp_config, self._index_oid_template)
        noisy('found', len(self._ids), 'items for target', self._target_name)

    def collect(self):
        cache = {}

        try:
            if self._scan_on_collect:
                self.scan()

            for documentation, bulk_values, bulk_labels in self._metrics_groups:
                metric_name = self._name_template % bulk_values.name
                verbose('collecting', metric_name)

                label_names = ['id']
                label_maps = []

                for label in bulk_labels:
                    # the labels are cached since they may be reused
                    if label.name not in cache:
                        cache[label.name] = label.get_values(self._snmp_config, self._ids)
                    label_names.append(label.name)
                    label_maps.append(cache[label.name])

                metric = GaugeMetricFamily(
                    metric_name,
                    documentation,
                    labels=label_names
                )

                # values are not reused
                value_map = bulk_values.get_values(self._snmp_config, self._ids)

                # do some fuckery (bad design, I know.)
                for i in self._ids:
                    labels = [str(i)]  # id is first
                    for label_map in label_maps:
                        label_value = label_map[i]
                        labels.append(str(label_value))

                    value = value_map[i]
                    metric.add_metric(labels, value)

                yield metric

        except Exception as e:
            print('Failed to scan SNMP, aborting collection')
            SCAN_FAIL_COUNTER.inc()
            raise e


class PowerCollector(Collector):
    def collect(self) -> float:
        verbose('collecting ilo_server_power_draw')
        try:
            reading = snmp_get(config, POWER_METER_READING)
            support = snmp_get(config, POWER_METER_SUPPORT)
            status = snmp_get(config, POWER_METER_STATUS)

            if not isinstance(reading, int):
                print('expected power meter reading to be an int, got', type(reading))
                print('value in question:', reading)
                reading = -1
            if not isinstance(support, int):
                print('expected power meter support to be an int, got', type(support))
                print('value in question:', support)
                support = 1
            if not isinstance(status, int):
                print('expected power meter status to be an int, got', type(status))
                print('value in question:', status)
                status = 1

            if support not in POWER_METER_SUPPORT_MAP:
                print('ILO returned a value outside of the expected range for POWER_METER_SUPPORT:', support)
                support_s = 'unknown'
            else:
                support_s = POWER_METER_SUPPORT_MAP[support]
            if status not in POWER_METER_STATUS_MAP:
                print('ILO returned a value outside of the expected range for POWER_METER_STATUS:', status)
                status_s = 'unknown'
            else:
                status_s = POWER_METER_STATUS_MAP[status]

            metric = GaugeMetricFamily('ilo_server_power_draw', 'Power draw of the server in watts', labels=['support', 'status'])
            metric.add_metric([support_s, status_s], reading)
            yield metric
        except Exception as e:
            print('Failed to scan SNMP, aborting collection')
            SCAN_FAIL_COUNTER.inc()
            raise e


if __name__ == '__main__':

    config = SnmpConfiguration(
        SnmpEngine(),
        CommunityData(args.snmp_community),
        UdpTransportTarget((args.ilo_address, args.snmp_port)),
        ContextData(),
    )

    REGISTRY.register(PowerCollector())

    no_value = BulkDummyValue('info')

    REGISTRY.register(BulkCollector(
        config,
        TEMP_INDEX,
        'temperature',
        not args.scan_once,
        ('Information temperature sensors', no_value, [TEMP_SENSOR_LOCALE, TEMP_CONDITION, TEMP_THRESHOLD_TYPE]),
        ('Temperatures readings of each temperature sensor in celsius', TEMP_CELSIUS, []),
        ('Temperature thresholds for each temperature sensor in celsius', TEMP_THRESHOLD, []),
    ))

    REGISTRY.register(BulkCollector(
        config,
        FAN_INDEX,
        'fan',
        not args.scan_once,
        ('Information about system fans', no_value, [FAN_LOCALE, FAN_CONDITION, FAN_SPEED, FAN_PRESENT, FAN_PRESENCE_TEST]),
    ))

    REGISTRY.register(BulkCollector(
        config,
        CPU_INDEX,
        'cpu',
        not args.scan_once,
        ('Information about CPUs', no_value, [CPU_NAME, CPU_STATUS, CPU_POWER_STATUS]),
        ('Speed of CPUs in megahertz', CPU_SPEED, []),
        ('CPU step', CPU_STEP, []),     # revision?
        ('Number of enabled cores', CORES_ENABLED, []),
        ('Number of available threads', THREADS_AVAILABLE, []),
    ))

    # logical drives are for v2 if it ever exists (I don't use logical drives, sorry)

    REGISTRY.register(BulkCollector(
        config,
        DRIVE_INDEX,
        'drive',
        not args.scan_drives_once,
        ('Information about installed drives', no_value, [DRIVE_PORT, DRIVE_BOX, DRIVE_BAY, DRIVE_VENDOR, DRIVE_SERIAL, DRIVE_FIRMWARE, DRIVE_LINK_RATE, DRIVE_SUPPORTS_PREDICTIVE_FAILURE_MONITORING, DRIVE_SMART_STATUS, DRIVE_MEDIA_TYPE, DRIVE_ROTATIONAL_SPEED, DRIVE_STATUS, DRIVE_CONDITION]),
        ('Sizes of installed drives in megabytes', DRIVE_SIZE, []),
        ('Temperatures of installed drives in celsius', DRIVE_TEMP, []),
        ('Temperature thresholds of installed drives in celsius', DRIVE_TEMP_THRESHOLD, []),
        ('Maximum temperatures of installed drives in celsius', DRIVE_TEMP_MAX, []),
        ('Reference time of installed drives in hours', DRIVE_REFERENCE_TIME, []),
        scan_method=scrape.detect_complex,
    ))

    REGISTRY.register(BulkCollector(
        config,
        MEMORY_INDEX,
        'memory',
        not args.scan_once,
        ('Information about system memory', no_value, [MEMORY_LOCATION, MEMORY_MANUFACTURER, MEMORY_PART_NUMBER, MEMORY_STATUS, MEMORY_CONDITION]),
        ('Sizes of system memory modules in kilobytes', MEMORY_SIZE, []),
    ))

    # start metrics endpoint
    addr = args.server_address
    port = args.server_port
    print('starting metrics server on http://%s:%s' % (addr, port))
    server, thread = start_http_server(port, addr)
    print('ready!')

    thread.join()
    print('thread died!')
