import argparse
import sys
from urllib.parse import urlparse

def normalize_url(url):
    """
    Normalize a given URL.
    """
    url = urlparse(url)
    params = set()
    for param in url.query.split('&'):
        params.add(param.split('=')[0])
    return url.scheme + url.netloc + url.path + ''.join(params)

def weaponize_url(url, payload, identifier):
    """
    Weaponize a given URL.
    """
    url = urlparse(url)
    param_string = "?"
    for param in url.query.split('&'):
        identifier += 1
        temp_payload = payload.replace("<id>", "{}{}".format(args.prefix, identifier))
        param_string += param.split("=")[0] + "=" + temp_payload + "&"
    return [url.scheme + "://" + url.netloc + url.path + param_string[:-1], identifier]

def weaponize_url_preserve(url, payload, identifier):
    """
    Weaponize a given URL, preserving original parameter values. 
    """
    url = urlparse(url)
    weaponized_urls = []
    for param in url.query.split('&'):
        identifier += 1
        temp_payload = payload.replace("<id>", "{}{}".format(args.prefix, identifier))
        weaponized_urls.append(url.scheme + "://" + url.netloc + url.path + "?" + url.query.replace(param, param.split("=")[0] + "=" + temp_payload))
    return [weaponized_urls, identifier]

if __name__ == "__main__":
    # setup argparse
    parser = argparse.ArgumentParser(description="Populates payloads with unique identifiers into URL GET parameters.")
    parser.add_argument("-p", "--payload", help="Original payload to manipulate, place <id> in the position you wish to be replaced, it will be replaced with 1 -> n", required=True)
    parser.add_argument("-pr", "--prefix", help="Prefix for the payload identifier, e.g. pay<id> will result in pay1 -> pay99999", default="p")
    parser.add_argument("-o", "--output", help="Output file to write to", default=None)
    parser.add_argument("--preserve", help="Preseve other URL values, limiting to one payload per URL, keeping all other values the same as entered", default=False, action="store_true")
    parser.add_argument("-s", "--silent", help="Do not print to stdout", default=False, action="store_true")
    args = parser.parse_args()
    # initiate vars
    identifier = 0
    normalized_paths = set()
    weaponized_urls = set()
    if not sys.stdin.isatty():
        for line in sys.stdin:
            line = line.strip()
            normalized_url = normalize_url(line)
            if normalized_url in normalized_paths:
                continue
            else:
                if "?" not in line:
                    # lame request with no params, moving on
                    continue
                normalized_paths.add(normalized_url)
                if args.preserve:
                    result = weaponize_url_preserve(line, args.payload, identifier)
                    for url in result[0]:
                        weaponized_urls.add(url)
                        if not args.silent:
                            print(url)
                else:
                    result = weaponize_url(line, args.payload, identifier)
                    weaponized_urls.add(result[0])
                    if not args.silent:
                        print(result[0])
                identifier = result[1]

        if args.output:
            with open(args.output, 'w') as f:
                for url in weaponized_urls:
                    f.write(url + "\n")
