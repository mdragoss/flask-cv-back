import json
import logging
import os
from functools import lru_cache

import click
from flask import g
from flask.cli import with_appcontext
from pymongo import MongoClient
from pymongo.errors import (
    ConfigurationError,
    ConnectionFailure,
    ServerSelectionTimeoutError,
)

from config import config

app_logger = logging.getLogger('db')


def get_client():
    if 'client' not in g:
        try:
            g.client = MongoClient(
                f'mongodb://{config.MONGO_INITDB_ROOT_USERNAME}:{config.MONGO_INITDB_ROOT_PASSWORD}@{config.MONGO_URL}',
                connectTimeoutMS=3,
            )
            g.client.admin.command('ping')
            return g.client
        except (
            ConfigurationError,
            ConnectionFailure,
            ServerSelectionTimeoutError,
        ) as error:
            app_logger.exception(error)
            g.initial_data = init_data()
            return g.initial_data


def close_mongo(e=None):
    client = g.pop('client', None)
    if client is not None:
        client.close()


def init_mongo():
    client = get_client()
    if not isinstance(client, MongoClient):
        return None

    db = client['portfolio']
    collections = db.list_collection_names()
    if collections:
        if (
            len(
                set(collections).intersection(
                    {
                        'personal',
                        'skills_and_hobbies',
                        'experiences',
                        'educations',
                    }
                )
            )
            == 4
        ):
            print('All collections are ready.')
            return
    initial_data = init_data()
    personal = initial_data.get('personal')
    if personal:
        personal_id = db.personal.insert_one(personal).inserted_id
        app_logger.info(personal_id)

    skills_and_hobbies = initial_data.get('skills_and_hobbies')
    if skills_and_hobbies:
        skill_id = db.skills_and_hobbies.insert_one(
            {'qualities': 'skills', 'values': skills_and_hobbies['skills']}
        ).inserted_id
        app_logger.info(skill_id)
        hobby_id = db.skills_and_hobbies.insert_one(
            {'qualities': 'hobbies', 'values': skills_and_hobbies['hobbies']}
        ).inserted_id
        app_logger.info(hobby_id)

    experiences = initial_data.get('experiences')
    if experiences:
        db.experiences.insert_many(experiences, ordered=False)
    educations = initial_data.get('educations')
    if educations:
        db.educations.insert_many(educations, ordered=False)


@lru_cache(maxsize=None)
def init_data():
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    FIXTURES = os.path.join(APP_DIR, 'fixtures')
    initial_data = {}
    if os.path.exists(os.path.join(FIXTURES, 'skills_and_hobbies.json')):
        with open(os.path.join(FIXTURES, 'skills_and_hobbies.json')) as f:
            skills_and_hobbies = json.load(f)
            initial_data['skills_and_hobbies'] = skills_and_hobbies

    if os.path.exists(os.path.join(FIXTURES, 'personal.json')):
        with open(os.path.join(FIXTURES, 'personal.json')) as f:
            personal = json.load(f)
            initial_data['personal'] = personal

    if os.path.exists(os.path.join(FIXTURES, 'experience.json')):
        with open(os.path.join(FIXTURES, 'experience.json')) as f:
            experiences = json.load(f)
            initial_data['experiences'] = experiences

    if os.path.exists(os.path.join(FIXTURES, 'education.json')):
        with open(os.path.join(FIXTURES, 'education.json')) as f:
            educations = json.load(f)
            initial_data['educations'] = educations

    return initial_data


@click.command('init-mongo-db')
@with_appcontext
def init_mongo_command():
    init_mongo()
