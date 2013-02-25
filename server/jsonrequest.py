import json
import webapp2


class RequestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(
            json.dumps(self.process())
        )

    def post(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(
            json.dumps(self.process())
        )

    def process(self):
        return {}
