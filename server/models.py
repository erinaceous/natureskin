"""
The classes in this file are models for the datastore.
"""
from google.appengine.ext import db


class Layer(db.Model):
    """Metadata for a layer."""
    name = db.StringProperty()
    #description = db.TextProperty()
    #author = db.StringProperty()
    #organization = db.StringProperty()
    #phone = db.PhoneNumberProperty()
    #email = db.EmailProperty()
    #website = db.LinkProperty()
    #address = db.PostalAddressProperty()
    uploaded_by = db.UserProperty()
    uploaded_at = db.DateTimeProperty(auto_now_add=True)


class Polygon(db.Model):
    """This model represents a single item of a layer - one polygon on
       the map."""
    dataset = db.StringProperty()
    bounds_nw = db.GeoPtProperty()
    bounds_se = db.GeoPtProperty()
    polygon = db.ListProperty(db.GeoPt)
    layer = db.ReferenceProperty(reference_class=Layer)
    name = db.StringProperty()
    description = db.TextProperty()
    phone = db.PhoneNumberProperty()
    email = db.EmailProperty()
    website = db.LinkProperty()
    address = db.PostalAddressProperty()
    owner = db.UserProperty()


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
