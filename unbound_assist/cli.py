#!/usr/bin/env python3

"""A script for managing a DNS sinkhole for use with Unbound.

This script allows a user to generate a file for consumption by Unbound.
DNS sinkhole records are maintained in a database.
Each record has an ip address and url associated with it along with whether
or not it is blacklisted.

Users can import a record/set of records from the command-line, or
through files adhering to a specific format.

Interact with the database using files or single records:

    unbound-sinkhole db [-r] [-d] [-f] FILE | RECORD
    unbound-sinkhole db [-r] [-w] [-f] FILE | RECORD
    unbound-sinkhole db [-r] [-b] [-f] FILE | RECORD

    unbound-sinkhole db [-p]

Enable/disable the sinkhole (this restarts unbound):

    unbound-sinkhole enable [-r]

    unbound-sinkhole disable [-r]
"""


import os
import sites as site_utils

sub_commands = set("purge", "enable", "disable", "reload", "modify")

sites_list = os.getenv('HOME') + 'unbound-assist-sites'  # TODO /etc/unbound-assist/sites-list

whitelist = os.getenv('HOME') + 'unbound-assist-whitelist'  # TODO /etc/unbound-assist/whitelist'

server_config = os.getenv('HOME') + 'unbound-server-config'  # todo /etc/unbound/unbound.conf.d/unbound.conf

def main():
    """ Parse command-line and provide desired action."""

    import sys
    if sys.argv[1] is None:
        raise Exception("one arg required")

    sub_command = sys.argv.pop()

    if sub_command == "db":
        args = # parse db args
        args['action'](args)
    elif sub_command == "enable":
        args = # parse enable args
        writer.update_server_config(config_file, enable=True)
    elif sub_command == "disable":
        args = # parse disable args
        writer.update_server_config(config_file, enable=True)
        disable_sinkhole()
    else:
        raise Exception("invalid sub command")

    #if restart
    unbound.restart()

    # import argparse

    # parser = argparse.ArgumentParser(description=__doc__)

    # # ADD EACH TYPE OF ARGUMENT TO ARG PARSER
    # # one or more parameters per addArgument
    # parser.add_argument(
    #     '--sites-list',
    #     '-u',
    #     default=sites_list, # default value
    #     dest='sites_list', # where to store the variable
    #     help='The sites to pull data from',
    #     metavar='SITES_LIST',
    #     nargs=1,
    #     type=str,
    #     required=True)

    # parser.add_argument(
    #     '--server-config',
    #     '-s',
    #     default=None, # default value
    #     dest='server_config', # where to store the variable
    #     help='The config file containing the unbound server clause that is to be modified to include sinkholing files',
    #     metavar='SERVER_CONFIG',
    #     nargs=1,
    #     type=str,
    #     required=True)

    # # parse the args
    # #  - optional: includes the main config file
    # #  - mandatory: includes location of server config file
    # # read the unbound-assist config file
    # # for each entry in config file
    # #   download the CSV list
    # #   create the sinkholefile
    # #     add appropriate entry for each entry
    # #   mark as successful/fail?
    # # open the unbound conf file
    # # find the server clause
    # # insert include statements for successful writes

    # args = parser.parse_args()
    # print(parser)

    # with open(str(args.sites_list[0]), 'r') as f:
    #     sites = f.read().splitlines()

    # for site in sites:
    #     new_list = site_utils.create_sinklist(site)
    #     site_utils.register_list(new_list, args.server_config)

if __name__ == '__main__':
    main()
