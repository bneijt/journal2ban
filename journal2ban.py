#!/usr/bin/python3
import sys
import json
import http.client
import logging
import ipaddress
import re
import urllib.request
import urllib.error
from subprocess import call
from time import sleep

#logging.getLogger().setLevel(logging.INFO)

def evaluate(record):
    if not "MESSAGE" in record:
        logging.error("Record missing message key, skipping")
        return False
    msg = record["MESSAGE"]
    if "authentication failure" in msg:
        match = re.search(r"rhost=([0-9a-f.:]+)", msg) 
        if not match == None:
            try:
                address = ipaddress.ip_address(match.group(1))
                if isinstance(address, ipaddress.IPv4Address):
                    logging.info("Adding %s to blackfour", address.exploded)
                    call(["ipset", "-exist", "add", "blackfour", address.exploded])
                elif isinstance(address, ipaddress.IPv6Address):
                    logging.info("Adding %s to blacksix", address.exploded)
                    call(["ipset", "-exist", "add", "blacksix", address.exploded])
                else:
                    return False
            except ValueError:
                logging.error("Matched IP with invalid IP: '%s'" % msg)
        else:
            logging.error("Could not find rhost in '%s'" % msg)
    return True

def feedJsonFromInto(url, handler):
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    response = urllib.request.urlopen(req)
    while True:
        line = response.readline().decode("UTF-8")
        if line == "":
            break
        if not line.startswith("{"):
            logging.error("Probably not json, skipping record: '%s'", line)
            continue
        handler(json.loads(line))

def main():
    url = "http://localhost:19531/entries?follow&_SYSTEMD_UNIT=sshd.service"
    while True:
        logging.info("Connecting to %s" % url)
        try:
            feedJsonFromInto(url, evaluate)
        except urllib.error.URLError as ex:
            logging.error("Unable to connect to %s: %s" % (url, ex.reason))
        sleep(5)
    return 0


if __name__ == "__main__":
    sys.exit(main())

