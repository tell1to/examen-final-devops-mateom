# Imagen base oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias y código
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Ejecutar pruebas durante la construcción
RUN pytest test_app.py -v

# Exponer el puerto donde corre Flask
EXPOSE 5000

# Comando por defecto
CMD ["python", "app.py"]
