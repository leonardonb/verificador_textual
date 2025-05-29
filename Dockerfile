# Imagem base com Python
FROM python:3.10-slim

# Instalações essenciais
RUN apt-get update && apt-get install -y \
    build-essential \
    graphviz \
    poppler-utils \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório da aplicação
WORKDIR /app

# Copia os arquivos da aplicação
COPY . .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando para rodar a aplicação Flask
CMD ["python", "app.py"]
