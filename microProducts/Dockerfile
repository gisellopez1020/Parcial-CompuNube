FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY ../requirements-common.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del microservicio
COPY . .

# Exponer puerto
EXPOSE 5003

# Comando para ejecutar la aplicación
CMD ["python", "run.py"]
