"""
Unbound related functions.
"""


import os
import re
import shutil
import subprocess
import tempfile

_unbound_checkconf = '/usr/sbin/unbound-checkconf'
_unbound_service = 'unbound.service'

server_clause_re =  '^\s*(server:)(\s)*(#.*)?$'
generic_clause_re = '^\s*([a-z]{1}[a-z-]*[a-z]{1}:)(\s)*(#.*)?$'



def insert_line(config_file, statement,  present=True):
    """Idempotently insert/remove line from file.

    Update the server configuration file by adding/removing
    the include statement.

    args:
        config_file: the server config file to modify.
        present: whether or not the include statement should be
           enabled.
    """
    # create temp file
    temp_file = tempfile.mkstemp()[1]

    # create new file in temp file
    # adding/omitting the include statement as needed
    # overwrite existing file with the temp file
    with open(config_file, "r") as cf, open(temp_file, "w") as tf:

        line = cf.readline()
        while not re.match(server_clause_re, line):
            tf.write(line)
            line = cf.readline()

        server_clause = line
        lines = []
        line = cf.readline()
        while not re.match(generic_clause_re, line):
            lines.append(line)
            line = cf.readline()
        lines.append(line)

        tf.write(server_clause)
        if present:
            if (statement not in lines):
                # insert the statement with leading whitespace that should be present

                tf.write(re.match('^(\s*)(.*)$', lines[0]).groups()[0] +
                         statement)
        else:
            try:
                lines.remove(statement)
            except ValueError as e:
                pass
        for line in lines:
            tf.write(line)

        tf.writelines(cf.readlines())
        return True


    # copy tempfile contents to config file
    # (avoiding copying the file, changing perms, etc.)
    with open(config_file, "w") as cf, open(temp_file, "r") as tf:
        cf.writelines(tf.readlines())


def test_server_config(config):
    """ Use unbound-checkconf to check config.

    args:
        config: file to check
    raises:
        CalledProcessError when exit status not 0.
    """
    subprocess.check_call([_unbound_checkconf, config])

def get_substate():
    return subprocess.call('systemctl show --property="SubState" ' + unbound_service)

def restart():
    """ Restart unbound using systemd.
    """
    if os.geteuid() != 0:
        raise Exception('must be root')

    substate = get_substate()
    if substate != 'SubState=running':
        raise Exception('unbound is not running')
    subprocess.call('systemctl restart ' + unbound_service)
