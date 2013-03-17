"""
The classes in this file are models for the datastore.
"""
from google.appengine.ext import db


class Layer(db.Expando):
    """Metadata for a layer."""
    name = db.StringProperty()
    uploaded_by = db.UserProperty()
    uploaded_at = db.DateTimeProperty(auto_now_add=True)


class Polygon(db.Expando):
    """This model represents a single item of a layer - one polygon on
       the map."""
    center = db.GeoPtProperty()
    point = db.GeoPtProperty()
    name = db.StringProperty()


class Post(db.Model):
    """A 'post' is a photo or text post that may or may not be
       associated with a polygon and/or layer."""
    polygon = db.ReferenceProperty(reference_class=Polygon)
    layer = db.ReferenceProperty(reference_class=Layer)
    coordinates = db.GeoPtProperty()
    heading = db.FloatProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    photo = db.LinkProperty()
    url = db.LinkProperty()
    owner = db.UserProperty()
    tags = db.ListProperty(db.Category)


class Comment(db.Model):
    """A comment can be associated with a layer, a polygon or an entity"""
    association = db.ReferenceProperty()
    owner = db.UserProperty()
    content = db.TextProperty()
    rating = db.RatingProperty()
    created = db.DateTimeProperty(auto_now_add=True)
