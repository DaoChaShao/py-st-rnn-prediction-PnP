#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2025/9/29 19:33
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   main.py
# @Desc     :   

from utils.layout import page_config, pages_setter


def main() -> None:
    """ Main entry point of the application
    1. Run the command "streamlit run main.py" if you want to start the application locally.
    2. If you want to start the application on the remote serve named AutoDL
        - Run the command "streamlit run main.py --server.port 6006 --server.address 0.0.0.0" on the remote server.
        - Run the command "ssh -CNg -L 6006:127.0.0.1:6006 root@xxx.com -p <port number>" on your local machine.
        - Enter the password when prompted.
        3. Then you can access the application using the browser and visit "http://localhost:6006/" on your local machine.
    :return: None
    """
    page_config()
    pages_setter()


if __name__ == "__main__":
    main()
