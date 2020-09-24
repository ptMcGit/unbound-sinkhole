default_destination_dir = './'
import pathlib
import requests
import urllib
import tempfile

record_template = 'local-zone "{0}" refuse'


def fix_url(site_url):
    url = urllib.parse.urlparse(site_url)
    if url.path == "":
        raise Exception("path is not present")

#    return urllib.parse.urlparse('https' + url.netloc + url.path)
    return 'https://' + url.netloc + url.path

def site_url_as_file(site_url):
    return Wj

def create_sinklist(site_url, white_list=None, destination=None):
    response = get_data(site_url)

    if destination is None:
        parsed_url = urllib.parse.urlparse(r.url)
        destination = parsed_url.netloc + "-" + parsed_url.split('/')[-1] + ".sinklist"

    if white_list is None:
        white_list = []

    with open(destination, "w") as f:
        for entry in iter(get_entries(response)):
            # I think we just need the URL, not the IP
            # '.' makes it an fqdn
            ip, domain = entry.decode('utf-8').split(' ')
            if domain not in white_list:
                f.write(record_template.format(domain + '.'))

    return destination


def get_entries(url_response):
    for line in url_response.iter_lines():
        # drop comments
        if not re.match('^\s*#.*', line):
            yield line


def get_data(site_url, destination=None):
    """ Expects a string URL w/o protocol.

    """
    import requests
    r = requests.get(fix_url(site_url))
    # if response != 200 throw an error
    # d.raise_for_status()
    return r


def register_list(sinkhole_file, server_config):
    tempf = tempfile.mkstemp()
    with open(tempf, 'w' ) as t and open(server_config, 'r') as f:
        for line in f:
            if re.match('^\s*server:\s+', line):
                parse_server_clause(t, f)
                break

def parse_server_clause(t, f):
    for line in f:
        if re.match('^\s*(views|
