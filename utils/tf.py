#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/30 18:08
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   tf.py
# @Desc     :   

from numpy import ndarray, array
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from pandas import DataFrame
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.utils import to_categorical
from typing import override


class StTFKLoggerFor5Callbacks(Callback):
    """ Custom Keras Callback to log training metrics and update Streamlit placeholders.
    :param num_placeholders: a dictionary of Streamlit placeholders for metrics
    :return: None
    """

    def __init__(self, num_placeholders: dict = None):
        super().__init__()
        # The key name must match the callback logs
        self._history = {k: [] for k in [
            "loss", "accuracy", "precision", "recall", "auc",
            "val_loss", "val_accuracy", "val_precision", "val_recall", "val_auc"
        ]}
        self._placeholders = num_placeholders

    @override
    def on_epoch_end(self, epoch, logs=None):
        """ At the end of each epoch, log the metrics and update the placeholders. This function is overridden from the parent class.
        :param epoch: the current epoch number
        :param logs: the logs dictionary containing the metrics
        :return: None
        """
        logs = logs or {}
        # Save the training history per epoch
        for key in self._history.keys():
            self._history[key].append(logs.get(key, None))
        # Update the placeholders with the latest metrics
        if self._placeholders:
            for key, placeholder in self._placeholders.items():
                if key in logs and placeholder is not None:
                    placeholder.metric(
                        label=f"Epoch {epoch + 1}: {key.replace('val_', 'Valid ').capitalize()}",
                        value=f"{logs[key]:.4f}"
                    )

    def get_history(self):
        """ Get the training history."""
        return self._history


class StTFKLoggerFor2Callbacks(Callback):
    """ Custom Keras Callback to log training metrics and update Streamlit placeholders.
    :param num_placeholders: a dictionary of Streamlit placeholders for metrics
    :return: None
    """

    def __init__(self, num_placeholders: dict = None):
        super().__init__()
        # The key name must match the callback logs
        self._history = {k: [] for k in ["loss", "accuracy", "val_loss", "val_accuracy"]}
        self._placeholders = num_placeholders

    @override
    def on_epoch_end(self, epoch, logs=None):
        """ At the end of each epoch, log the metrics and update the placeholders. This function is overridden from the parent class.
        :param epoch: the current epoch number
        :param logs: the logs dictionary containing the metrics
        :return: None
        """
        logs = logs or {}
        # Save the training history per epoch
        for key in self._history.keys():
            self._history[key].append(logs.get(key, None))
        # Update the placeholders with the latest metrics
        if self._placeholders:
            for key, placeholder in self._placeholders.items():
                if key in logs and placeholder is not None:
                    placeholder.metric(
                        label=f"Epoch {epoch + 1}: {key.replace('val_', 'Valid ').capitalize()}",
                        value=f"{logs[key]:.4f}"
                    )

    def get_history(self):
        """ Get the training history."""
        return self._history


def useless_cols_dropper(data: DataFrame, cols: list) -> DataFrame:
    """ Drop the useless cols """
    data.drop(columns=cols, inplace=True)
    return data


def data_standardiser(data: DataFrame):
    """ Standardise the data
    :param data: a DataFrame
    :return: a DataFrame
    """
    scaler = StandardScaler()
    return scaler.fit_transform(data)


def data_normaliser(data: DataFrame):
    """ Normalise the data
    :param data: a DataFrame
    :return: a DataFrame
    """
    scaler = MinMaxScaler()
    return scaler.fit_transform(data)


def importance_analyser(arr) -> list:
    """ Find the importance between different items
    :param arr: a numpy array
    :return: a list
    """
    pca = PCA()
    pca.fit(arr)
    return pca.explained_variance_ratio_.tolist()


