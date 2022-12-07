FROM python:3.7-slim

RUN pip install --upgrade pip

RUN pip install --upgrade flake8 coverage twine
