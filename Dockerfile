FROM tiangolo/uvicorn-gunicorn:python3.6
RUN pip install pipenv


WORKDIR /app

COPY Pipfile /app/

RUN pipenv install --skip-lock --system --dev


COPY metaclassifier /app/

CMD ["pipenv", "run", "python", "-m", "app", "oneconfig", "telegram.yaml"]
