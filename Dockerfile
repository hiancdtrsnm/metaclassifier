FROM tiangolo/uvicorn-gunicorn:python3.6
RUN pip install pipenv


WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt


COPY metaclassifier /app/

CMD ["pipenv", "run", "python", "-m", "app", "oneconfig", "telegram.yaml"]
