# WSGI
WSGI is a Python standard specification for connection servers and application during web develepment. Its initial goal is to let users choose a web framework without disturbing who stands at side of a web server. Althrough odoo is something WSGI compitable, there is hardly a choice how it is hosted, and therefore you may not take advantages of the provided features of an HTTP server (or proxy).

# Werkzeug
Odoo depends heavily on a python WSGI module \-\- `werkzeug`. At its homepage it says:

> Werkzeug is a WSGI utility library for Python. It is widely used and BSD licensed.

At the first glance it feels good but odoo plays too much on it.

## Website and static resources
Odoo tries to hold everything in its hand. There may be many considerations such as being aware of `QWeb` framework and ORM objects, but absolutely this feature slows down accessing the static resources like style sheets, scripts and images. And, since the handler of a path is located at runtime and what is even more serious it is neither cached nor optimized you may waste a little time getting or posting something *every time*. When you type a decorator `@http.route` on a method, you actually know exactly how this path is handled, but odoo still bothers to look it up through a rule map. The `@http.route` gives a much simple way to make a path handler while gives up execution efficiency.

So `goodo` should work out a better way to handle `@http.route` rules and will end up for temporary.
