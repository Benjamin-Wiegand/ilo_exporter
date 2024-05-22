from snmp import SnmpConfiguration, snmp_get_all


class EnumMapping(object):
    def __init__(self, value: int, value_map: dict[int, str]):
        self._value = value
        self._value_map = value_map

    def get_value(self) -> int:
        return self._value

    def get_name(self) -> str | None:
        if self._value not in self._value_map.keys():
            return None
        return self._value_map[self._value]

    def __str__(self) -> str:
        name = self.get_name()
        if name is None:
            return 'unknown state %i' % self._value
        return name


class BulkValues(object):
    def __init__(self, oid_template, name: str):
        self._oid_template = oid_template
        self._name = name

    @property
    def name(self):
        return self._name

    def get_values(self, c: SnmpConfiguration, indexes: list) -> dict:
        oids = [self._oid_template(index) for index in indexes]
        results = snmp_get_all(c, *oids)
        result_dict = {}
        for index in indexes:
            result_dict[index] = results.pop(0)

        return result_dict


class BulkDummyValue(BulkValues):
    def __init__(self, name: str):
        super().__init__(None, name)
        self._name = name

    def get_values(self, _: SnmpConfiguration, indexes: list) -> dict:
        result_dict = {}
        for index in indexes:
            result_dict[index] = 1

        return result_dict


class BulkPredeterminedValues(BulkValues):
    def __init__(self, name: str, values: dict = {}):
        super().__init__(None, name)
        self._name = name
        self.values = values

    def get_values(self, c: SnmpConfiguration, indexes: list) -> dict:
        return self.values


class BulkNumbers(BulkValues):
    def __init__(self, oid_template, name: str):
        super().__init__(oid_template, name)

    def get_values(self, c: SnmpConfiguration, indexes: list) -> dict:
        result_dict = super().get_values(c, indexes)
        for key in result_dict.keys():
            if not isinstance(result_dict[key], int):
                result_dict[key] = -1
                print('unknown value (not an int):', result_dict[key])
        return result_dict


class BulkEnums(BulkNumbers):
    def __init__(self, oid_template, name: str, value_map: dict):
        super().__init__(oid_template, name)
        self._value_map = value_map

    @property
    def state_map(self):
        return self._value_map

    def get_values(self, c: SnmpConfiguration, indexes: list) -> dict:
        result_dict = super().get_values(c, indexes)
        for key in result_dict.keys():
            value = result_dict[key]
            result_dict[key] = EnumMapping(value, self._value_map)
            if __debug__ and value not in self._value_map:
                print('unexpected enum value from ilo for %s: %i' % (self.name, value))
        return result_dict


class BulkStrings(BulkValues):
    def __init__(self, oid_template, name: str):
        super().__init__(oid_template, name)

    def get_values(self, c: SnmpConfiguration, indexes: list) -> dict:
        result_dict = super().get_values(c, indexes)
        for key in result_dict.keys():
            if not isinstance(result_dict[key], str):
                result_dict[key] = 'unknown value: %s' % str(result_dict[key])
                print('unknown value (not a string):', result_dict[key])
            else:
                result_dict[key] = result_dict[key].strip()
        return result_dict
