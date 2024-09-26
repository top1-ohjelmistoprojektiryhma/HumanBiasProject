[![GHA workflow badge](https://github.com/top1-ohjelmistoprojektiryhma/HumanBiasProject/actions/workflows/main.yml/badge.svg)](https://github.com/top1-ohjelmistoprojektiryhma/HumanBiasProject/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/top1-ohjelmistoprojektiryhma/HumanBiasProject/graph/badge.svg?token=6QQXK7UA5D)](https://codecov.io/gh/top1-ohjelmistoprojektiryhma/HumanBiasProject)

# Dokumentaatio:

## Backlogit
- [Product ja Sprint backlog](https://docs.google.com/spreadsheets/d/1MgSFmB2FVtgCejguAnvmcLbdJNIUZ8DQazVcVI62wbg/edit?usp=sharing)
  
## Definition of Done
- User story toimii kuvauksen mukaisesti.
- Pylint score vähintään (9.00).
- Dokumentaatio suomeksi ja koodi englanniksi.
- Docstring-kommentointi kaikkeen.
- Koodi on luettavaa.
- Testikattavuus 70% ja testit menee läpi. Web-käyttöliittymää testataan vain manuaalisesti.
- Toimii tuotantoympäristössä.

## Riippuvuudet
Tarvittava Python versio:
```bash
python-versions = "^3.9"
```
Asenna Poetry:
```bash
pip install poetry
```
Jos node.js ei ole asennettuna, asenna sen uusin versio 20.17.0 (MacOs, Linux):
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 20

```
# Asennusohjeet

Siirry projektin juurihakemistoon

Luo tiedosto ```.env``` **_ja_** määritä se muotoon
```
GEMINI_KEY=<gemini-api-key>
OPEN_AI_KEY=<openai-api-key>
ANTHROPIC-KEY=<anthropic-api-key>
```

Luo virtuaaliympäristö sovellusta varten
```bash
python3 -m venv venv
```
Aktivoi virtuaaliympäristö (MacOs, Linux)
```bash
source venv/bin/activate
```
Asenna riippuvuudet
```bash
poetry install
```

Siirry kansiion ```src/ui```
```bash
npm install
```

# Käynnistysohjeet
## Käynnistäminen poetry-taskilla
Avaa kaksi terminaalia, joilla siirryt projektin juurihakemistoon.
Aja toisessa terminaalissa komento
```bash
poetry run invoke backend
```
Ja toisessa terminaalissa komento
```bash
poetry run invoke frontend
```

## Vaihtoehtoinen käynnistystapa:

Siirry projektin juurihakemistoon

Aktivoi virtuaaliympäristö (MacOs, Linux)
```bash
source venv/bin/activate
```

Käynnistä backend
```bash
python3 src/main.py
```

Avaa toinen terminaali/välilehti
Siirry toisessa terminaalissa kansioon ```src/ui```

Käynnistä sovellus
```bash
npm start
```

## Testit ja pylint

Pylintin voi ajaa komennolla
```bash
poetry run invoke lint
```

Testit komennolla
```bash
poetry run invoke test
```

Testikattavuuden komennolla
```bash
poetry run invoke coverage
```
Kattavuusraportti tulostuu komentoriville ja selainversio muodostuu kansioon _htmlcov_
