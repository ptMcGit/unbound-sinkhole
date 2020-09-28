""" Module for parsing and validating data.

Does the following:

- parsing records from files
- validates records

The expected format for records is

    <ip address> <url>
"""

import ipaddress
from pathlib import Path
import re

def _check_hostname(hostname):
    """Thorough hostname validation.

    Predicate function that checks hostname according
    to the prevailing Internet specs.

    Not mine - from stackoverflow

    Args:
        hostname: hostname to check

    Returns: True if hostname is valid, else False.
    """
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def _check_ip_addr(address):
    """Check if IPv4/6 address is valid.

    Predicate function that checks if IP address
    is valid.

    Args:
        address: The address to check.

    Returns: True if hostname is valid, else False.
    """
    try:
        return ipaddress.ip_address(address)
    except ValueError:
        return False

def record_check(record):
    """Check if a record is valid or not.

    Args:
        record: The record to check.

    Returns: The record when valid, else None.
    """
    # remove any successive whitespace, and strip sides
    record = re.sub(r'^(\s*)(\S+)(\s+)(\S+)(\s*)$',
                    '\\2 \\4',
                    record).split(' ')

    if not _check_ip_addr(record[0]):
        return None
    if not _check_hostname(record[1]):
        return None
    return record

def _gen_records(filelist):
    """A generator function for records.

    Take a list of files and create a
    generator that furnishes records.

    Args:
        filelist: list from which records are drawn.

    Returns: yields records.
    """
    # if no errors
    for item in filelist:
        with open(item, 'r') as fileh:
            for line in fileh:
                yield tuple(record_check(line))


def process_files(filelist):
    """Checks files provided then generates records.

    The files provided are checked along with each
    of the records.

    If all of the file and records are valid a
    generator is returned.

    Args:
        filelist: files to process.

    Returns: a generator containing records.

    Raises: Exception when a path doesn't exist,
        or when a bad record is found.
    """
    # evaluate each file and each record first
    for item in filelist:
        if not Path(item).exists():
            raise Exception("path does not exist")
        with open(item, 'r') as fileh:
            count = 1
            for line in fileh:
                record_status = record_check(line)
                if not record_status:
                    raise Exception('bad record found at line {0} in file {1}'.format(count, item))
                count += 1

    return _gen_records(filelist)
