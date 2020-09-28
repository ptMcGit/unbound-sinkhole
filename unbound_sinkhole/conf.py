from collections import defaultdict
import configparser
# db.py
import sys


sql_db = None
#sinkhole_db = None
sinkhole_file = None
#sinkhole_conf = None
unbound_conf = None

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]

# we can explicitly make assignments on it
this.configs = None

def initialize_confs(config_file):
    if (this.configs is None):
        cp = configparser.ConfigParser()
        cp.read(config_file)


        #breakpoint
#        from pprint import pprint as pp; from code import interact; interact(local=dict(globals(), **locals()))

        main_section = cp['main']



        # convert any empty strings to None
        d = {**dict(main_section),
             **dict( (key, None) for (key, val) in main_section.items() if val == '')}

        d = defaultdict(lambda : None, d)

        for k, v in d.items():
            setattr(this, k, v)

    else:
        msg = "Config file has already been imported."
        raise RuntimeError(msg)


# def get_confs(config_file):
#     """Get configuration values from the configuration file.

#     Read the configuration file and return the key-values such
#     unassigned keys' values are None.

#     Args:
#         config_file: the configuration file to read

#     Returns: a dict containing the configuration values.
#     """
#     cp = configparser.ConfigParser()
#     cp.read(config_file)
#     main_section = cp['main']

#     # convert any empty strings to None
#     d = {**dict(main_section),
#          **dict( (key, None) for (key, val) in main_section.items() if val == '')}

#     return defaultdict(lambda : None, d)
