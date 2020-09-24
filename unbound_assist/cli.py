#!/usr/bin/env python3

import os
import sites as site_utils

# other functions here

# Describe contents and usage of the module.

"""<Simply, what does the script do?>.

<Long description>.

    Typical usage example:



"""

sites_list = os.getenv('HOME') + 'unbound-assist-sites'  # TODO /etc/unbound-assist/sites-list

whitelist = os.getenv('HOME') + 'unbound-assist-whitelist'  # TODO /etc/unbound-assist/whitelist'

server_config = os.getenv('HOME') + 'unbound-server-config'  # todo /etc/unbound/unbound.conf.d/unbound.conf


# def f():
#     """<Simply, what does the function do?>.

#     <Long description>.

#     Args:
#         <arg1>: <what arg1 does>.
#         <arg2>: <what arg2 does>.

#     Returns:
#         <What does it return?>

#     Raises:
#         <What/when does it raise an error?>
#     """

# class C():
#     """<Summary of class here.>

#     <Long description>.

#     Attributes:
#         attr1: <about attr1>.
#         attr2: <about attr2>.
#     """

#     def __init__(self, <args>):
#         """<Description>."""
#         self.arg1 = arg1

#     def public_method(self):
#         """Performs operation blah."""


def main():
    """ Parse command-line and provide desired action."""

    import argparse

    parser = argparse.ArgumentParser(description=__doc__)

    # ADD EACH TYPE OF ARGUMENT TO ARG PARSER
    # one or more parameters per addArgument
    parser.add_argument(
        '--sites-list',
        '-u',
        default=sites_list, # default value
        dest='sites_list', # where to store the variable
        help='The sites to pull data from',
        metavar='SITES_LIST',
        nargs=1,
        type=str,
        required=True)

    parser.add_argument(
        '--server-config',
        '-s',
        default=None, # default value
        dest='server_config', # where to store the variable
        help='The config file containing the unbound server clause that is to be modified to include sinkholing files',
        metavar='SERVER_CONFIG',
        nargs=1,
        type=str,
        required=True)

    # parse the args
    #  - optional: includes the main config file
    #  - mandatory: includes location of server config file
    # read the unbound-assist config file
    # for each entry in config file
    #   download the CSV list
    #   create the sinkholefile
    #     add appropriate entry for each entry
    #   mark as successful/fail?
    # open the unbound conf file
    # find the server clause
    # insert include statements for successful writes

    args = parser.parse_args()
    print(parser)

    with open(str(args.sites_list[0]), 'r') as f:
        sites = f.read().splitlines()

    for site in sites:
        new_list = site_utils.create_sinklist(site)
        site_utils.register_list(new_list, args.server_config)
        #breakpoint

    from pprint import pprint as pp; from code import interact; interact(local=dict(globals(), **locals()))


if __name__ == '__main__':
    main()
