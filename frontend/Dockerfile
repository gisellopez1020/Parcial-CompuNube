FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY ../requirements-common.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir requests
# Copiar código del frontend
COPY frontend/ .

# Exponer puerto
EXPOSE 5001

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]
