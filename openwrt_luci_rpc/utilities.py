from .constants import Constants
import logging

log = logging.getLogger(__name__)


def normalise_keys(result):
    """Replace 17.06 keys with newer ones."""

    # named tuple keys cannot have spaces or begin with dots. Replace
    # those with underscores
    result = \
        {k.replace(".", "_").replace(" ", "_"): v for k, v in result.items()}

    for old_key, new_key in Constants.MODERN_KEYS.items():
        if old_key in result:
            result[new_key] = result[old_key]
            del result[old_key]

    return result


def get_key_from_dhcp(dhcp_result, mac, key = 'name'):
    """Determine a key from DHCP for this mac."""
    if dhcp_result:

        host = [x for x in dhcp_result.values()
                if x['.type'] == 'host'
                and 'mac' in x
                and key in x
                and x['mac'].upper() == mac]

        if host:
            log.debug("DHCP lookup {} for mac {} "
                      "found {}".format(mac, key, host[0][key]))
            return host[0][key]

    return None