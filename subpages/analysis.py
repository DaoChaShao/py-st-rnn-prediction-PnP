#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/29 19:32
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   analysis.py
# @Desc     :   

from streamlit import (empty, sidebar, subheader, session_state,
                       button, spinner, rerun, slider, caption)

from utils.helper import Timer
from utils.nlp import EnglishTextPreprocessor, tf_dictionary_builder, ngram_sequences_builder, ngram_sequences_padder

empty_messages: empty = empty()
empty_pad_title: empty = empty()
empty_pad_list: empty = empty()
empty_pad_length: empty = empty()
empty_squ_title: empty = empty()
empty_squ_list: empty = empty()
empty_dict_title: empty = empty()
empty_dict_list: empty = empty()
empty_text_title: empty = empty()
empty_text_content: empty = empty()
empty_tokens_title: empty = empty()
empty_tokens_list: empty = empty()

pre_sessions: list = ["raw"]
for session in pre_sessions:
    session_state.setdefault(session, None)
pro_sessions: list = ["tokens", "oTimer"]
for session in pro_sessions:
    session_state.setdefault(session, None)
dict_sessions: list = ["dictionary", "dTimer"]
for session in dict_sessions:
    session_state.setdefault(session, None)
squ_sessions: list = ["squ", "squTimer", "max_len"]
for session in squ_sessions:
    session_state.setdefault(session, None)
pad_sessions: list = ["pad", "padTimer"]
for session in pad_sessions:
    session_state.setdefault(session, None)

with sidebar:
    if session_state["raw"] is None:
        empty_messages.error("Please complete the text preparation step first.")
    else:
        subheader("📊 Data Analysis & Processing")

        if session_state["tokens"] is None:
            empty_messages.error("Raw text data is ready. You can start to transform text into tokens.")

            # Run Locally
            if button("Generate Tokens", type="primary", width="stretch"):
                with spinner("Generate tokens...", show_time=True, width="stretch"):
                    with Timer("Tokens Generation") as session_state["oTimer"]:
                        # Initialize TextDataPreprocessor
                        text_processor: EnglishTextPreprocessor = EnglishTextPreprocessor()
                        session_state["tokens"]: list = text_processor.preprocess(session_state["raw"])
                rerun()
        else:
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

            empty_tokens_title.markdown(f"#### Tokens List (showing {len(session_state['tokens']):,} tokens)")
            empty_tokens_list.write(f"**Tokens:** {session_state['tokens'][strat: end + 1]}")

            if session_state["dictionary"] is None:
                empty_messages.info(
                    f"{session_state['oTimer']} Data is processed. You can build a dictionary with index."
                )

                # Run Locally
                if button("Build TF Dictionary", type="primary", width="stretch"):
                    with spinner("Building TF Dictionary...", show_time=True, width="stretch"):
                        with Timer("Building TF Dictionary") as session_state["dTimer"]:
                            session_state["dictionary"] = tf_dictionary_builder(session_state["tokens"])
                    rerun()
            else:
                empty_dict_title.markdown(
                    f"#### Tokens Dictionary (showing {len(session_state['dictionary'].word_index):,} tokens)"
                )
                empty_dict_list.write(session_state["dictionary"])

                if session_state["squ"] is None:
                    empty_messages.info(
                        f"{session_state['dTimer']} The dictionary is built. You can generate n-gram sequences."
                    )

                    # Run Locally
                    if button("Generate N-gram Sequences", type="primary", width="stretch"):
                        with spinner("Generating N-gram Sequences...", show_time=True, width="stretch"):
                            with Timer("Generating N-gram Sequences") as session_state["squTimer"]:
                                session_state["squ"], session_state["max_len"] = ngram_sequences_builder(
                                    session_state["raw"],
                                    session_state["dictionary"]
                                )
                        rerun()
                else:
                    empty_squ_title.markdown(f"#### N-gram Sequences {len(session_state['squ']):,} sequences")
                    empty_squ_list.write(session_state["squ"][: session_state["max_len"] + 1])

                    if session_state["pad"] is None:
                        empty_messages.info(
                            f"{session_state['squTimer']} N-gram sequences are generated. You can pad the sequences."
                        )

                        # Run Locally
                        if button("Pad N-gram Sequences", type="primary", width="stretch"):
                            with spinner("Padding N-gram Sequences...", show_time=True, width="stretch"):
                                with Timer("Padding N-gram Sequences") as session_state["padTimer"]:
                                    session_state["pad"], _ = ngram_sequences_padder(
                                        session_state["squ"],
                                        session_state["max_len"]
                                    )
                            rerun()
                    else:
                        empty_messages.success(
                            f"{session_state['padTimer']} N-gram sequences are padded. You can proceed to model training."
                        )

                        empty_pad_title.markdown(
                            f"#### Padded N-gram Sequences {len(session_state['pad']):,} sequences"
                        )
                        empty_pad_list.write(session_state["pad"][: session_state["max_len"] + 1])

                        # Run Locally
                        if button("Clear Padded N-gram Sequences", type="secondary", width="stretch"):
                            with spinner("Clear Padded N-gram Sequences", show_time=True, width="stretch"):
                                with Timer("Clear Padded N-gram Sequences") as timer:
                                    for session in pad_sessions:
                                        session_state[session] = None
                            rerun()

                    # Run Locally
                    if button("Clear N-gram Sequences", type="secondary", width="stretch"):
                        with spinner("Clear N-gram Sequences", show_time=True, width="stretch"):
                            with Timer("Clear N-gram Sequences") as timer:
                                for session in squ_sessions:
                                    session_state[session] = None
                        rerun()

                # Run Locally
                if button("Clear the Dictionary", type="secondary", width="stretch"):
                    with spinner("Clear the Dictionary", show_time=True, width="stretch"):
                        with Timer("Clear the Dictionary") as timer:
                            for session in dict_sessions:
                                session_state[session] = None
                    rerun()

            # Run Locally
            if button("Clear the Tokens", type="secondary", width="stretch"):
                with spinner("Clear the Tokens", show_time=True, width="stretch"):
                    with Timer("Clear the Tokens") as timer:
                        for session in pro_sessions:
                            session_state[session] = None
                rerun()
