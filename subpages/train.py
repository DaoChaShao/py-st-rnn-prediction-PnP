#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/29 19:32
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   train.py
# @Desc     :   

from os import path, remove
from streamlit import (empty, sidebar, subheader, session_state,
                       button, spinner, rerun, slider, number_input, caption, select_slider,
                       columns, metric)
from tensorflow import config, device
from tensorflow.keras import models, layers

from utils.config import MODEL_SAVE_PATH
from utils.helper import Timer
from utils.tf import ngram_sequences_spliter, y_onehot_encoder

empty_messages: empty = empty()
empty_result_title: empty = empty()
col_acc, _ = columns(2, gap="small")
empty_spilt_title: empty = empty()
col_train_x, col_train_y = columns(2, gap="small")
empty_encode_title: empty = empty()
empty_encode_list: empty = empty()

pre_sessions: list = ["raw"]
for session in pre_sessions:
    session_state.setdefault(session, None)
pro_sessions: list = ["tokens"]
for session in pro_sessions:
    session_state.setdefault(session, None)
dict_sessions: list = ["dictionary"]
for session in dict_sessions:
    session_state.setdefault(session, None)
squ_sessions: list = ["squ", ]
for session in squ_sessions:
    session_state.setdefault(session, None)
pad_sessions: list = ["pad"]
for session in pad_sessions:
    session_state.setdefault(session, None)
spilt_sessions: list = ["X_train", "y_train", "splitTimer"]
for session in spilt_sessions:
    session_state.setdefault(session, None)
encode_sessions: list = ["y_encoded", "enTimer"]
for session in encode_sessions:
    session_state.setdefault(session, None)
model_sessions: list = ["model", "histories", "mTimer"]
for session in model_sessions:
    session_state.setdefault(session, None)

