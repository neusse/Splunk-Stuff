#!/usr/bin python


# this is a quick program to read a list of searches from a csv file and disable them.
# here is the SPL to create the list. just export it from splunk.
# This is a Qick and dirty way to not have to run the query from python.  Less code since this is a one shot thing.

# change the "search orphan=1 disabled=0 is_scheduled=1 " as needed.

# | rest timeout=600 splunk_server=local /servicesNS/-/-/saved/searches add_orphan_field=yes count=0 
# | search orphan=1 disabled=0 is_scheduled=1 
# | eval status = if(disabled = 0, "enabled", "disabled") 
# | fields title eai:acl.owner eai:acl.app eai:acl.sharing orphan status is_scheduled cron_schedule next_scheduled_time next_scheduled_time actions 
# | rename title AS "search name" eai:acl.owner AS owner eai:acl.app AS app eai:acl.sharing AS sharing


### These are not used, but hope to someday
# import sys
# import os
# import time
# import argparse
# import subprocess
# from distutils.version import StrictVersion
# import distutils.util

import requests
import csv
import urllib.parse

import urllib3
# surpress self signed certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


TARGETHOST = "neusse.com"
CSVFILE = "unshed.csv"


# need to convert over to use tokens in the header.
USERNAME="george"
PASSWORD="password"

def disable_search( myapp, mysearch, myowner ):
    ''' Do the actual disable with a REST call '''

    disable_uri = f"https://{TARGETHOST}:8089/servicesNS/nobody/{myapp}/saved/searches/{mysearch}/disable?"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    ret = requests.post( disable_uri, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
    if ret.status_code != 200:
        print(ret.content)
        raise ValueError(f"Unable to disable app - {myapp}  search - {mysearch}     {ret.status_code}")
    else:
        print(f" DISABLED ==> app({myapp}) search({mysearch})")
        #print(ret.content)


def change_owner( myapp, mysearch, myowner ):
    ''' Do the actual disable with a REST call '''
    ''' This function does not work riught now  Need to fix it to work'''

    disable_uri = f"https://{TARGETHOST}:8089/servicesNS/nobody/{myapp}/saved/searches/{mysearch}/owner?"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = f"owner = {myowner}"
    ret = requests.post( disable_uri, headers=headers, data=data, auth=(USERNAME, PASSWORD), verify=False)
    if ret.status_code != 200:
        print(ret.content)
        raise ValueError(f"Unable to disable app - {myapp}  search - {mysearch}     {ret.status_code}")
    else:
        print(f" DISABLED ==> app({myapp}) search({mysearch})")
        #print(ret.content)





def main():
    ''' read orphan csv and disable the search'''

    with open(CSVFILE) as orph:
        csv_reader = csv.DictReader(orph, delimiter=',')
        count = 0
        for row in csv_reader:
            print(f"{row['search name']} - {row['owner']} - {row['app']} - {row['is_scheduled']}")

            # Url encode so things work
            app = urllib.parse.quote(row['app'])
            search_name = urllib.parse.quote(row['search name'])

            disable_search( app, search_name, row['owner'] )

            count += 1

        print(f"Disabled {count} searches!")



if __name__ == "__main__":
    main()

