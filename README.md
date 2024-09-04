# Dokumentaatio:

## Definition of Done
- User story toimii kuvauksen mukaisesti.
- Pylint score vähintään (9.00).
- Dokumentaatio suomeksi ja koodi englanniksi.
- Docstring-kommentointi kaikkeen.
- Koodi on luettavaa.
- Testikattavuus 70% ja testit menee läpi.
- Toimii tuotantoympäristössä.

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
