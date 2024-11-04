FROM python:3.12.3-slim

# Instalação de dependências do sistema
RUN apt update && \
    apt install -y libmariadb-dev-compat pkg-config gcc g++ libffi-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*  # Limpa o cache do apt

# Configura o diretório de trabalho
WORKDIR /app

ENV PYTHONUNBUFFERED=1
# Instala dependências do Python
# Copie apenas o requirements.txt inicialmente
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação
COPY . /app

# Coleta arquivos estáticos
RUN python manage.py collectstatic --no-input --clear

RUN python manage.py migrate

# O comando para rodar a aplicação
CMD ["gunicorn", "combio.wsgi:application", "-b", "0.0.0.0:8000", "--workers", "4"]