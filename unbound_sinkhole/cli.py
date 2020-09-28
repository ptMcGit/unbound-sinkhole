#!/usr/bin/env python3

"""A script for managing a DNS sinkhole through Unbound.

This script allows a user to generate a file for consumption by Unbound.
DNS sinkhole records are maintained in a database.
Each record has an ip address and url associated with it along with
whether or not it is blacklisted.

Users can import a record/set of records from the command-line, or
through files adhering to a specific format.

The CLI allows the following:

- Add/delete records
- Toggle blacklisting/whitelisting
- Enable/disable sinkhole
- Reload Unbound
"""

import sys

import unbound_sinkhole.argparser as argparser
import unbound_sinkhole.conf as conf
import unbound_sinkhole.db as db
import unbound_sinkhole.parsing as parsing
import unbound_sinkhole.unbound as unbound
import unbound_sinkhole.writer as writer

MAIN_CONFIG = "/usr/local/etc/unbound-sinkhole/unbound-sinkhole.conf"

def _print_stderr(msg):
    print("{0}: {1}".format(sys.argv[0].split('/')[-1], msg),
          file=sys.stderr)

def _modify(args):
    db_arg = args.positional_arg

    if args.file:
        record_gen = parsing.process_files(db_arg)
    else:
        record_gen = (r for r in [(db_arg[0], db_arg[1])])

    if args.delete:
        if db.delete_records(record_gen):
            _print_stderr('success')
    elif args.whitelist:
        if db.update_records(record_gen, blacklist=False):
            _print_stderr('success')
    elif args.blacklist:
        if db.update_records(record_gen, blacklist=True):
            _print_stderr('success')


def main(cmdline_override=None):
    """Main entrypoint."""

    conf.initialize_confs(MAIN_CONFIG)

    db.SINKHOLE_DB = conf.SINKHOLE_DB

    if cmdline_override is None:
        #args = argparser.parser.parse_args()
        args = argparser.parse_args()
    else:
        args = argparser.parse_args(cmdline_override)

    if args.sub_command == "reset":
        if db.purge_db():
            _print_stderr("DB successfully reset")

    elif args.sub_command == "modify":
        _modify(args)

    elif args.sub_command == "enable":
        writer.update_server_config(conf.SERVER_CONF, enable=True)
        _print_stderr('success')

    elif args.sub_command == "disable":
        writer.update_server_config(conf.SERVER_CONF, enable=False)
        _print_stderr('success')

    if args.reload:
        unbound.restart()

if __name__ == '__main__':
    main()
