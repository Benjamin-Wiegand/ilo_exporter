from snmp_groups import BulkEnums, BulkNumbers, BulkStrings

MEMORY_INDEX = '1.3.6.1.4.1.232.6.2.14.13.1.1'

MEMORY_LOCATION = BulkStrings(
    (lambda i: '1.3.6.1.4.1.232.6.2.14.13.1.13.%i' % i),
    'location',
)

MEMORY_MANUFACTURER = BulkStrings(
    (lambda i: '1.3.6.1.4.1.232.6.2.14.13.1.9.%i' % i),
    'manufacturer',
)

MEMORY_PART_NUMBER = BulkStrings(
    (lambda i: '1.3.6.1.4.1.232.6.2.14.13.1.10.%i' % i),
    'part_number',
)

MEMORY_SIZE = BulkNumbers(
    (lambda i: '1.3.6.1.4.1.232.6.2.14.13.1.6.%i' % i),
    'size',
)

# this is an enum, but I don't know the mappings
# I also don't have HP smart ram for testing
# MEMORY_TECHNOLOGY = BulkNumbers(
#     (lambda i: '1.3.6.1.4.1.232.6.2.14.13.1.8.%i' % i),
#     'technology',
# )

# this is another enum, but I don't know the mappings
# MEMORY_TYPE = BulkNumbers(
#     (lambda i: '1.3.6.1.4.1.232.6.2.14.13.1.7.%i' % i),
#     'type',
# )

MEMORY_STATUS = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.14.13.1.19.%i' % i),
    'status',
    {
        1: 'other',
        2: 'notPresent',
        3: 'present',
        4: 'good',
        5: 'add',
        6: 'upgrade',
        7: 'missing',
        8: 'doesNotMatch',
        9: 'notSupported',
        10: 'badConfig',
        11: 'degraded',
        12: 'spare',
        13: 'partial',
    }
)

MEMORY_CONDITION = BulkEnums(
    (lambda i: '1.3.6.1.4.1.232.6.2.14.13.1.20.%i' % i),
    'condition',
    {
        1: 'other',
        2: 'ok',
        3: 'degraded',
        4: 'degradedModuleIndexUnknown',
    }
)

# for debugging
MEMORY_VALUES = [
    MEMORY_LOCATION,
    MEMORY_MANUFACTURER,
    MEMORY_PART_NUMBER,
    MEMORY_SIZE,
    MEMORY_STATUS,
    MEMORY_CONDITION
]