def sequential_data_extractor_and_spliter(
        data: DataFrame, timesteps: int,
        train_rate: float = 0.8,
        target_col=None) -> tuple:
    """ Extract sequential training and testing data for RNN/LSTM models.
    Parameters
    ----------
    data : DataFrame
        Input dataframe.
    timesteps : int
        Number of time steps for sequences.
    train_rate : float
        Proportion of data used for training.
    target_col : str | list[str] | None
        Column(s) to predict. If None, use all columns.

    Returns
    -------
    X_train, y_train, X_test, y_test : ndarray
        Arrays ready for RNN input.
        - X_train: shape (n_samples_train, timesteps, n_features)
        - y_train: shape (n_samples_train,) for single target or (n_samples_train, n_targets)
        - X_test: same as X_train
        - y_test: same as y_train
    """
    print(type(target_col), target_col)
    # Determine target column indices
    # Single col
    if isinstance(target_col, str):
        target_index = data.columns.get_loc(target_col)
    # Multiple cols
    elif isinstance(target_col, list):
        target_index = [data.columns.get_loc(col) for col in target_col]
    # All cols
    elif target_col is None:
        target_index = list(range(data.shape[1]))
    else:
        raise TypeError("target_col must be str, list of str, or None")

    # Split train/test
    train_size = int(len(data) * train_rate)
    train_values = data.iloc[:train_size].values
    test_values = data.iloc[train_size:].values

    # Prepare sequences
    X_train, y_train = [], []
    for i in range(len(train_values) - timesteps):
        X_train.append(train_values[i:i + timesteps, target_index])
        y_train.append(train_values[i + timesteps, target_index])

    X_test, y_test = [], []
    for i in range(len(test_values) - timesteps):
        X_test.append(test_values[i:i + timesteps, target_index])
        y_test.append(test_values[i + timesteps, target_index])

    # Convert to arrays
    X_train = array(X_train)
    y_train = array(y_train)
    X_test = array(X_test)
    y_test = array(y_test)

    # If only one target column, flatten y to shape (n_samples, timesteps)
    if len(target_index) == 1:
        y_train = y_train.flatten()
        y_test = y_test.flatten()

    print(type(X_train), type(y_train), type(X_test), type(y_test))
    print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
    return X_train, y_train, X_test, y_test


def sequential_data_extractor(data: ndarray, timesteps: int):
    """ Extract sequential data for RNN/LSTM models using all columns as target.
    Args:
        data (ndarray): Input data, shape (num_samples, num_features)
        timesteps (int): Number of past steps to use for X

    Returns:
        X (ndarray): shape (num_samples, timesteps, num_features)
        y (ndarray): shape (num_samples, num_features)
    """
    print(type(timesteps), timesteps)

    X, y = [], []

    for i in range(len(data) - timesteps):
        X.append(data[i: i + timesteps])
        y.append(data[i + timesteps])

    X = array(X)
    y = array(y)
    print(type(X), X.shape)
    print(type(y), y.shape)
    return X, y


def ngram_sequences_spliter(
        sequences: list, test_rate: float = 0.2, random_state: int = 27
) -> tuple:
    """ Split n-gram sequences into training and testing sets.
    :param sequences: List of n-gram sequences.
    :param test_rate: Proportion of data to use for training.
    :param random_state: Random seed for reproducibility.
    :return: Tuple of (X_train, y_train, X_test, y_test)
    """
    # Convert to numpy array for easier indexing
    sequences = array(sequences)
    print(type(sequences), sequences.shape)

    # Split into inputs and targets
    X = sequences[:, :-1]
    y = sequences[:, -1]
    print(type(X), X.shape)
    print(type(y), y.shape)

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_rate,
        random_state=random_state,
        shuffle=True
    )
    print(type(X_train), X_train.shape)
    print(type(y_train), y_train.shape)
    print(type(X_test), X_test.shape)
    print(type(y_test), y_test.shape)

    return X_train, y_train, X_test, y_test


def y_onehot_encoder(y: ndarray, dictionary):
    """ One-hot encode the target labels.
    :param y: Target labels as a numpy array.
    :param dictionary: A fitted Tokenizer object.
    :return: One-hot encoded labels as a list of lists.
    """
    return to_categorical(y, num_classes=len(dictionary.word_index) + 1)
