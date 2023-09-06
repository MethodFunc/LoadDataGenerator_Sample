import sys
from urllib.parse import quote_plus

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError


def create_mongo_uri(configs):
    if configs.DB_TEST:
        return configs.DB_URI
    return f"mongodb://{configs.DB_HOST}:{quote_plus(configs.DB_PWD)}@{configs.DB_HOST}/?authSource=admin"


async def ping_database(client, log):
    try:
        await client.admin.command('ping')
        log.info("Database Access!!")
    except ServerSelectionTimeoutError:
        log.critical("Failed to connect to the database. Timeout: 5.0s")
        sys.exit()


async def init_database(document, configs, log):
    """
    Initialize the MongoDB database connection.

    Parameters:
    - document: The document model for Beanie ORM.
    - configs: The configuration object containing database settings.
    """

    uri = create_mongo_uri(configs)

    client = AsyncIOMotorClient(
        uri, serverSelectionTimeoutMS=5000
    )

    await ping_database(client, log)

    await init_beanie(
        database=client[configs.DB_DATABASE],
        document_models=[document]
    )
