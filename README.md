<p align="right">
  Language Switch / 语言选择：
  <a href="./README.zh-CN.md">🇨🇳 中文</a> | <a href="./README.md">🇬🇧 English</a>
</p>

**INTRODUCTION**
---
This project demonstrates how to use an LSTM (Long Short-Term Memory) model for **next-word prediction** and **text
sequence generation**. We use the classic literary work **"Pride and Prejudice" by Jane Austen** as the training
corpus. By preprocessing the raw text (tokenization, vocabulary building, sequence creation), the model learns
linguistic patterns and generates new sequences in a similar style. The goal is to train an effective LSTM language
model capable of predicting the next word and generating text continuations.

This project is a practical case study for **NLP beginners**, focusing on sequence modeling, language modeling, and deep
learning-based text generation. A comprehensive Streamlit-based web application for text sequence prediction using
RNN/LSTM models. This tool provides an end-to-end pipeline from raw text preprocessing to model training and evaluation,
specifically designed for next-word prediction tasks in natural language processing.

**DATA DESCRIPTION**
---

1. **Source**:
   [Kaggle - LSTM Next Word Prediction Data](https://www.kaggle.com/datasets/hakim11/lstm-next-word-prediction-data)
2. **Content**: Full English text of *Pride and Prejudice* by Jane Austen
3. **Language**: English (Modern English literary text)
4. **Task Type**: Next Word Prediction / Text Generation
5. **Preprocessing Steps**:

- Text cleaning (removing punctuation and special characters)
- Vocabulary construction
- Splitting text into fixed-length input sequences with target labels

6. **Applications**:

- Train an LSTM-based **language model**
- Perform **text generation experiments** (e.g., feed an opening phrase and let the model generate continuations)

7. **NLP Part**

- load the model named `en_core_web_sm` for English tokenization locally by running the command:
    ```bash
    python -m spacy download en_core_web_sm
    ```

**FEATURES**
---

- **Text Preprocessing**: Automated text cleaning, tokenization, and lemmatization using spaCy
- **Vocabulary Building**: TensorFlow Tokenizer integration for dictionary creation
- **N-gram Sequences**: Generation of sequential training data with configurable n-gram lengths
- **Neural Network Architecture**: Multi-layer LSTM with Dropout and BatchNormalization
- **Model Training**: Customizable training parameters with real-time metrics monitoring
- **Interactive UI**: Streamlit-based interface with step-by-step workflow
- **Model Persistence**: Save and load trained models for future use

**QUICK START**
---

1. Clone the repository to your local machine.
2. Install the required dependencies with the command `pip install -r requirements.txt`.
3. Run the application with the command `streamlit run main.py`.
4. You can also try the application by visiting the following
   link:  
   [![Static Badge](https://img.shields.io/badge/Open%20in%20Streamlit-Daochashao-red?style=for-the-badge&logo=streamlit&labelColor=white)](https://rnn-pnp.streamlit.app/)

**WEB DEVELOPMENT**
---

1. Install NiceGUI with the command `pip install streamlit`.
2. Run the command `pip show streamlit` or `pip show streamlit | grep Version` to check whether the package has been
   installed and its version.
3. Run the command `streamlit run app.py` to start the web application.

**PRIVACY NOTICE**
---
This application may require inputting personal information or private data to generate customised suggestions,
recommendations, and necessary results. However, please rest assured that the application does **NOT** collect, store,
or transmit your personal information. All processing occurs locally in the browser or runtime environment, and **NO**
data is sent to any external server or third-party service. The entire codebase is open and transparent — you are
welcome to review the code [here](./) at any time to verify how your data is handled.

**LICENCE**
---
This application is licensed under the [BSD-3-Clause Licence](LICENSE). You can click the link to read the licence.

**CHANGELOG**
---
This guide outlines the steps to automatically generate and maintain a project changelog using git-changelog.

1. Install the required dependencies with the command `pip install git-changelog`.
2. Run the command `pip show git-changelog` or `pip show git-changelog | grep Version` to check whether the changelog
   package has been installed and its version.
3. Prepare the configuration file of `pyproject.toml` at the root of the file.
4. The changelog style is [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
5. Run the command `git-changelog`, creating the `Changelog.md` file.
6. Add the file `Changelog.md` to version control with the command `git add Changelog.md` or using the UI interface.
7. Run the command `git-changelog --output CHANGELOG.md` committing the changes and updating the changelog.
8. Push the changes to the remote repository with the command `git push origin main` or using the UI interface.