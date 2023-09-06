from beanie.odm.operators.update.general import Set

from database.connections import init_database
from database.models import generator_model
from asyncio import gather


async def upsert_one_row(values, document):
    data_ = document(**values.to_dict())

    upsert_dict = data_.model_copy(deep=True)
    del upsert_dict.id
    del upsert_dict.revision_id
    del upsert_dict.DATETIME

    await document.find_one(document.DATETIME == data_.DATETIME).upsert(
        Set(upsert_dict),
        on_insert=data_
    )


async def upsert_data(data, document):
    """Insert or Update the document in the database."""
    tasks = [upsert_one_row(values, document) for _, values in data.iterrows()]
    await gather(*tasks)


async def process_database(data, configs, log):
    """Process the data and insert it into the database."""
    wind_model = generator_model(configs)
    await init_database(wind_model, configs, log)
    await upsert_data(data, wind_model)
