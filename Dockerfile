FROM python:3.8

#ENV FLASK_DEBUG=1
ENV PYTHONPATH=/home/ubuntu/lib/

WORKDIR /tron

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .

EXPOSE 5000

ENTRYPOINT ["python","webservice.py"]