from snmp_groups import BulkEnums

FAN_INDEX = '1.3.6.1.4.1.232.6.2.6.7.1.2.0'

FAN_LOCALE = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.7.1.3.0.%i' % i),
    'locale',
    {
        1: 'other',
        2: 'unknown',
        3: 'system',
        4: 'systemBoard',
        5: 'ioBoard',
        6: 'cpu',
        7: 'memory',
        8: 'storage',
        9: 'removable media',
        10: 'power supply',
        11: 'ambent',
        12: 'chassis',
        13: 'bridge card',
        14: 'management board',
        15: 'backplane',
        16: 'network slot',
        17: 'blade slot',
        18: 'virtual',
    }
)

FAN_PRESENT = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.7.1.4.0.%i' % i),
    'presence',
    {
        1: 'other',
        2: 'absent',
        3: 'present',
    }
)

FAN_PRESENCE_TEST = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.7.1.5.0.%i' % i),
    'presence_test',
    {
        1: 'other',
        2: 'tachOutput',
        3: 'spinDetect',
    }
)

FAN_SPEED = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.7.1.6.0.%i' % i),
    'speed',
    {
        1: 'other',
        2: 'normal',
        3: 'high',
    }
)

FAN_CONDITION = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.7.1.6.0.%i' % i),
    'condition',
    {
        1: 'other',
        2: 'normal',
        3: 'degraded',
        4: 'failed',
    }
)

# for debugging
FAN_VALUES = [
    FAN_LOCALE,
    FAN_PRESENT,
    FAN_PRESENCE_TEST,
    FAN_SPEED,
    FAN_CONDITION,
]
