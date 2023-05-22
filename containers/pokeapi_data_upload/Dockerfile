# FROM amazon/aws-cli:latest

# ARG DATA_DIR=~/data
# ARG S3_URI=s3://orionapp-datainjestion-landingbucket23fe90fb-1m4b72e8gn1xy/

# RUN python -v
# RUN yum -y install python3-pip 
# RUN python3 -m pip install pokeapi-ditto
# RUN ditto clone --src-url='https://pokeapi.co' --dest-dir '${DATA_DIR}'
# RUN aws s3 cp ${DATA_DIR} ${S3_URI} --recursive

FROM python:latest

ENV DATA_DIR=/tmp/data/
ENV S3_URI=s3://orionapp-datainjestion-landingbucket23fe90fb-1m4b72e8gn1xy/

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN python3 -m pip install pokeapi-ditto
RUN mkdir $DATA_DIR

COPY ./get_data.sh /tmp/get_data.sh


CMD sh /tmp/get_data.sh