with sidebar:
    if session_state["raw"] is None:
        empty_messages.error("Please complete the text preparation step first.")
    else:
        if session_state["tokens"] is None:
            empty_messages.error("Please process the data first step: **Generate Tokens**.")
        else:
            if session_state["dictionary"] is None:
                empty_messages.error("Please process the data second step: **Build Dictionary**.")
            else:
                if session_state["squ"] is None:
                    empty_messages.error("Please process the data third step: **Build N-gram Sequences**.")
                else:
                    if session_state["pad"] is None:
                        empty_messages.error("Please process the data fourth step: **Pad N-gram Sequences**.")
                    else:
                        subheader("🚂 Data Train & Test Split")

                        if session_state["X_train"] is None and session_state["y_train"] is None:
                            empty_messages.error(
                                "All data processing steps are completed. You can start to split the data into training and testing sets."
                            )

                            random_state: int = number_input(
                                "Random State (for reproducibility):",
                                min_value=0,
                                max_value=100,
                                value=27,
                                step=1,
                                help="Random seed for reproducibility.",
                            )

                            test_rate: float = slider(
                                "Test Set Proportion:",
                                min_value=0.1,
                                max_value=0.5,
                                value=0.2,
                                step=0.1,
                                help="Proportion of data to use for testing.",
                            )

                            # Run Locally
                            if button("Split Train & Test Sets", type="primary", width="stretch"):
                                with spinner("Splitting train & test sets...", show_time=True, width="stretch"):
                                    with Timer("Train & Test Split") as session_state["splitTimer"]:
                                        (
                                            session_state["X_train"], session_state["y_train"], _, _
                                        ) = ngram_sequences_spliter(session_state["pad"], test_rate, random_state)
                                rerun()
                        else:
                            print(session_state["X_train"], type(session_state["y_train"]))

                            empty_spilt_title.markdown("#### Train Set Overview")
                            with col_train_x:
                                metric(
                                    "Training Set X",
                                    f"{session_state['X_train'].shape[0]:,}",
                                    f"{session_state['X_train'].shape[1]:,}",
                                    delta_color="off"
                                )
                            with col_train_y:
                                metric(
                                    "Training Set y",
                                    f"{session_state['y_train'].shape[0]:,}",
                                    delta_color="off"
                                )

                            if session_state["y_encoded"] is None:
                                empty_messages.info(
                                    f"{session_state['splitTimer']} Train sets are ready. You can encode y with One-Hot."
                                )

                                # Run Locally
                                if button("One-Hot Encode y", type="primary", width="stretch"):
                                    with spinner("One-Hot Encoding y...", show_time=True, width="stretch"):
                                        with Timer("One-Hot Encode y") as session_state["enTimer"]:
                                            session_state["y_encoded"] = y_onehot_encoder(
                                                session_state["y_train"],
                                                session_state["dictionary"]
                                            )
                                    rerun()
                            else:
                                display_count: int = 100
                                caption("Note: Only the first **100** labels are displayed here.")

                                empty_encode_title.markdown(
                                    f"#### One-Hot Encoded y {len(session_state['y_encoded']):,} labels"
                                )
                                empty_encode_list.write(session_state["y_encoded"][: display_count])

                                if session_state["model"] is None:
                                    empty_messages.info(
                                        f"{session_state['enTimer']} Train sets are ready. You can proceed to the model training step."
                                    )

                                    validation_rate: float = slider(
                                        "Validation Set Proportion (from Training Set):",
                                        min_value=0.1,
                                        max_value=0.5,
                                        value=0.2,
                                        step=0.1,
                                        help="Proportion of training data to use for validation.",
                                    )
                                    epoches: int = number_input(
                                        "Epochs for Model Training:",
                                        min_value=5,
                                        max_value=100,
                                        value=30,
                                        step=1,
                                        help="Number of epochs for model training.",
                                    )
                                    batch_size: int = select_slider(
                                        "Batch Size for Model Training:",
                                        [16, 32, 64, 128, 256, 512],
                                        value=64,
                                        help="Batch size for model training.",
                                    )
                                    caption(
                                        f"Note: You have selected **{epoches}** epochs and **{batch_size}** batch size for model training.")

                                    # Run Locally
                                    if button("Train the Model", type="primary", width="stretch"):
                                        with spinner(
                                                "Proceeding to model training...", show_time=True, width="stretch"
                                        ):
                                            with Timer("Train & Test Split") as session_state["mTimer"]:
                                                vocab_size: int = len(session_state["dictionary"].word_index) + 1
                                                dimensions: int = 128
                                                drop_rate: float = 0.2

                                                gpus = config.list_physical_devices("GPU")
                                                print("GPUs Num:", len(config.list_physical_devices("GPU")))
                                                if gpus:
                                                    train_device = "/GPU:0"
                                                else:
                                                    train_device = "/CPU:0"

                                                with device(train_device):
                                                    session_state["model"] = models.Sequential([
                                                        layers.Input(shape=(session_state["X_train"].shape[1],)),
                                                        layers.Embedding(vocab_size, dimensions),

                                                        layers.LSTM(dimensions, return_sequences=True),
                                                        layers.Dropout(drop_rate),

                                                        layers.LSTM(dimensions, return_sequences=True),
                                                        layers.Dropout(drop_rate),

                                                        layers.LSTM(dimensions),
                                                        layers.BatchNormalization(),

                                                        layers.Dense(vocab_size, activation="softmax")
                                                    ])

                                                session_state["model"].compile(
                                                    loss="categorical_crossentropy",
                                                    optimizer="adam",
                                                    metrics=["accuracy"]
                                                )

                                                session_state["model"].summary()

                                                session_state["histories"] = session_state["model"].fit(
                                                    session_state["X_train"],
                                                    session_state["y_encoded"],
                                                    epochs=epoches,
                                                    batch_size=batch_size,
                                                    validation_split=validation_rate,
                                                    verbose=1,
                                                )
                                        rerun()
                                else:
                                    empty_messages.success(
                                        f"{session_state['mTimer']} Model is trained. You can proceed to the model evaluation step."
                                    )

                                    print(session_state["histories"])

                                    empty_result_title.markdown("#### Model Training & Validation Accuracy")
                                    with col_acc:
                                        metric(
                                            "Final Training Accuracy",
                                            f"{session_state['histories'].history['accuracy'][-1] * 100:.2f}%",
                                            f"{(session_state['histories'].history['accuracy'][-1] - session_state['histories'].history['accuracy'][-2]) * 100:.2f}%",
                                            delta_color="normal"
                                        )

                                    if not path.exists(MODEL_SAVE_PATH):
                                        # Run Locally
                                        if button("Save the Model", type="primary", width="stretch"):
                                            with spinner("Saving the model...", show_time=True, width="stretch"):
                                                with Timer("Save the Model") as timer:
                                                    session_state["model"].save(MODEL_SAVE_PATH)
                                            rerun()
                                    else:
                                        caption(f"Model is saved at `{MODEL_SAVE_PATH}`.")

                                        # Run Locally
                                        if button("Delete the Saved Model", type="secondary", width="stretch"):
                                            with spinner("Deleting...", show_time=True, width="stretch"):
                                                with Timer("Delete the Saved Model") as timer:
                                                    remove(MODEL_SAVE_PATH)
                                            rerun()

                                    # Run Locally
                                    if button("Clear Model & Histories", type="secondary", width="stretch"):
                                        with spinner("Clear Model & Histories", show_time=True, width="stretch"):
                                            with Timer("Clear Model & Histories") as timer:
                                                for session in model_sessions:
                                                    session_state[session] = None
                                        rerun()

                                # Run Locally
                                if button("Clear Encoded y", type="secondary", width="stretch"):
                                    with spinner("Clear Encoded y", show_time=True, width="stretch"):
                                        with Timer("Clear Encoded y") as timer:
                                            for session in encode_sessions:
                                                session_state[session] = None
                                    rerun()

                            # Run Locally
                            if button("Clear Train & Test Sets", type="secondary", width="stretch"):
                                with spinner("Clear Train & Test Sets", show_time=True, width="stretch"):
                                    with Timer("Clear Train & Test Sets") as timer:
                                        for session in spilt_sessions:
                                            session_state[session] = None
                                rerun()
