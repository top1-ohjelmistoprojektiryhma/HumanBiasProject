# Valitse pohjaksi Node.js ympäristö
FROM node:16

# Asenna Python ja muut tarvittavat paketit
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv curl
RUN npm install -g foreman


# Asenna Poetry
RUN pip3 install poetry

# Kopioi Node.js (frontend) -sovellus ja asenna riippuvuudet
WORKDIR /src/ui
COPY ui/package*.json ./
RUN npm install

# Kopioi Python (backend) -sovellus ja asenna riippuvuudet
WORKDIR /src/backend

# Kopioi Poetry-tiedostot
COPY pyproject.toml poetry.lock ./

# Asenna riippuvuudet ilman virtuaaliympäristöä
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Kopioi muu Python-projekti
COPY src/backend/ ./

# Voit määritellä miten molemmat palvelut ajetaan (esim. taustaprosessit tai erilliset kontit)
CMD ["nf", "start"]
