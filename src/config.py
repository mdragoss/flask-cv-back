import os
from dataclasses import dataclass


@dataclass
class Config:
    MONGO_INITDB_ROOT_USERNAME: str = os.getenv(
        'MONGO_INITDB_ROOT_USERNAME', 'user'
    )
    MONGO_INITDB_ROOT_PASSWORD: str = os.getenv(
        'MONGO_INITDB_ROOT_PASSWORD', 'pass'
    )
    MONGO_URL: str = os.getenv(
        'MONGO_URL',
        'localhost:27017',
    )


config = Config()
