"""
    THIS ISN'T FUNCTIONAL!
    ----------------------
    Shapefiles from the Natural England datasets need to be, in order to
    be used in Google Maps, reprojected from British National Grid to
    WGS84 lat/lon coordinates.
    The best (easiest, quickest) way I can think of doing this is to
    use pyshp and pyproj to decode a shapefile and reproject the points.
    This is computationally expensive so I don't want to waste all my
    free AppEngine compute resources on it (plus pyproj won't work on
    GAE on account of being a CPython extension).
    Processing of shapefiles will be done on a seperate ChunkHost
    instance which has the ability to run 'vanilla' Python.
    Because of this, the shapefile-parsing functionality is being moved
    out of the AppEngine project and into its own tools/ script,
    shapefile_to_geojson.py -- which spits out GeoJSON files, which this
    module WILL be able to handle + add to the database with the 
    `FromGeoJSON` class.
"""

import jsonrequest

from google.appengine.ext import db
from google.appengine.api import users
from models import Layer, Polygon


class CreateLayer(jsonrequest.RequestHandler):
    """Creates a layer (if it doesn't already exist)."""
    def process(self):
        layer = Layer.get_by_key_name(self.request.get('code'))
        if layer is not None:
            response = {
                "error": "Layer with this code already exists.",
                "entity": db.to_dict(layer)
            }
            response['entity']['uploaded_at'] =\
                str(response['entity']['uploaded_at'])
            return response
        layer = Layer(key_name=self.request.get('code'))
        layer.name = self.request.get('name')
        layer.description = self.request.get('description')
        layer.author = self.request.get('author')
        layer.organization = self.request.get('organization')
        layer.phone = self.request.get('phone')
        layer.email = self.request.get('email')
        layer.website = self.request.get('website')
        layer.address = self.request.get('address')
        layer.uploaded_by = users.get_current_user()
        key = layer.put()
        self.response.headers['Content-Type'] = 'application/json'
        response = {"id": key.id_or_name()}
        return response


class FromShapeFile(jsonrequest.RequestHandler):
    """"""
