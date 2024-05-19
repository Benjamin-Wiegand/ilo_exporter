# just a highly simplified wrapper over pysnmp

from pysnmp.hlapi import NoSuchInstance, Integer, Integer32, Counter32, OctetString, ObjectType, ObjectIdentity, getCmd, nextCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData

# for bulk requests. I find large requests crash the ilo (lol)
MAX_CHUNK = 64


class SnmpConfiguration(object):
    def __init__(self, engine: SnmpEngine, auth: CommunityData, transport: UdpTransportTarget, context: ContextData):
        self.engine = engine
        self.auth = auth
        self.transport = transport
        self.context = context


class AgentError(Exception):
    pass


class EngineError(Exception):
    pass


def process_value(var_bind) -> str | int | float | None:
    val = var_bind[1]
    if isinstance(val, NoSuchInstance):
        return None
    elif isinstance(val, Integer) or isinstance(val, Integer32) or isinstance(val, Counter32):
        return int(val)
    elif isinstance(val, OctetString):
        return str(val)
    else:
        print('i dunno:', val)
        print('unhandled type:', type(val))
        return val.prettyPrint()


def snmp_get(c: SnmpConfiguration, oid: str | tuple[int]) -> str | int | float | None:
    """ gets a single oid """
    return snmp_get_all(c, oid)[0]


def snmp_get_all(c: SnmpConfiguration, *oid: str | tuple[int]) -> list[str | int | float | None]:
    """ does a bulk request """
    if len(oid) > MAX_CHUNK:
        # split it up to not break the target
        results = []
        results.extend(snmp_get_all(c, *oid[:MAX_CHUNK]))
        results.extend(snmp_get_all(c, *oid[MAX_CHUNK:]))
        return results

    # do snmp get
    it = getCmd(c.engine, c.auth, c.transport, c.context, *[ObjectType(ObjectIdentity(x)) for x in oid])
    engine_err, agent_err, agent_err_index, var_binds = next(it)

    # handle errors
    if engine_err:
        raise EngineError(engine_err)
    elif agent_err:
        raise AgentError('%s at %s' % (agent_err.prettyPrint(), var_binds[int(agent_err_index) - 1] if agent_err_index else '?'))

    # debugging
    # for var_bind in var_binds:
    #     print('got snmp:', ' = '.join([x.prettyPrint() for x in var_bind]))

    return [process_value(vb) for vb in var_binds]


def snmp_walk(c: SnmpConfiguration, base_oid: str) -> list[tuple[str, str | int | float | None]]:
    """ does a walk within the range of a specified base oid """
    results = []

    # do snmp get
    it = nextCmd(c.engine, c.auth, c.transport, c.context, ObjectType(ObjectIdentity(base_oid)))
    within = True
    while within:
        engine_err, agent_err, agent_err_index, var_binds = next(it)

        # handle errors
        if engine_err:
            raise EngineError(engine_err)
        elif agent_err:
            raise AgentError('%s at %s' % (agent_err.prettyPrint(), var_binds[int(agent_err_index) - 1] if agent_err_index else '?'))

        for var_bind in var_binds:
            # print(var_bind)
            oid = str(var_bind[0].getOid())
            if oid.startswith(base_oid):
                results.append((oid, process_value(var_bind)))
            else:
                within = False

        if len(var_binds) == 0:
            within = False

    return results
