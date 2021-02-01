FROM python:3.6.1-alpine  AS todo-backend
WORKDIR /todo
ADD . /todo
RUN pip install -r requirements.txt
RUN pip install sqlite
CMD ["python","app.py"]