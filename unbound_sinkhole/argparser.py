import argparse

def parse_args(args=None):
    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)





file_arg = (['--file',
             '--f'],
            {'dest': 'file',
             'help': 'Whether File to load data from.',
             'nargs': 1,
             'default': False,
             'required': False})

record_arg = (['record']) #,
               #{'help': 'Record to add to DB.'})

reload_arg = (['--reload',
             '-r'],
            {'dest': 'reload',
             'help': 'Whether or not to reload Unbound.',
             'action': 'store_true',
             'required': False})

delete_arg = (['--delete',
               '-d'],
              {'dest': 'delete',
               'help': 'Delete record(s) from the DB.',
               'action': 'store_true'})

whitelist_arg = (['--whitelist',
               '-w'],
              {'dest': 'whitelist',
               'help': 'Whitelist record(s) from the DB.',
               'action': 'store_true'})
blacklist_arg = (['--blacklist',
               '-b'],
              {'dest': 'blacklist',
               'help': 'Blacklist record(s) from the DB.',
               'action': 'store_true'})


parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument(*reload_arg[0],
                    **reload_arg[1])

subparsers = parser.add_subparsers(dest='sub_command',
                                   help='Subcommand help',
                                   required=True)

modify_db_parser = subparsers.add_parser('modify',
                                         help='modify help')


modify_db_parser.add_argument(*file_arg[0],
                              **file_arg[1])

modify_db_parser.add_argument('positional_arg',
                              nargs='+')

# type_group = modify_db_parser.add_mutually_exclusive_group(required=True)

# type_group.add_argument(*file_arg[0],
#                         **file_arg[1])

# type_group.add_argument('record') #*record_arg[0]) #**record_arg[1])


transaction_arg_group = modify_db_parser.add_mutually_exclusive_group(required=True)

transaction_arg_group.add_argument(*delete_arg[0],
                                   **delete_arg[1])

transaction_arg_group.add_argument(*whitelist_arg[0],
                                   **whitelist_arg[1])

transaction_arg_group.add_argument(*blacklist_arg[0],
                                   **blacklist_arg[1])

# whitelist_parser = subparsers.add_parser('whitelist', help='whitelist help')
# blacklist_parser = subparsers.add_parser('blacklist', help='blacklist help')

enable_parser = subparsers.add_parser('enable', help='enable help')

disable_parser = subparsers.add_parser('disable', help='disable help')

disable_parser = subparsers.add_parser('reset', help='Reset the database, removing all records.')
