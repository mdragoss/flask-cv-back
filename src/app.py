import os

from flask import Flask
from pymongo import MongoClient

from db import get_client, init_mongo_command
from views.experience_and_studies import Education, Experience
from views.personal import Personal
from views.skills_and_hobby import SkillAndHobby

app = Flask(__name__)
app.config['DEBUG'] = os.getenv('DEBUG', False)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '')


with app.app_context():
    client = get_client()
    is_mongo = False
    if isinstance(client, dict):
        is_mongo = False

    if isinstance(client, MongoClient):
        is_mongo = True

app.cli.add_command(init_mongo_command)


@app.route('/')
def status():
    return {'status': 'ok'}


app.add_url_rule(
    '/personal',
    view_func=Personal.as_view('personal', client=client, is_mongo=is_mongo),
)
app.add_url_rule(
    '/skills',
    view_func=SkillAndHobby.as_view(
        'skills',
        client=client,
        collection='skills',
        is_mongo=is_mongo,
    ),
)
app.add_url_rule(
    '/hobbies',
    view_func=SkillAndHobby.as_view(
        'hobbies',
        client=client,
        collection='hobbies',
        is_mongo=is_mongo,
    ),
)

app.add_url_rule(
    '/experience',
    view_func=Experience.as_view(
        'experience', client=client, is_mongo=is_mongo
    ),
)

app.add_url_rule(
    '/education',
    view_func=Education.as_view('education', client=client, is_mongo=is_mongo),
)


if __name__ == "__main__":
    app.run(port=8000, load_dotenv=False)
