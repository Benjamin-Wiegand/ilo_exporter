from snmp_groups import BulkEnums, BulkNumbers

TEMP_INDEX = '1.3.6.1.4.1.232.6.2.6.8.1.2.0'

TEMP_CELSIUS = BulkNumbers(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.8.1.4.0.%i' % i),
    'celsius',
)

TEMP_THRESHOLD = BulkNumbers(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.8.1.5.0.%i' % i),
    'threshold',
)

TEMP_SENSOR_LOCALE = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.8.1.3.0.%i' % i),
    'sensor_locale',
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
    }
)

TEMP_THRESHOLD_TYPE = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.8.1.7.0.%i' % i),
    'threshold_type',
    {
        1: 'other',
        5: 'blowout',
        9: 'caution',
        15: 'critical',
        16: 'noreaction',
    }
)

TEMP_CONDITION = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.6.8.1.6.0.%i' % i),
    'condition',
    {
        1: 'other',
        2: 'normal',
        3: 'high',
    }
)

# for debugging
TEMP_VALUES = [
    TEMP_SENSOR_LOCALE,
    TEMP_THRESHOLD_TYPE,
    TEMP_CONDITION,
    TEMP_CELSIUS,
    TEMP_THRESHOLD,
]
