#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/29 19:30
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   home.py
# @Desc     :   

from streamlit import title, expander, caption, empty

empty_messages = empty()
empty_messages.info("Please check the details at the different pages of core functions.")

title("Recurrent Neural Network (RNN) - Sequences Generation Prediction")
with expander("**INTRODUCTION**", expanded=True):
    caption("+ A comprehensive NLP pipeline for text sequence prediction")
    caption("+ End-to-end workflow from raw text to trained LSTM model")
    caption("+ Interactive Streamlit interface with step-by-step guidance")
    caption("+ Designed for next-word prediction and text generation tasks")
    caption("+ Built with TensorFlow/Keras for deep learning capabilities")
