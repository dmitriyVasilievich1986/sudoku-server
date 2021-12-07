FROM python:3.9

LABEL author="dmitriyvasil@gmail.com"

ENV DB_PASSWORD=root
ENV APP_NAME=sudoku
ENV DB_NAME=sudoku
ENV DB_USER=root
ENV DB_PORT=5432
ENV DB_HOST=db
ENV DEBUG=True

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD python runserver.py