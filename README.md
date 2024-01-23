# Please write a Python Flask application that presents your CV data (limited in time 6 - 8hours):
1. As a JSON REST API with endpoints GET /personal, GET /experience, GET /education, ...
2. As a Flask CLI command that prints the data to the console

> The CV data can be hard-coded in the code or read from disk. You do not need to integrate with any database. Please include a README file on how to start the REST API and how to execute the CLI command.

## 1. Create virtual env and install pipenv
```sh
python3 -m venv venv

# activate virtual env

source venv/bin/activate
```

Then install pipenv
```sh
pip3 install pipenv
```

## 2. Copy .env.example into .env
```sh
copy .env.example .env
```
> pipenv will load and export .env file's data

## 3. Install project dependencies
```sh
# pipenv should install from pipfile.lock
pipenv install
```

## 4. Run project
### 4.1 Pipenv run without mongo
Will start project load data from fixtures
```sh
pipenv run start
```

### 4.2 Pipenv run with mongo
1. First create mongo container
```sh
docker run --name mongodb -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=pass mongodb/mongodb-community-server:latest
```

2. Export data from fixtures to mongo
```sh
pipenv run mongo_init
```

3. Run app
```sh
pipenv run start
```

### 4.3 Run all in containers
```sh
cd deployment && sh start-local.sh
```

To run cli is possible in the following way
- To listing a all commands can run
```sh
flask --app src/app commands
```

- To run one single command is possible in the following way
```sh
flask --app src/app commands experience
```


