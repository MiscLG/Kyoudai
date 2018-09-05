from google.appengine.ext import ndb
from google.appengine.ext import blobstore

class Photo(ndb.Model):
    user = ndb.StringProperty()
    category = ndb.StringProperty()
    name = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()
class Drawing(ndb.Model):
    category = ndb.StringProperty()
    media_type = ndb.StringProperty()
    name = ndb.StringProperty()
    blob_key = ndb.BlobKeyProperty()
    likes = ndb.IntegerProperty()
    comments = ndb.IntegerProperty()
    description = ndb.StringProperty()
    def addLike():
        likes+=1
    def addComment():
        comments+=1
    def addDescription(description):
        self.description = description
class User(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
class ArtComment(ndb.Model):
    user = ndb.StringProperty()
    connect_blob_key = ndb.BlobKeyProperty()
    
    
    
