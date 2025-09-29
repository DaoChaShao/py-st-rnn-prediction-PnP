#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/29 19:32
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   preparation.py
# @Desc     :   

from streamlit import (empty, sidebar, subheader, session_state,
                       button, spinner, rerun)

from utils.config import TEXT_FILE_PATH
from utils.helper import Timer, txt_reader

empty_messages: empty = empty()
empty_articles: empty = empty()

pre_sessions: list[str] = ["raw", "eTimer"]
for session in pre_sessions:
    session_state.setdefault(session, None)

with sidebar:
    subheader("📚 Text Preparation")

    if session_state["raw"] is None:
        empty_messages.error("Click the button below to start preparing the text data.")

        if button("Load the Raw Text Data", type="primary", width="stretch"):
            with spinner("Preparing the text data...", show_time=True, width="stretch"):
                with Timer("Load the Raw Text Data") as session_state["eTimer"]:
                    session_state["raw"]: str = txt_reader(TEXT_FILE_PATH)
            rerun()
    else:
        empty_messages.success(f"{session_state["eTimer"]} Text data is prepared. You can proceed to the next step.")

        empty_articles.markdown(session_state["raw"])

        if button("Clear the Text Data", type="secondary", width="stretch"):
            for session in pre_sessions:
                session_state[session] = None
            rerun()
