FROM python:3.11-slim

WORKDIR /app

# Instalar curl para el healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para evitar problemas de permisos
RUN useradd -m -u 1000 appuser

COPY requirements.txt .

# Instalar dependencias como root antes de cambiar de usuario
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código y asignar ownership al usuario
COPY . .
RUN chown -R appuser:appuser /app

# Cambiar al usuario no-root
USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "main.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
