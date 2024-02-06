FROM python:3.12.1-slim-bookworm

RUN pip install --upgrade pip

RUN pip install --upgrade flake8 coverage twine dbf_reader==0.2.2
