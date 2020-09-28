"""Module with Unbound related functions.
"""

import os
import re
import subprocess
import tempfile

_UNBOUND_CHECKCONF = '/usr/sbin/unbound-checkconf'
_UNBOUND_SERVICE = 'unbound.service'

_SERVER_CLAUSE_RE =  r'^\s*(server:)(\s)*(#.*)?$'
_GENERIC_CLAUSE_RE = r'^\s*([a-z]{1}[a-z-]*[a-z]{1}:)(\s)*(#.*)?$'

def insert_line(config_file, statement,  present=True):
    """Idempotently nsert/remove line from file.

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
    with open(config_file, "r") as cfh, open(temp_file, "w") as tfh:

        line = cfh.readline()
        while not re.match(_SERVER_CLAUSE_RE, line):
            tfh.write(line)
            line = cfh.readline()

        server_clause = line
        lines = []
        line = cfh.readline()
        while not re.match(_GENERIC_CLAUSE_RE, line):
            lines.append(line)
            line = cfh.readline()
        lines.append(line)

        tfh.write(server_clause)
        if present:
            if statement not in lines:
                # insert the statement with leading whitespace that should be present

                tfh.write(re.match(r'^(\s*)(.*)$', lines[0]).groups()[0] +
                         statement)
        else:
            try:
                lines.remove(statement)
            except ValueError:
                pass
        for line in lines:
            tfh.write(line)

        tfh.writelines(cfh.readlines())

    # copy tempfile contents to config file
    # (avoiding copying the file, changing perms, etc.)
    with open(config_file, "w") as cfh, open(temp_file, "r") as tfh:
        cfh.writelines(tfh.readlines())

    return True

def test_server_config(config):
    """Use unbound-checkconf to check config.

    args:
        config: file to check
    raises:
        CalledProcessError when exit status not 0.
    """
    subprocess.check_call([_UNBOUND_CHECKCONF, config])

def get_substate():
    """Get the systemd substate of the Unbound service.
    """
    return subprocess.call('systemctl show --property="SubState" ' + _UNBOUND_SERVICE)

def restart():
    """Restart unbound using systemd.
    """
    if os.geteuid() != 0:
        raise Exception('must be root')

    substate = get_substate()
    if substate != 'SubState=running':
        raise Exception('unbound is not running')
    subprocess.call('systemctl restart ' + _UNBOUND_SERVICE)
