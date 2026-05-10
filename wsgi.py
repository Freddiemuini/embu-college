# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below assumes you're using Flask. If you are using a different web
# framework, look at the other examples in this directory.
#
# +++++++++++ FLASK +++++++++++
# Flask works like any other WSGI-compatible framework, we just need
# to import the application.  Often Flask apps are called "app" so we
# may need to rename it during the import:
#
from app import app as application  # noqa
#
# +++++++++++ GENERAL WSGI +++++++++++
# Alternatively, if your main Python file is called something
# else than app.py, you can rename the below to point to a different file:
#
# from your_main_file import app as application  # noqa
#
# +++++++++++ HELLO WORLD +++++++++++
# If you prefer a hello world test, comment out the above two lines and
# uncomment the below. It will override anything above.
#
# def application(environ, start_response):
#     if environ.get('PATH_INFO') == '/':
#         status = '200 OK'
#         content = 'Hello World!'
#     else:
#         status = '404 NOT FOUND'
#         content = 'Page not found.'
#     response_headers = [('Content-Type', 'text/html'), ('Content-Length', str(len(content)))]
#     start_response(status, response_headers)
#     yield content.encode('utf8')
#
# +++++++++++ DJANGO +++++++++++
# If you're using Django, comment out the above and uncomment the below.
# You'll also need to set up your Django settings file by going to the
# PythonAnywhere web tab and setting the DJANGO_SETTINGS_MODULE environment
# variable to the name of your settings file.
#
# import os
# import sys
#
# path = '/home/<your-username>/<your-project>'
# if path not in sys.path:
#     sys.path.append(path)
#
# os.environ['DJANGO_SETTINGS_MODULE'] = '<your-project>.settings'
#
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()