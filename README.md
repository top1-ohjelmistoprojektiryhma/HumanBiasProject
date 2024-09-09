[![GHA workflow badge](https://github.com/top1-ohjelmistoprojektiryhma/HumanBiasProject/actions/workflows/main.yml/badge.svg)](https://github.com/top1-ohjelmistoprojektiryhma/HumanBiasProject/actions/workflows/main.yml)

# Dokumentaatio:

## Definition of Done
- User story toimii kuvauksen mukaisesti.
- Pylint score vähintään (9.00).
- Dokumentaatio suomeksi ja koodi englanniksi.
- Docstring-kommentointi kaikkeen.
- Koodi on luettavaa.
- Testikattavuus 70% ja testit menee läpi.
- Toimii tuotantoympäristössä.

## Riippuvuudet
Tarvittava Python versio:
```bash
python-versions = "^3.8"
```
Asenna Poetry:
```bash
pip install poetry
```
Jos node.js ei ole asennettuna, asenna sen uusin versio 20.17.0:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 20

```

# Käynnistysohjeet

Siirry projektin juurihakemistoon

Luo virtuaaliympäristö sovellusta varten
```bash
python3 -m venv venv
```
Aktivoi virtuaaliympäristö (MacOs, Linux)
```bash
source venv/bin/activate
```

Aja
```bash
python src/main.py
```

Siirry kansioon ```src/ui```

Asenna riippuvuudet
```bash
poetry install
```
```bash
npm install
```
Käynnistä sovellus
```bash
npm start
```
## Pylint

Pylintin voi ajaa komennolla
```bash
poetry run pylint src
```
