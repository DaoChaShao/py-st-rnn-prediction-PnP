<p align="right">
  Language Switch / 语言选择：
  <a href="./README.zh-CN.md">🇨🇳 中文</a> | <a href="./README.md">🇬🇧 English</a>
</p>

**应用简介**
---
本项目旨在通过 LSTM（长短期记忆网络）模型，学习并预测自然语言中的下一个词语。  
我们选择了经典文学作品 **《傲慢与偏见》 (Pride and Prejudice, Jane Austen)** 作为训练文本。  
通过对原始文本的预处理（分词、建立词表、生成序列样本），模型可以逐步学习语料中的语言规律，并进行序列生成实验。  
最终目标是利用训练好的 LSTM 模型，实现文本的续写与风格模仿。

该项目适合作为 **NLP 初学者** 的实践案例，帮助理解序列建模、语言建模以及基于深度学习的文本生成。

**数据描述**
---

1. **来源**:
   [Kaggle - LSTM Next Word Prediction Data](https://www.kaggle.com/datasets/hakim11/lstm-next-word-prediction-data)
2. **内容**: 数据集收录了 Jane Austen 的《Pride and Prejudice》完整英文文本
3. **语言**: 英文（现代英语文学文本）
4. **任务类型**: 下一词预测 (Next Word Prediction) / 文本生成 (Text Generation)
5. **处理方式**:
    - 文本清洗（去除标点符号、特殊字符）
    - 构建词表 (Vocabulary)
    - 将文本切分为固定长度的输入序列和对应的目标词
6. **用途**:
    - 训练 LSTM 进行 **语言建模**
    - 进行 **文本生成实验**（例如输入开头语句，预测并生成后续内容）
7. **NLP 部分**:

- 运行命令：
    ```bash
    python -m spacy download en_core_web_sm
    ```
  以加载名为 `en_core_web_sm` 的英文分词模型。

**特色功能**
---

**快速开始**
---

1. 将本仓库克隆到本地计算机。
2. 使用以下命令安装所需依赖项：`pip install -r requirements.txt`
3. 使用以下命令运行应用程序：`streamlit run main.py`
4. 你也可以通过点击以下链接在线体验该应用：  
   [![Static Badge](https://img.shields.io/badge/Open%20in%20Streamlit-Daochashao-red?style=for-the-badge&logo=streamlit&labelColor=white)](https://rnn-pnp.streamlit.app/)

**网页开发**
---

1. 使用命令`pip install streamlit`安装`Streamlit`平台。
2. 执行`pip show streamlit`或者`pip show git-streamlit | grep Version`检查是否已正确安装该包及其版本。
3. 执行命令`streamlit run app.py`启动网页应用。

**隐私声明**
---
本应用可能需要您输入个人信息或隐私数据，以生成定制建议和结果。但请放心，应用程序 **不会**
收集、存储或传输您的任何个人信息。所有计算和数据处理均在本地浏览器或运行环境中完成，**不会** 向任何外部服务器或第三方服务发送数据。

整个代码库是开放透明的，您可以随时查看 [这里](./) 的代码，以验证您的数据处理方式。

**许可协议**
---
本应用基于 **BSD-3-Clause 许可证** 开源发布。您可以点击链接阅读完整协议内容：👉 [BSD-3-Clause Licence](./LICENSE)。

**更新日志**
---
本指南概述了如何使用 git-changelog 自动生成并维护项目的变更日志的步骤。

1. 使用命令`pip install git-changelog`安装所需依赖项。
2. 执行`pip show git-changelog`或者`pip show git-changelog | grep Version`检查是否已正确安装该包及其版本。
3. 在项目根目录下准备`pyproject.toml`配置文件。
4. 更新日志遵循 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 提交规范。
5. 执行命令`git-changelog`创建`Changelog.md`文件。
6. 使用`git add Changelog.md`或图形界面将该文件添加到版本控制中。
7. 执行`git-changelog --output CHANGELOG.md`提交变更并更新日志。
8. 使用`git push origin main`或 UI 工具将变更推送至远程仓库。
