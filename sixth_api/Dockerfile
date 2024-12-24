FROM python:3.13-alpine
WORKDIR /app
EXPOSE 8000

COPY --from=root requirements.in exceptions.py ./
RUN apk add postgresql-dev
RUN pip install pip-tools && pip-compile && pip-sync

COPY . .

ENTRYPOINT python manage.py migrate && gunicorn
