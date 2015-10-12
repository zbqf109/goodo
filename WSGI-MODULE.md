# WSGI
WSGI is a Python standard specification which is defined in [PEP-3333](https://www.python.org/dev/peps/pep-3333) for connecting servers and application during web development. Its initial goal is to let users choose a web framework without disturbing who stands at side of a web server. Althrough odoo is something WSGI compitable, there is hardly a choice how it is hosted, and therefore you may not take advantages of the provided features of an HTTP server (or proxy).

# Werkzeug
Odoo depends heavily on a python WSGI module \-\- `werkzeug`. At its homepage it says:

> Werkzeug is a WSGI utility library for Python. It is widely used and BSD licensed.

At the first glance it feels good but odoo plays too much on it.

## Website and static resources
Odoo tries to hold everything in its hand. There may be many considerations such as being aware of `QWeb` framework and ORM objects, but absolutely this feature slows down accessing the static resources like style sheets, scripts and images. And, since the handler of a path is located at runtime and what is even more worse is that it is neither cached nor optimized and you may waste a little more time when getting or posting something *every time*. When you type a decorator `@http.route` on a method, you actually know exactly how this path is handled, but odoo still bothers to look it up through a rule map. The `@http.route` gives a much simple way to make a path handler while gives up execution efficiency.

Another consideration may be that some requests are bound to a database while others are not. You cannot dispatch a request whose handler needs a database context before the database connections are set up. Odoo remedies this situation by a introducing a variable called `server_wide_modules` which is a Python `list` technically. It consists of a series of modules, each should include some kinds of classes or methods decorated by `@http.route`. Odoo will dispatch requests to these modules only if no database is connected and to other modules if any database connection already exists.   

So `goodo` should work out a better way to handle `@http.route` rules.

## Goodo's improvements

Restrictions are that you must make odoo the root directory of your website. Goodo makes a slightly revamp so that:

* it can be deployed under any sub-directories, and
* you can deploy odoo behind any WSGI-compatible services to take advantage of their features.

## Ways go there

Goodo adds a new configuration named `subroot` under which the original `odoo` is kept, but there is no extra effort taken by developers. For example, you still write `@http.route('/path/to/your/addon')` exactly the same as ever before, and the actual `route` function in `http` module is adjusted so that it can build a correct url pattern by add a prefix to it.

For the frontend, a new member `subroot` which is auto-detected through `location` is added to `odoo` object. Before a `json`/`xml`/`url` request is sent, the url is rebuilt with a prefix of `odoo.subroot` so that it refers the correct resource.
  
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

## Known issues

* Background images missing.

    In some `css` files, there are rules like `background:url('/web/blabla')`. Since the request for that resource of `url` specified is launched by the browser and there seems no way to hook these requests, some images need by an HTML element may be lost (you get a *404 Not Found* response for that requests each).

* Static templates
   
    Besides `QWeb`, `odoo` utilizes `jinja` template system. In such template files, for example *openerp/addons/web/views/database_manager.html*, links are not relative to `subroot`. 