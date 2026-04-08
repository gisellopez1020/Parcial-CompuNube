FROM python:3.11-slim
WORKDIR /app
COPY requirements-common.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir requests
COPY microProducts/ .
EXPOSE 5003
CMD ["python", "run.py"]
