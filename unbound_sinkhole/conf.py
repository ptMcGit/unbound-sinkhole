"""Module that reads and stores configuration.

Configuration is read from a configuration file; then
the key value pairs are attached to the module so
that they function as module-level variables.
"""

from collections import defaultdict
import configparser
import sys

SINKHOLE_DB = None
SINKHOLE_CONF = None
UNBOUND_CONF = None
SERVER_CONF = None

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# we can explicitly make assignments on it
this.configs = None

def initialize_confs(config_file):
    """Read configs from config file.

    Read the key-value pairs from the config file
    provided, and attach them to the module.

    Args:
        config_file: the configuration file to read from.
    """

    if this.configs is None:
        parser = configparser.ConfigParser()

        parser.read(config_file)

        main_section = parser['main']

        # convert any empty strings to None
        data = {**dict(main_section),
             **dict( (key, None) for (key, val) in main_section.items() if val == '')}

        data = defaultdict(lambda : None, data)

        for key, val in data.items():
            setattr(this, key.upper(), val)

        return

    raise RuntimeError("Config file has already been imported.")
