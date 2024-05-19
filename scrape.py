from snmp import snmp_get_all, snmp_walk, SnmpConfiguration, SnmpEngine, CommunityData, UdpTransportTarget, ContextData


def detect_things(c: SnmpConfiguration, base_oid: str) -> list[int]:
    """ Scans for things and returns a list of their ids. """
    things = []
    for _, index in snmp_walk(c, base_oid):
        assert isinstance(index, int)
        assert index not in things
        things.append(index)
    return things


# because of the way drive indexing works, this is the simplest way I can think to do it without over-complicating
# everything else
def detect_complex(c: SnmpConfiguration, base_oid: str) -> list[tuple[int]]:
    """ Scans for things and returns a list of their oid indexes. """
    drives = []
    for oid, _ in snmp_walk(c, base_oid):
        index = oid[len(base_oid) + 1:]
        index = (*[int(i) for i in index.split('.')],)
        assert index not in drives
        drives.append(index)
    return drives


if __name__ == '__main__':
    from targets.fan import FAN_VALUES, FAN_INDEX
    from targets.temp import TEMP_VALUES, TEMP_INDEX
    from targets.cpu import CPU_VALUES, CPU_INDEX
    from targets.memory import MEMORY_VALUES, MEMORY_INDEX
    from targets.drive import DRIVE_INDEX
    from targets.logical_drive import LOGICAL_DRIVES_INDEX

    config = SnmpConfiguration(
        SnmpEngine(),
        CommunityData('deeznuts'),
        UdpTransportTarget(('192.168.100.88', 161)),
        ContextData(),
    )

    print('scanning hardware...')
    fans = detect_things(config, FAN_INDEX)
    temp_sensors = detect_things(config, TEMP_INDEX)
    cpus = detect_things(config, CPU_INDEX)
    logical_drives = detect_things(config, LOGICAL_DRIVES_INDEX)
    drives = detect_complex(config, DRIVE_INDEX)
    memory_slots = detect_things(config, MEMORY_INDEX)

    print('\'puter has', len(fans), 'fans')
    print('\'puter has', len(temp_sensors), 'temp sensors')
    print('\'puter has', len(cpus), 'processors')
    print('\'puter has', len(logical_drives), 'logical drives')
    print('\'puter has', len(drives), 'physical drives')
    print('\'puter has', len(memory_slots), 'memory slots')

    for ilo_enum in FAN_VALUES:
        states = ilo_enum.get_values(config, fans)
        for fan in fans:
            print('fan', fan, ilo_enum.name, 'is', states[fan])
        print()

    for value in TEMP_VALUES:
        states = value.get_values(config, temp_sensors)
        for sensor in temp_sensors:
            print('temperature', sensor, value.name, 'is', states[sensor])
        print()

    for value in CPU_VALUES:
        states = value.get_values(config, cpus)
        for cpu in cpus:
            print('cpu', cpu, value.name, 'is', states[cpu])
        print()

    for value in MEMORY_VALUES:
        states = value.get_values(config, memory_slots)
        for slot in memory_slots:
            print('memory slot', slot, value.name, 'is', states[slot])
        print()

