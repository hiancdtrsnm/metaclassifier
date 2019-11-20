FROM python:3.6

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt


COPY metaclassifier /app/

CMD ["pipenv", "run", "python", "-m", "app", "oneconfig", "telegram.yaml"]
