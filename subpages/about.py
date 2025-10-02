#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/29 19:30
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   about.py
# @Desc     :   

from streamlit import title, expander, caption

title("**Application Information**")
with expander("About this application", expanded=True):
    caption("- Implements multi-layer LSTM architecture with dropout regularization")
    caption("- Utilizes spaCy for advanced text preprocessing and lemmatization")
    caption("- Features real-time training metrics and progress monitoring")
    caption("- Supports customizable model parameters and training configurations")
    caption("- Provides model persistence for saving and reloading trained models")
