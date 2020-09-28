"""Module with writer funcions.

These functions help write data to the DNS sinkhole file
for consumption by Unbound.
"""

import unbound_sinkhole.conf as conf
import unbound_sinkhole.db as db
import unbound_sinkhole.unbound as unbound

_DEFAULT_SINKHOLE_RESPONSE = "always_nxdomain"
TEMPLATE = 'local-zone "{0}" ' + _DEFAULT_SINKHOLE_RESPONSE
INCLUDE_STATEMENT = 'include: {0}\n'

def records_to_file():
    """Write records to the sinkhole file.
    """
    with open(conf.SINKHOLE_CONF, "w") as sfh:
        for record in db.get_blacklist():
            sfh.write(TEMPLATE.format(record.url) + '\n')

def update_server_config(config_file, enable=True):
    """Update the server config.

    Update the statement in the server config
    that causes the sinkhole file to be included.

    args:
        config_file: the config file to update
        enable: whether or not the statement is present;
            this determines whether sinkholing is enabled.
    """

    return unbound.insert_line(config_file,
                        INCLUDE_STATEMENT.format(conf.SINKHOLE_CONF),
                        present=enable)
