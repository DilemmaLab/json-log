#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Script imitates log-writing of JSON-formatted string to file 'logfile'
# File 'logfile' is being written continuously

# {"@fields":
# {
#  "uuid": "00n0n0nn-n00n-0n00-nn00-0000n00n000n",
#  "level": "INFO", "status_code": 200, "content_type": "application/json",
#  "path": "/v1/items/1/", "method": "PUT", "name": "django.http"
# },
#  "@timestamp": "2015-05-30T09:45:45+00:00", "@source_host": "c00000000000",
#  "@message": "Request processed"}

import sys
import datetime
import time # time.sleep()
from random import randint
from uuid import uuid4

def randomizer():
    level = ["INFO", "ERROR", "SUCCESS", "NONE"]
    # level = ["ERROR", "ERROR", "ERROR", "ERROR"]
    # Supportable Status codes:
    #               [200,201,202,203,204,205,
    #                300,301,302,303,304,305,
    #                400,401,402,403,404,405,
    #                500,501,502,503,504,505]
    status_code = [200, 300, 400, 500]
    uuid_default = "00n0n0nn-n00n-0n00-nn00-0000n00n000n"
    uuid = [uuid4(), uuid_default][randint(0,1)] # To have at least several uuids with the same number ('uuid_default') in the file
    method = ['PUT', 'GET', 'POST', 'DELETE']
    # timestamp = datetime.datetime.now().isoformat()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    message = ["Request declined", "Request succeed", "Request failed", "No request"]
    # Let's Randomize it! :)
    rand_item = randint(0, 3)
    # sys.stdout.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (uuid, level[randint(0, 3)],
    #         status_code[randint(0, 3)]+(rand_item+rand_item%3), method[randint(0, 3)],
    #         timestamp, message[randint(0, 3)])) # TEST
    return (uuid, level[randint(0, 3)],
            status_code[randint(0, 3)]+(rand_item+rand_item%3), method[randint(0, 3)],
            timestamp, randint(10000000000, 60000000000), message[randint(0, 3)])
    # End of randomizer()

if __name__ == "__main__":
    log_file = open('service.log', 'w+')

    while(1):
        log_file.write('{"@fields": '
                       '{"uuid": "%s", '
                       '"level": "%s", '
                       '"status_code": %d, '
                       '"content_type": "application/json", '
                       '"path": "/v1/items/1/", '
                       '"method": "%s", '
                       '"name": "django.http"}, '
                       '"@timestamp": "%s", '
                       '"@source_host": "c%s", '
                       '"@message": "%s"}\n' % randomizer())
        time.sleep(randint(1, 49)/10.) # Imitates random delay (Why? Just for lulz)
    log_file.close()
