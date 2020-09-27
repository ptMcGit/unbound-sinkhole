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

import os
import sys

def main():
    """Main entrypoint."""

    args = argparser.parser.parse_args()

    if args.sub_command == "reset":
        db.purge_db()

    if args.sub_command == "modify":
        db_arg = args.positional_arg

        if args.file:
            record_gen = process_files(db_arg)
        else:
            record_gen = (r for r in (db_arg[0], db_arg[1]))

        if args.delete:
            db.delete_records(record_gen)
        elif args.whitelist:
            db.update_records(record_gen, blacklist=False)
        elif args.blacklist:
            db.update_records(record_gen, blacklist=True)


    elif args.sub_command == "enable":
        writer.update_server_config(config_file, enable=True)

    elif args.sub_command == "disable":
        writer.update_server_config(config_file, enable=False)

    if args.reload:
        unbound.restart()

if __name__ == '__main__':
    main()