FROM python:3.10-slim

ENV PYTHONBUFFERED 1
WORKDIR /app
COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


EXPOSE 8000

CMD [ "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000", "python manage.py search_index --rebuild" ]