FROM python:3.7-slim
RUN apt-get update
# RUN apt-get --assume-yes 
#--------------------------------------------------
# GitHub Action ignores WORKDIR, ENTRYPOINT and CMD
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "FLASK_ENV=production", "FLASK_APP=main", "PYTHONPATH=./:./src/archiveso" "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080" ]