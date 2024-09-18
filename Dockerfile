# TÄMÄ ON KESKEN JA VIRHEELLINEN

# Valitse pohjaksi Node.js ympäristö
FROM node:16

# Asenna Python ja muut tarvittavat paketit
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv curl

# Asenna Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Kopioi Node.js (frontend) -sovellus ja asenna riippuvuudet
WORKDIR /src/ui
COPY ui/package*.json ./
RUN npm install

# Kopioi Python (backend) -sovellus ja asenna riippuvuudet
WORKDIR .

# Kopioi Poetry-tiedostot
COPY ./pyproject.toml backend/poetry.lock ./

# Asenna riippuvuudet ilman virtuaaliympäristöä
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Kopioi muu Python-projekti
COPY src/ ./

# Voit määritellä miten molemmat palvelut ajetaan (esim. taustaprosessit tai erilliset kontit)
