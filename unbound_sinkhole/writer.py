"""
Writer funcions.

These functions help write data to the DNS sinkhole file
for consumption by unbound.
"""

import sqlite3
import db
import tempfile
import unbound

default_sinkhole_response = "always_nxdomain"
sinkhole_file = "sinkhole.conf"
template = 'local-zone "{0}" ' + default_sinkhole_response
include_statement = 'include: ' + sinkhole_file + '\n'

def records_to_file():
    """Write records to the sinkhole file.
    """
    with open(sinkhole_file, "w") as f:
        for r in db.get_blacklist():
           f.write(template.format(r.url) + '\n')


def update_server_config(config_file, enable=True):
    """Update the server config.

    Update the statement in the server config
    that causes the sinkhole file to be included.

    args:
        config_file: the config file to update
        enable: whether or not the statement is present;
            this determines whether sinkholing is enabled.
    """

    unbound.insert_line(config_file,
                        include_statement,
                        present=enable)

# def update_server_config(config_file, enable=True):
#     """Update the server configuration file.

#     Update the server configuration file by adding/removing
#     the include statement.

#     args:
#         config_file: the server config file to modify.
#         enable: whether or not the include statement should be
#            enabled.
#     """
#     # create temp file
#     temp_file = tempfile.mkstemp()

#     # create new file in temp file
#     # adding/omitting the include statement as needed
#     # overwrite existing file with the temp file
#     with open(config_file, "r") as cf, open(temp_file, "w") as tf:

#         server_clause =  '^\s*(server:)(\s)*(#.*)?$'
#         generic_clause = '^\s*([a-z]{1}[a-z-]*[a-z]{1}:)(\s)*(#.*)?$'


#         line = cf.readline()
#         while not re.match(server_clause, line):
#             tf.write(line)
#             line = cf.readline()

#         lines = [line]
#         line = cf.readline()
#         while not re.match(generic_clause, line):
#             lines.append(line)
#             line = cf.readline()
#         if enable:
#             if (include_statement not in lines):
#                 tf.write(line)
#         else:
#             try:
#                 lines.remove(include_statement)
#             except ValueError as e:
#                 ...
#         for line in lines:
#             tf.write(line)

#         tf.writelines(cf.readlines())
