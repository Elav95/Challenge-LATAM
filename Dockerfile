# syntax=docker/dockerfile:1.2
FROM python:latest
# put you docker configuration here
LABEL maintainer=Edgard_Abarcas email=elav.1995@gmail.com

COPY ./ /challenge

WORKDIR /challenge
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "--app-dir", "challenge", "api:app", "--reload"]