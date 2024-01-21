import json
import os
from pprint import pprint

from flask import Blueprint

commands_blueprint = Blueprint('commands', __name__)

APP_DIR = os.path.abspath(os.path.dirname(__file__))
FIXTURES = os.path.join(APP_DIR, 'fixtures')


@commands_blueprint.cli.command('personal-info')
def print_personal_info():
    """Print personal info from command line"""
    if os.path.exists(os.path.join(FIXTURES, 'personal.json')):
        with open(os.path.join(FIXTURES, 'personal.json')) as f:
            personal = json.load(f)
            pprint(personal)


@commands_blueprint.cli.command('skills')
def print_skills():
    """Print personal skills"""
    if os.path.exists(os.path.join(FIXTURES, 'skills_and_hobbies.json')):
        with open(os.path.join(FIXTURES, 'skills_and_hobbies.json')) as f:
            skills_and_hobbies = json.load(f)
            pprint(skills_and_hobbies['skills'])


@commands_blueprint.cli.command('hobbies')
def print_hobbies():
    """Print personal hobbies"""
    if os.path.exists(os.path.join(FIXTURES, 'skills_and_hobbies.json')):
        with open(os.path.join(FIXTURES, 'skills_and_hobbies.json')) as f:
            skills_and_hobbies = json.load(f)
            pprint(skills_and_hobbies['hobbies'])


@commands_blueprint.cli.command('experience')
def print_experience():
    if os.path.exists(os.path.join(FIXTURES, 'experience.json')):
        with open(os.path.join(FIXTURES, 'experience.json')) as f:
            experiences = json.load(f)
            pprint(experiences)


@commands_blueprint.cli.command('educations')
def print_educations():
    if os.path.exists(os.path.join(FIXTURES, 'education.json')):
        with open(os.path.join(FIXTURES, 'education.json')) as f:
            educations = json.load(f)
            pprint(educations)
