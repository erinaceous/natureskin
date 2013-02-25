#!/usr/bin/env python
"""
A test set of classes, to experiment and learn how to use AppEngine.
"""

import webapp2
import upload_shapefile


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, natureskin!')


routing = [
    ('/', MainPage),
    ('/layer/new', upload_shapefile.CreateLayer)
]
app = webapp2.WSGIApplication(routing, debug=True)
