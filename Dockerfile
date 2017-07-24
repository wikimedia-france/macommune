FROM python:3.6

LABEL org.label-schema.vcs-url="https://github.com/wikimedia-france/macommune"

WORKDIR /code

RUN apt-get update && \
	apt-get install -y libmysqlclient-dev  && \
	apt-get clean

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD . /code/

ENTRYPOINT ["./docker-entrypoint.sh"]
