FROM python:3.6.1-alpine
WORKDIR /todo
ADD . /todo
RUN pip install -r requirements.txt
CMD ["python","app.py"]