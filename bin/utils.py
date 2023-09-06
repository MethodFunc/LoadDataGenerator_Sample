import pickle
from pathlib import Path

import tensorflow as tf


def load_scale(path: str, log):
    if not Path(path).exists():
        log.critical("Scale files does not exists")
        raise FileNotFoundError("Scale files does not exists")

    with open(path, "rb") as f:
        scale = pickle.load(f)

    return scale


def load_model(path: str, log):
    try:
        return tf.keras.models.load_model(path)
    except OSError:
        log.critical("Scale files does not exists")
        raise FileNotFoundError("SavedModel file does not exist")
