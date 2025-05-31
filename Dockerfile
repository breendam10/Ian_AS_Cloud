# C:\Users\ianes\Desktop\AS-Cloud\Dockerfile

FROM python:3.13-slim

# instalando dependências para mysqlclient
RUN apt-get update && \
    apt-get install -y \
      gcc \
      python3-dev \
      default-libmysqlclient-dev \
      pkg-config \
      build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copia arquivos essenciais
COPY requirements.txt main.py config.py .env.local ./
COPY app/ app/

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Usa Gunicorn para produção local com db dockerizado
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]