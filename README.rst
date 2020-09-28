# `unbound-sinkhole`

## Overview

This is a command-line utility that generates files for consumption by Unbound (caching DNS server) that can be used to sinkhole IP addresses.

Users provide records, or files containing records, directly via the command-line to modify a database in which records are blacklisted or whitelisted.

The file generated from these records is included inside a specified Unbound configuration file, i.e. it writes an `include: <file>` statement in the server clause of the configuration file.

## How to Use it?

1. Assumptions

You are using unbound as your DNS server, and you have a configuration file with a server clause e.g.:

```
server:
    interface: 127.0.0.1
    ...
```

2. Prerequisites

By default the script expects a configuration file at `/usr/local/etc/unbound-sinkhole.conf` that uses `configparser` syntax. (See `./unbound_sinkhole/data/unbound-sinkhole.conf`).

Identify the appropriate server configuration file and set it as the value for `server_config` in the aforementioned `unbound-sinkhole.conf` file.

3. Perform the desired commands.

**Get help**

```
unbound-sinkhole -h
```

**Add to blacklist using a file**

```
unbound-sinkhole modify -f -b <file>
```

**Add a single record to the blacklist**

```
unbound-sinkhole modify -b <ip address> <host name>
```

**Add a single record to the whitelist**

```
unbound-sinkhole modify -w <ip address> <host name>
```

- can also provide a file to whitelist from

**Reset the blacklist**

```
unbound-sinkhole reset
```

**Enable/disable sinkholing**

```
unbound-sinkhole [enable|disable]
```

Use the `-r` flag to reload unbound.

## TODO

- fix language regarding blacklist/whitelist as it obscures how things work
- refactor away from module variable pattern in `conf.py`?
- add more helpful error messages
- create/use appropriate exception classes
- create setuptools installation script
- would exporting records be valuable?
- the ability to create and manage multiple files for different cases, e.g. not just `nxdomain`, but `refuse` etc.
- should be able to delete, say, all on the whitelist, or all on the blacklist--will need to change from mutually exclusive argparse args group
- generalize code for use with other operating systems such as Windows (change use of paths from strings to `Path`s)
