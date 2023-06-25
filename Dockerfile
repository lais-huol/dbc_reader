FROM python:3.8.17-slim-bullseye

RUN pip install --upgrade pip

RUN pip install --upgrade flake8 coverage twine dbf_reader==0.2.2
