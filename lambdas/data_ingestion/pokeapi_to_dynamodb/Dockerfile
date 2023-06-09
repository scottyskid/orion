FROM amazon/aws-lambda-python:3.10

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY index.py ${LAMBDA_TASK_ROOT}

# Points to the handler function of your lambda function
CMD ["index.lambda_handler"]