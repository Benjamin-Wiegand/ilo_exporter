from snmp_groups import BulkEnums, BulkNumbers, BulkStrings

CPU_INDEX = '1.3.6.1.4.1.232.1.2.2.1.1.1'

CPU_NAME = BulkStrings(
    (lambda i: '1.3.6.1.4.1.232.1.2.2.1.1.3.%i' % i),
    'name',
)

CPU_SPEED = BulkNumbers(
    (lambda i: '1.3.6.1.4.1.232.1.2.2.1.1.4.%i' % i),
    'speed',
)

CPU_STEP = BulkNumbers(
    (lambda i: '1.3.6.1.4.1.232.1.2.2.1.1.5.%i' % i),
    'step',
)

CPU_STATUS = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.1.2.2.1.1.6.%i' % i),
    'status',
    {
        1: 'unknown',
        2: 'ok',
        3: 'degraded',
        4: 'failed',
        5: 'disabled',
    }
)

CORES_ENABLED = BulkNumbers(
    (lambda i: '1.3.6.1.4.1.232.1.2.2.1.1.15.%i' % i),
    'cores_enabled',
)

THREADS_AVAILABLE = BulkNumbers(
    (lambda i: '1.3.6.1.4.1.232.1.2.2.1.1.25.%i' % i),
    'threads_available',
)

CPU_POWER_STATUS = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.1.2.2.1.1.26.%i' % i),
    'power_status',
    {
        1: 'unknown',
        2: 'Low Powered',
        3: 'Normal Powered',
        4: 'High Powered',
    }
)

# for debugging
CPU_VALUES = [
    CPU_NAME,
    CPU_SPEED,
    CPU_STEP,
    CPU_STATUS,
    CORES_ENABLED,
    THREADS_AVAILABLE,
    CPU_POWER_STATUS,
]
