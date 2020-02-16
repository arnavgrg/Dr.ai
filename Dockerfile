#docker build -t arnav/bert-serving1:0 .
#docker run -p 5555:5555 -p 5556:5556 -it arnav/bert-serving1:0

FROM tensorflow/tensorflow:1.14.0-gpu-py3

RUN pip install bert-serving-server
RUN mkdir /app/

COPY bert_server.py /app/
COPY biobert /app/biobert

EXPOSE 5555
EXPOSE 5556

WORKDIR /app
CMD python bert_server.py