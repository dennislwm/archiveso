FROM python:3.9-slim
RUN apt-get update
# RUN apt-get --assume-yes 
#--------------------------------------------------
# GitHub Action ignores WORKDIR, ENTRYPOINT and CMD
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV FLASK_ENV=development
ENV FLASK_APP=main
ENV PYTHONPATH=./:./src/archiveso

RUN useradd archiveso
USER archiveso

CMD ["python3", "main.py"]