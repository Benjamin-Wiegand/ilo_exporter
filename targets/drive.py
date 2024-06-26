from snmp_groups import BulkEnums, BulkNumbers, BulkStrings

DRIVE_INDEX = '1.3.6.1.4.1.232.3.2.5.1.1.2'

# controller index
# DRIVE_CONTROLLER = BulkNumbers(
#     (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 1) + i),
#     'controller'
# )

DRIVE_PORT = BulkStrings(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 62) + i),
    'port'
)

DRIVE_BOX = BulkNumbers(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 63) + i),
    'box'
)

DRIVE_BAY = BulkNumbers(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 5) + i),
    'bay'
)

DRIVE_VENDOR = BulkStrings(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 3) + i),
    'vendor',
)

# this may be slightly redundant
DRIVE_LOCATION = BulkStrings(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 64) + i),
    'location',
)

DRIVE_SERIAL = BulkStrings(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 51) + i),
    'serial',
)

DRIVE_FIRMWARE = BulkStrings(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 4) + i),
    'firmware',
)

DRIVE_SIZE = BulkNumbers(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 45) + i),
    'size',
)

DRIVE_LINK_RATE = BulkEnums(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 65) + i),
    'link_rate',
    {
        1: 'other',
        2: '1.5Gbps',
        3: '3.0Gbps',
        4: '6.0Gbps',
        5: '12.0Gbps',
    }
)

DRIVE_TEMP = BulkNumbers(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 70) + i),
    'temperature'
)

DRIVE_TEMP_THRESHOLD = BulkNumbers(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 71) + i),
    'temperature_threshold'
)

DRIVE_TEMP_MAX = BulkNumbers(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 72) + i),
    'temperature_maximum'
)

DRIVE_STATUS = BulkEnums(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 6) + i),
    'status',
    {
        1: 'Other',
        2: 'Ok',
        3: 'Failed',
        4: 'Predictive Failure',
        5: 'Erasing',
        6: 'Erase Done',
        7: 'Erase Queued',
        8: 'SSD Wear Out',
        9: 'Not Authenticated',
    }
)

DRIVE_CONDITION = BulkEnums(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 37) + i),
    'condition',
    {
        1: 'other',
        2: 'ok',
        3: 'degraded',
        4: 'failed',
    }
)

DRIVE_REFERENCE_TIME = BulkNumbers(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 9) + i),
    'reference_time'
)

DRIVE_SUPPORTS_PREDICTIVE_FAILURE_MONITORING = BulkEnums(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 52) + i),
    'predictive_failure',
    {
        1: 'other',
        2: 'notAvailable',
        3: 'available'
    }
)

DRIVE_SMART_STATUS = BulkEnums(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 57) + i),
    'smart_status',
    {
        1: 'other',
        2: 'ok',
        3: 'replaceDrive'
    }
)

DRIVE_ROTATIONAL_SPEED = BulkEnums(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 59) + i),
    'rotational_speed',
    {
        1: 'other',
        2: '7200 rpm',
        3: '10k rpm',
        4: '15k rpm',
        5: 'ssd',
    }
)

DRIVE_MEDIA_TYPE = BulkEnums(
    (lambda i: (1, 3, 6, 1, 4, 1, 232, 3, 2, 5, 1, 1, 69) + i),
    'media_type',
    {
        1: 'other',
        2: 'rotatingPlatters',
        3: 'solidState',
    }
)


# there appear to be a hell of a lot more, but I don't have the time to add them all right now
# here is a reference: https://oidref.com/1.3.6.1.4.1.232.3.2.5.1.1
