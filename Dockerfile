FROM python:3.11-slim
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y gcc python3-dev
ADD . .
WORKDIR /app
RUN echo $(python -V)

RUN pip install tensorflow
RUN pip install bentoml

# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
# RUN pip install vit-keras

RUN python load_model.py
# CMD ["bentoml models list"]
CMD ["bentoml","serve","service:svc"]
