from datetime import datetime

from beanie import Document, Indexed


def generator_model(configs):
    class BaseDocument(Document):
        DATETIME: Indexed(datetime)
        col1: float
        col2: float
        col3: float
        col4: float

        class Settings:
            name = configs.DB_COLLECTION

    class FirstDocumnet(BaseDocument):
        col5: float
        col6: float
        col7: float

    class SecondDocumnet(BaseDocument):
        col5: float
        col6: float

    if configs.DATA_TYPE == 1:
        return FirstDocumnet

    elif configs.DATA_TYPE == 2:
        return SecondDocumnet
