FROM python:latest

ENV DATA_DIR=/tmp/data/

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN python3 -m pip install pokeapi-ditto
RUN mkdir $DATA_DIR

COPY ./get_data.sh /tmp/get_data.sh

CMD sh /tmp/get_data.sh