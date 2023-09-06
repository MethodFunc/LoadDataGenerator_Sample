from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import tensorflow as tf

tf.keras.backend.set_floatx('float32')

SECONDS_IN_DAY = 86400
MINUTES_IN_DAY = 1440


def generate_data(dataset, model, args):
    # Generated data (batch x window x seq_len)
    generated_data = []

    timestamps = {
        "s": SECONDS_IN_DAY,
        "t": MINUTES_IN_DAY

    }

    freq_times = timestamps[args.FREQ.lower()]
    calc_range = int(round(freq_times / (args.WINDOW_SIZE * args.BATCH_SIZE), 0))
    g_range = 1 if calc_range == 0 else calc_range

    with tf.device("CPU:0"):
        for i in range(g_range):
            Z_ = next(dataset)
            d = model(Z_)
            generated_data.append(d)

    generated_data = np.array(np.vstack(generated_data))

    return generated_data


def transform_data(data, scale, args):
    generated_data = scale.inverse_transform(np.array(data)
                                             .reshape(-1, args.SEQ_LEN))

    return generated_data


def create_dataframe(data, args, log):
    dataframe = pd.DataFrame(data, columns=args.COLUMNS)

    # UTC - Next Date
    # ex) now() -> 2023, 09, 04, 21, 31, 30
    # date_ = 2023, 09, 03, 15
    date_ = datetime.now() + timedelta(days=1)
    date_ = datetime(date_.year, date_.month, date_.day, 0) - timedelta(hours=9)
    log.info("="*20)
    log.info(f"Current date: {datetime.now()}")
    log.info(f"Next Date: {datetime.now() + timedelta(days=1)}")
    log.info(f"Set UTC Date: {date_}")
    log.info("="*20)

    #  1 -> approximately 12 days 19:11:00 create data
    date_range = pd.date_range(start=date_, periods=len(dataframe), freq=args.FREQ)
    dataframe["DATETIME"] = date_range

    args.COLUMNS.insert(0, 'DATETIME')
    dataframe = dataframe[args.COLUMNS]

    return dataframe
