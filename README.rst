# unbound-assist

version 1

Command-line utility that assists in sinkholing IP addresses.

It downloads CSV lists from providers found in ~/.unbound-assist (or the desired config file), and modifies an existing unbound config file to sinkhole the domains found on thos lists.


version 2

Add new whitelist records:

unbound-assist insert -u -w -f "file"

Add new blacklist records:

unbound-assist insert -u -b -f "file"

Add new whitelist record:

unbound-assist insert -u -w -r <ip> <url>

Add new blacklist record:

unbound-assist insert -u -w -r <ip> <url>

Purge the database

unbound-assist purge -u -w -b

Reload unbound

unbound-assist update

Disable the database

unbound-assist disable
