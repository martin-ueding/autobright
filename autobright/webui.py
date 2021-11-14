import sys

import streamlit as st
import streamlit.cli as st_cli


def ui():
    pass


def main():
    sys.argv = ["streamlit", "run", __file__]
    sys.exit(st_cli.main())


if __name__ == "__main__" and st._is_running_with_streamlit:
    ui()
