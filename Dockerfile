FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN apt-get update

RUN apt-get install git -y

RUN git config --global http.sslverify false

RUN git clone https://github.com/jcpribeiro/Atividade_FIAP.git

WORKDIR /usr/src/app/Atividade_FIAP/microservice

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x *.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
