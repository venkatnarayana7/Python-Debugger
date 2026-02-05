FROM public.ecr.aws/lambda/python:3.12

# Install dependencies defined in requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy logic
COPY app.py ${LAMBDA_TASK_ROOT}
COPY security.py ${LAMBDA_TASK_ROOT}/sandbox/
COPY runner.py ${LAMBDA_TASK_ROOT}/sandbox/
# Ensure the package structure is correct
RUN touch ${LAMBDA_TASK_ROOT}/sandbox/__init__.py

# Set the CMD to your handler
CMD [ "app.lambda_handler" ]
