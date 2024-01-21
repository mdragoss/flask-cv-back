from flask.typing import ResponseReturnValue
from flask.views import View


class Experience(View):
    init_every_request = False
    methods = ('GET',)

    def __init__(self, client, is_mongo: bool) -> None:
        self.client = client
        self.is_mongo = is_mongo

    def dispatch_request(self) -> ResponseReturnValue:
        if not self.is_mongo:
            experiences = self.client.get('experiences', None)
            if not experiences:
                return {'detail': 'no experiences data found'}, 404
            return experiences, 200

        db = self.client['portfolio']
        collection = db['experiences']
        collection_data = list(collection.find({}))
        if not collection_data:
            return {'detail': 'no experiences data found'}, 404

        result = [
            {k: v for k, v in data.items() if k != '_id'}
            for data in collection_data
        ]
        return result, 200


class Education(View):
    init_every_request = False
    methods = ('GET',)

    def __init__(self, client, is_mongo: bool) -> None:
        self.client = client
        self.is_mongo = is_mongo

    def dispatch_request(self) -> ResponseReturnValue:
        if not self.is_mongo:
            educations = self.client.get('educations', None)
            if not educations:
                return {'detail': 'no educations data found'}, 404
            return educations, 200

        db = self.client['portfolio']
        collection = db['educations']
        collection_data = list(collection.find({}))
        if not collection_data:
            return {'detail': 'no educations data found'}, 404

        result = [
            {k: v for k, v in data.items() if k != '_id'}
            for data in list(collection_data)
        ]
        return result, 200
