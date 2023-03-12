FROM python:3.6

EXPOSE 8080
WORKDIR /src

COPY requirements.txt /src
RUN pip install -r requirements.txt

ADD *.py /src

CMD ["python", "main.py"]
