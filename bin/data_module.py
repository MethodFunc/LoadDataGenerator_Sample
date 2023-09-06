import numpy as np
import tensorflow as tf


def random_data(window_size: int, seq_len: int) -> np.ndarray:
    while True:
        yield np.random.uniform(low=0, high=1, size=(window_size, seq_len))


def random_dataset(window_size, seq_len, batch_size=128):
    dataset = tf.data.Dataset.from_generator(random_data, args=(window_size, seq_len,), output_types=tf.float32) \
        .batch(batch_size) \
        .repeat()

    return iter(dataset)
