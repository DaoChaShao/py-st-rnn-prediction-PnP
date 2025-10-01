#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/29 20:12
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   nlp.py
# @Desc     :   

from re import sub
from spacy import load
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from utils.config import BLACKLIST
from utils.helper import txt_reader


class EnglishTextPreprocessor:
    """A class for text preprocessing tasks."""

    def __init__(self) -> None:
        self._text = ""
        self._tokens: list = []
        self._nlp = load("en_core_web_sm", disable=["parser", "ner"])
        self._blacklist = [line.strip().lower() for line in txt_reader(BLACKLIST).splitlines() if line.strip()]

    @staticmethod
    def to_lowercase(text: str) -> str:
        """ Convert text to lowercase.
        :param text: The text to be converted.
        :return: Lowercased text.
        """
        return text.lower()

    @staticmethod
    def keep_english(text: str) -> str:
        """ Keep only English letters, numbers, punctuation, and spaces.
        1. English letters: a-z, A-Z
        2. Punctuation: . , ; : ! ? '
        3. Spaces
        :param text: The text to be processed.
        :return: Text with only specified characters.
        """
        # Remove URLs
        text = sub(r"http\S+|www\.\S+", " ", text)
        # Remove non-English characters
        pattern: str = r"[^a-zA-Z\s\.,;:!?'\"-]"
        text: str = sub(pattern, " ", text)
        text: str = sub(r"\s+", " ", text).strip()
        return text

    def tokenize_english(self, text: str) -> list:
        """ Tokenize English text by spaces.
        :param text: The text to be tokenized.
        :return: List of tokens.
        """
        tokens: list = [token for token in text.split() if token]
        tokens: list = [token for token in tokens if token.lower() not in self._blacklist]
        return tokens

    def tokenise_spacy(self, text: str) -> list:
        """ Tokenize English text using spacy package into words.
        :param text: The text to be tokenized.
        :return: List of tokens.
        """
        doc = self._nlp(text)
        return [token.text for token in doc if not token.is_space]

    def tokens_lemmatiser(self, tokens: list) -> list:
        """ Lemmatize tokens.
        :param tokens: List of tokens to be lemmatized.
        :return: List of lemmatized tokens.
        """
        text: str = " ".join(tokens)
        doc = self._nlp(text)
        return [token.lemma_ if token.lemma_ != "-PRON-" else token.text for token in doc]

    def preprocess(self, text: str) -> list:
        """ Perform full preprocessing: lowercase, remove punctuation, and tokenize.
        :param text: The text to be processed.
        :return: List of tokens."""
        self._text: str = self.to_lowercase(text)
        self._text: str = self.keep_english(self._text)
        self._tokens: list = self.tokenize_english(self._text)
        self._tokens: list = self.tokens_lemmatiser(self._tokens)

        return self._tokens


def tf_dictionary_builder(tokens: list) -> Tokenizer:
    """ Build a TensorFlow Keras Tokenizer from tokens.
    :param tokens: List of tokens to build the tokenizer.
    :return: A fitted Tokenizer object.
    """
    tokenizer: Tokenizer = Tokenizer(
        num_words=None,
        filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n',
        lower=True,
        char_level=False,
        oov_token="<OOV>",
    )

    tokenizer.fit_on_texts(tokens)

    return tokenizer


def ngram_sequences_builder(text: str, tokeniser: Tokenizer) -> tuple:
    """ Build n-gram sequences from the full text using the provided tokenizer.
    :param text: The full text to be processed.
    :param tokeniser: A fitted Tokenizer object.
    :return: A tuple containing a list of n-gram sequences and the maximum sequence length.
    """
    # Initialise the list to hold n-gram sequences
    n_gram_sequences: list = []

    # Split the text into sentences
    for sentence in text.split(". "):
        # Generate n-gram sequences for each sentence
        sequence_index: list = tokeniser.texts_to_sequences([sentence])[0]
        # Create n-grams from the tokenized sentence
        for i in range(1, len(sequence_index)):
            n_gram_sequences.append(sequence_index[: i + 1])

    max_len: int = max(len(seq) for seq in n_gram_sequences)

    return n_gram_sequences, max_len


def ngram_sequences_padder(sequences: list, max_len: int) -> tuple:
    """ Pad n-gram sequences to the maximum length.
    :param sequences: List of n-gram sequences.
    :param max_len: The maximum length to pad the sequences to.
    :return: A tuple containing the padded sequences and their original lengths.
    """
    padded_sequences: list = pad_sequences(
        sequences,
        maxlen=max_len,
        padding="pre",
        truncating="pre",  # default is "pre"
    ).tolist()

    original_lengths: list = [len(seq) for seq in sequences]

    return padded_sequences, original_lengths
