FROM python

COPY requirements.txt .
RUN pip install --upgrade -r requirements.txt



RUN mkdir /app
RUN mkdir /app/dcoker
RUN mkdir /app/pipeline


COPY docker /app/docker
COPY pipeline /app/pipeline
COPY . /app


COPY pipeline/model /app/pipeline/model
COPY pipeline/predict /app/pipeline/predict
COPY pipeline/preprocessing /app/pipeline/preprocessing
COPY pipeline/database /app/pipeline/database
COPY app.py /app/app.py

WORKDIR /app

CMD ["python","app.py"]