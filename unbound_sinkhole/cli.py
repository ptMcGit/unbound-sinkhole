#!/usr/bin/env python3

"""A script for managing a DNS sinkhole for use with Unbound.

This script allows a user to generate a file for consumption by Unbound.
DNS sinkhole records are maintained in a database.
Each record has an ip address and url associated with it along with whether
or not it is blacklisted.

Users can import a record/set of records from the command-line, or
through files adhering to a specific format.

Interact with the database using files or single records:

    unbound-sinkhole delete [-r] [-f] FILE | RECORD
    unbound-sinkhole whitelist [-r] [-f] FILE | RECORD
    unbound-sinkhole blacklist [-r] [-f] FILE | RECORD

    unbound-sinkhole db [-p]

Enable/disable the sinkhole (this restarts unbound):

    unbound-sinkhole enable [-r]

    unbound-sinkhole disable [-r]
"""

import unbound_sinkhole.argparser as argparser
import unbound_sinkhole.db as db
import unbound_sinkhole.parsing as parsing
import unbound_sinkhole.unbound as unbound
import unbound_sinkhole.writer as writer
import unbound_sinkhole.conf as conf

import os
import sys

main_config = "/usr/local/etc/unbound-sinkhole/unbound-sinkhole.conf"

def _print_stderr(msg):
    print("{0}: {1}".format(sys.argv[0].split('/')[-1], msg),
          file=sys.stderr)

def main(cmdline_override=None):
    """Main entrypoint."""

    conf.initialize_confs(main_config)

    db.sinkhole_db = conf.sinkhole_db

    if cmdline_override is None:
        #args = argparser.parser.parse_args()
        args = argparser.parse_args()
    else:
        args = argparser.parse_args(cmdline_override)

    if args.sub_command == "reset":
        if db.purge_db():
            _print_stderr("DB successfully reset")

    if args.sub_command == "modify":
        db_arg = args.positional_arg

        if args.file:
            record_gen = process_files(db_arg)
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

    elif args.sub_command == "enable":
        writer.update_server_config(conf.server_conf, enable=True)
        _print_stderr('success')

    elif args.sub_command == "disable":
        writer.update_server_config(conf.server_conf, enable=False)
        _print_stderr('success')

    if args.reload:
        unbound.restart()

if __name__ == '__main__':
    main()
