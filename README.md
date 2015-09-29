# goodo
A odoo fork to provide some new features.

## About odoo
odoo is a powerful and all\-in\-one software solution for ERP and CRM.

## About goodo
odoo's Problem is that it is *all\-in\-one*. Sometimes it is none of your business what has to be done, where to store data and files and how it is updated when changes are made. So goodo lets things to be more flexible and things do right things.

There are several steps following:

1. Remove dependencies on `werkzeug` so it can be deployed on any WSGI compatible server;
    * in progress

2. Postgresql should be optional and other databases are alternative;
    * to do

3. Porting to python 3.
    * to do

Any of the 3 steps is not easy to be done and will take a long time.

## Current progressing

goodo can now run on a WSGI server other than a Python HTTP Server with `werkzeug`.

### nginx with uwsgi

* In nginx's configure file:

        location /goodo {  
            uwsgi_pass 127.0.0.1:9000;  
            include uwsgi_params;  
        }

    **Note**: either the 9000 port or the `/goodo` sub-path can be changed to others you like.

* uwsgi:  
    uwsgi supports many means to configure it. Just leave the right port and make module to be `openerp.service.wsgi_server` like:

        module=openerp.service.wsgi_server

    **Note**: you may want to add odoo's path to uwsgi's `pythonpath`.

### apache with mod\_wsgi:

Make `PythonHandler` to be `openerp.service.wsgi_server`.

### odoo 

If you want to deploy odoo with a sub-path, you would add this line to its configuration file:

    subroot = /goodo

or in a command line:

    --subroot=/goodo  

## Wanted

It will be my great pleasure to work with you if you are interested in this project and happen to be:

* familiar with python
* good at painting

Please contact me at zbqf109@gmail.com


