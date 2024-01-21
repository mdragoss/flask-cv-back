from flask.typing import ResponseReturnValue
from flask.views import View


class Personal(View):
    init_every_request = False
    methods = ('GET',)

    def __init__(self, client, is_mongo) -> None:
        self.client = client
        self.is_mongo = is_mongo

    def dispatch_request(self) -> ResponseReturnValue:
        if not self.is_mongo:
            personal_data = self.client.get('personal', None)
            if not personal_data:
                return {'detail': 'no personal data found'}, 404

            return personal_data, 200

        db = self.client['portfolio']
        collection = db['personal']
        personal_data = collection.find_one()
        if personal_data is None:
            return {'detail': 'no data found'}, 404

        personal_data.pop('_id', None)
        return personal_data, 200
