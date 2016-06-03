# json-log
JSON-log: Console Utility for reading being written log-file, its data filtering and output formatting. <br />

To run as a console-utility before usage, first of all, execute in the current dir:
```
bash@PC ~ $ sudo cp json-log.py /usr/bin/json-log
bash@PC ~ $ sudo chmod 0755 /usr/bin/json-log
```

**JSON-format being used for Console Utility:**<br />
**_Input_**:<br />
```
{"@fields": 
{ 
 "uuid": "00n0n0nn-n00n-0n00-nn00-0000n00n000n", 
 "level": "INFO", "status_code": 200, "content_type": "application/json", 
 "path": "/v1/items/1/", "method": "PUT", "name": "django.http" 
}, 
 "@timestamp": "2015-05-30T09:45:45+00:00", "@source_host": "c00000000000", 
 "@message": "Request processed"}
 ```

**_Output_**:<br />
[@timestamp] @fields.level @message<br />
OR:<br />
< template-format ><br />

<br />
**_Usage_**:<br />
```
bash@PC ~ $ tail -f /var/log/service.log | json-log --format template.j2 --filter @fields.level=ERROR
bash@PC ~ $ json-log /var/log/service.log --format template.j2 --filter @fields.level=ERROR
```
<br />
You can use following template-formats: <br />
-- Jinja2 (e.g. template.j2); <br />
-- Mustache (e.g. template.mustache).<br /><br />

**Tip.** 
While using template-formatting, it is highly recommended to run utility as following to get more readable view as a table:
```
bash@PC ~ $ tail -f /var/log/service.log | json-log --format templates/tablebody.j2 --filter @fields.level=ERROR > templates/tablebody_result.html
```
And then just open 'templates/index.html' in Your web-browser. Enjoy the user-friendly table view! :)
