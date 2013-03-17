#!/usr/bin/env python
"""
A test set of classes, to experiment and learn how to use AppEngine.
"""

import webapp2
import jsonrequest
import upload_to_db


class MainPage(jsonrequest.RequestHandler):
    def process(self):
        return ["Hello, natureskin!"]


routing = [
    ('/', MainPage),
    ('/add', upload_to_db.ShapeUploader)
]
app = webapp2.WSGIApplication(routing, debug=True)
