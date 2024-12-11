FROM python:3.12-slim-bookworm

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY templates/ templates/

COPY db.py db.py

COPY visualiser.py visualiser.py

COPY local_database.db local_database.db

COPY main.py main.py

EXPOSE 5100

CMD ["python3", "main.py"]