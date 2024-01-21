from flask.typing import ResponseReturnValue
from flask.views import View


class SkillAndHobby(View):
    init_every_request = False
    methods = ('GET',)

    def __init__(self, client, collection, is_mongo: bool) -> None:
        self.client = client
        self.collection = collection
        self.is_mongo = is_mongo

    def dispatch_request(self) -> ResponseReturnValue:
        if not self.is_mongo:
            data = self.client.get('skills_and_hobbies', None)
            if not data and data.get(self.collection, []):
                return {'detail': f'no {self.collection} data found'}, 404

            return {self.collection: data.get(self.collection)}, 200

        db = self.client['portfolio']
        collection = db['skills_and_hobbies']
        collection_data = collection.find_one({'qualities': self.collection})
        if collection_data is None:
            return {'detail': f'no {self.collection} data found'}, 404

        collection_data.pop('_id', None)
        print(collection_data)
        return collection_data.get('values'), 200
