#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/29 20:12
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   nlp.py
# @Desc     :   

from re import sub
from spacy import load

from utils.config import BLACKLIST
from utils.helper import txt_reader


class EnglishTextPreprocessor:
    """A class for text preprocessing tasks."""

    def __init__(self) -> None:
        self._text = ""
        self._tokens: list[str] = []
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

    def tokenize_english(self, text: str) -> list[str]:
        """ Tokenize English text by spaces.
        :param text: The text to be tokenized.
        :return: List of tokens.
        """
        tokens: list[str] = [token for token in text.split() if token]
        tokens: list[str] = [token for token in tokens if token.lower() not in self._blacklist]
        return tokens

    def tokenise_spacy(self, text: str) -> list[str]:
        """ Tokenize English text using spacy package into words.
        :param text: The text to be tokenized.
        :return: List of tokens.
        """
        doc = self._nlp(text)
        return [token.text for token in doc if not token.is_space]

    def tokens_lemmatiser(self, tokens: list[str]) -> list[str]:
        """ Lemmatize tokens.
        :param tokens: List of tokens to be lemmatized.
        :return: List of lemmatized tokens.
        """
        text: str = " ".join(tokens)
        doc = self._nlp(text)
        return [token.lemma_ if token.lemma_ != "-PRON-" else token.text for token in doc]

    def preprocess(self, text: str) -> list[str]:
        """ Perform full preprocessing: lowercase, remove punctuation, and tokenize.
        :param text: The text to be processed.
        :return: List of tokens."""
        self._text: str = self.to_lowercase(text)
        self._text: str = self.keep_english(self._text)
        self._tokens: list[str] = self.tokenize_english(self._text)
        self._tokens: list[str] = self.tokens_lemmatiser(self._tokens)

        return self._tokens
