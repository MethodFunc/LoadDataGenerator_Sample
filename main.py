import asyncio
import time

from bin.data_module import random_dataset
from bin.gen_process import create_dataframe, generate_data, transform_data
from bin.utils import load_model, load_scale
from configs import Settings, load_logger
from database.CRUD import process_database


async def main(args, log):
    # load scale & model
    log.info("Scale and Model loading")
    scale = load_scale(args.SCALE_PATH, log)
    model = load_model(args.MODEL_PATH, log)

    random_series = random_dataset(args.WINDOW_SIZE, args.SEQ_LEN, args.BATCH_SIZE)

    log.info("Generated data...")
    generated_data = generate_data(random_series, model, args)
    log.info("Inverse scale data...")
    transformed_data = transform_data(generated_data, scale, args)
    log.info("Create dataframe...")
    dataframe = create_dataframe(transformed_data, args, log)

    # insert mongo database
    log.info("Insert Database")
    try:
        await process_database(dataframe, args, log)
    except Exception as e:
        log.critical("Database Insert Fail")
        log.debug(e)


if __name__ == "__main__":
    st = time.time()
    configs = Settings()
    logs = load_logger(configs.DATA_TYPE)
    logs.info("="*20)
    logs.info("DataGenerator Start")
    logs.info("=" * 20)

    assert configs.DATA_TYPE in [1, 2], "Invalid GEN_TYPE. Must be 1 or 2."

    if configs.DATA_TYPE == 1:
        configs.WINDOW_SIZE = 144
        configs.SEQ_LEN = 7
        configs.BATCH_SIZE = 128
        configs.COLUMNS = [f'col{i}' for i in range(1, 8)]

    elif configs.DATA_TYPE == 2:
        configs.WINDOW_SIZE = 144
        configs.SEQ_LEN = 6
        configs.BATCH_SIZE = 144
        configs.COLUMNS = [f'col{i}' for i in range(1, 7)]

    asyncio.run(main(configs, logs))

    logs.info(f"Done: {time.time() - st}")
