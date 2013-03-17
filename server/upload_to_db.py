#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
# encoding: utf-8
"""
   Add a single area to the database.
   Author: Owain Jones [github.com/doomcat]
"""

import json
import models
import jsonrequest
from google.appengine.ext import db


class ShapeUploader(jsonrequest.RequestHandler):
    def process(self):
        try:
            data = json.loads(self.request.body)
            data.update(data['meta'])
            data['center'] = "%f,%f" % (data['center'][1], data['center'][0])
            data['point'] = "%f,%f" % (data['point'][1], data['point'][0])
            del data['meta']
            model = models.Polygon(**data)
            model.put()
            return data
        except ValueError:
            return {}
