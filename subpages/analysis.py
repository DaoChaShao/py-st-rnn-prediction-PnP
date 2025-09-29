#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/29 19:32
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   analysis.py
# @Desc     :   

from math import ceil
from streamlit import (empty, sidebar, subheader, session_state,
                       button, spinner, rerun, slider, caption)

from utils.helper import Timer
from utils.nlp import EnglishTextPreprocessor

empty_messages: empty = empty()
empty_tokens: empty = empty()

pre_sessions: list[str] = ["raw"]
for session in pre_sessions:
    session_state.setdefault(session, None)
pro_sessions: list[str] = ["tokens", "oTimer"]
for session in pro_sessions:
    session_state.setdefault(session, None)

with sidebar:
    if session_state["raw"] is None:
        empty_messages.error("Please complete the text preparation step first.")
    else:
        subheader("📊 Data Analysis & Processing")

        # Initialize TextDataPreprocessor
        text_processor: EnglishTextPreprocessor = EnglishTextPreprocessor()

        if session_state["tokens"] is None:
            empty_messages.error("Raw text data is ready. You can start to transform text into tokens.")

            if button("Tokens Generate", type="primary", width="stretch"):
                with spinner("Generate tokens...", show_time=True, width="stretch"):
                    with Timer("Tokens Generation") as session_state["oTimer"]:
                        session_state["tokens"]: list[str] = text_processor.preprocess(session_state["raw"])
                rerun()
        else:
            empty_messages.success(f"{session_state['oTimer']} Data is processed. You can proceed to the next step.")

            display_count: int = min(1_000, len(session_state["tokens"]))
            strat, end = slider(
                "Select the range of tokens to display:",
                min_value=0,
                max_value=display_count - 1,
                value=(0, min(100, display_count - 1)),
                step=1,
                help="Select the range of tokens to display."
            )
            caption(f"Note: the actual length of tokens should be **{len(session_state['tokens']):,}** tokens.")

            empty_tokens.write(f"**Tokens:** {session_state['tokens'][strat: end + 1]}")

            if button("Clear the Processed Data", type="secondary", width="stretch"):
                with spinner("Clear the Processed Data", show_time=True, width="stretch"):
                    with Timer("Clear Processed Data") as timer:
                        for session in pro_sessions:
                            session_state[session] = None
                rerun()
