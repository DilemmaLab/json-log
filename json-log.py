#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Github: https://github.com/HubLemma
# Web-site: http://lemma.ml

# To run as a console-utility before execute in the current dir:
# bash@PC ~ $ sudo cp json-log.py /usr/bin/json-log
# bash@PC ~ $ sudo chmod 0755 /usr/bin/json-log
#
# JSON to Console Utility
# Input:
# {"@fields":
# {
#  "uuid": "00n0n0nn-n00n-0n00-nn00-0000n00n000n",
#  "level": "INFO", "status_code": 200, "content_type": "application/json",
#  "path": "/v1/items/1/", "method": "PUT", "name": "django.http"
# },
#  "@timestamp": "2015-05-30T09:45:45+00:00", "@source_host": "c00000000000",
#  "@message": "Request processed"}
#
# Output:
# [@timestamp] @fields.level @message
# OR:
# <template-format>
#
# Usage:
# bash@PC ~ $ tail -f /var/log/service.log | json-log --format template.j2 --filter @fields.level=ERROR
# bash@PC ~ $ json-log /var/log/service.log --format template.j2 --filter @fields.level=ERROR

# Available template-formats:
# -- Jinja2 (e.g. template.j2);
# -- Mustache (e.g. template.mustache).

# To get user-friendly view for template-formatting, it is highly recommended to run utility as following:
# bash@PC ~ $ tail -f /var/log/service.log | json-log --format templates/tablebody.j2 --filter @fields.level=ERROR > templates/tablebody_result.html
# And then just open 'templates/index.html' in Your web-browser. Enjoy the user-friendly table view! :)

import argparse
import re
import sys
import json
import os.path

import pystache
from jinja2 import Environment, FileSystemLoader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='JSON-log Console Utility. Please, enter'
                                                 ' formatting (\'-o\', \'--format\') and'
                                                 ' filtering (\'-i\', \'--filter\') arguments.')
    parser.add_argument('filename', default=None, nargs='?', metavar="FILE",
                        help='Name of input file') # Filename to get as argument
    parser.add_argument('-o', '--format', default=None, help='Output format, available as:\n'
                                                                    ' default - string;\n '
                                                                    ' template - mustache;\n'
                                                                    ' template - jinja2\n') # format
    parser.add_argument('-i', '--filter', default='@fields.=', help='Field of log to be filtered by \n'
                                                                         'in format @fields.fieldname=fieldvalue') # filter
    args = parser.parse_args()

    if not re.match(r'^@[\w]*\.[\w]*=[\w\d\-\s\"\']*$', args.filter):
        print "Unsupported Filter Format.\n" \
              "Right format examples:\n" \
              "@fields.level=ERROR\n" \
              "@fields.status_code=200\n" \
              "@fields.method=PUT\n" \
              "Program is being proceeded without filter..."
        args.filter = '@fields.='
    filter_dict = re.split('\.|=', args.filter)

    if args.format:
        # Поддержка шаблонизаторов (проверка расширения файла)
        # ** Есть вариант, что расширение поддерживается, но внутри файла - данные не верного формата.
        # ** В рамках данной реализации вариант такой ошибки не рассматривается и не обрабатывается.
        templ = args.format.split('.')[-1]
        if templ not in ('j2', 'mustache'):
            print "Unsupported Template Type.\n" \
                  "Only Jinja2 (file extension \".j2\") " \
                  "\nand Mustache (file extension \".mustache\") are supported." \
                  "\nProgram is being proceeded with default template (\"[@timestamp] @fields.level @message\")..."
            args.format = None
        # Проверка существования файла с шаблоном
        elif not os.path.isfile(args.format):
            print "No Template File Found.\n" \
                  "\nProgram is being proceeded with default template (\"[@timestamp] @fields.level @message\")..."
            args.format = None
    # ** Чтобы можно было читать из файла,
    # ** указав его в командной строке: $ json-log service.log
    input_stream = sys.stdin
    if args.filename:
        input_stream = open(args.filename, 'r')
    output = sys.stdout

    for line in input_stream:
        try:
            fields = json.loads(line).get(filter_dict[0], {})
            field = fields.get(filter_dict[1], None)
            timestamp = json.loads(line).get('@timestamp')
            message = json.loads(line).get('@message')
        except ValueError as e:
            # ** Если не осуществлять данную проверку, то можно есть риск получить ошибку невалидной строки для файла,
            # ** который обновляется в режиме реального времени.
            # ** Такая проверка введена намеренно
            # ** вместо проверки на то,
            # ** что файл открыт другим процессом в режиме "write",
            # ** т.е. вместо вызова bash-утилиты lsof на args.filename ферез subprocess
            # ** или вместо вызова собственного python-скрипта проверки.
            # ** Кроме того, есть вариант реализовать отдельную процедуру
            # ** для чтение из "being written"-файла.
            print "\nInput Data Error. " \
                  "Probably, input file is oppened for writting " \
                  "by another process.\n" \
                  "In this case it's better to use command through pipe " \
                  "as follows:\n" \
                  "$ tail -f filename.log | json-log \n" \
                  "\nProgramm is going to be closed...\n"
            input_stream.close()
            exit(1) # Exit with an Error

        if not field or str(field) == str(filter_dict[2]):
            if not args.format:
                if field:
                    output.write("[%s]\t%s\t%s\n" % (timestamp, json.dumps(field), str(message)))  # [@timestamp] @fields.level @message
                else:
                    output.write("[%s]\t%s\t%s\n" % (timestamp, json.dumps(fields), str(message)))  # [@timestamp] @fields.all_fields @message
            else:
                # Поддержка шаблонизаторов
                if templ == 'j2':
                    template_dir = os.path.dirname(os.path.abspath(args.format))
                    env_jinja = Environment(loader=FileSystemLoader(template_dir))
                    # Default: trim_blocks==False
                    output.write("%s" % env_jinja.get_template(args.format.split('/')[-1]).render({'timestamp': timestamp,
                                                                                                   'fields': fields,
                                                                                                   'message': message,
                                                                                                   str(filter_dict[1])+'bool': True
                                                                                                  })) # Jinja2
                elif templ == 'mustache':
                    output.write("%s" % pystache.render(open(args.format).read(), {'timestamp': timestamp,
                                                                                   'fields': fields,
                                                                                   'message': message,
                                                                                   str(filter_dict[1])+'bool': True
                                                                                   }))  # Mustache
    if args.filename:
         input_stream.close()

    exit(0) # Clean exit - No Errors
