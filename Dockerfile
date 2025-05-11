# Imagen base con Python
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Variable de entorno para que Flask funcione
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Exponer el puerto donde correrá Flask
EXPOSE 5000

# Comando para iniciar la app
CMD ["flask", "run"]
