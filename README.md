# Network Scanner

Scanner LAN sviluppato in Python con Flask e Nmap.

## Requisiti

* Python 3.11+
* Nmap installato e disponibile nel PATH

## Installazione

Clonare il repository:

git clone https://github.com/TUO_USERNAME/network-scanner.git

Entrare nella cartella:

cd network-scanner

Creare l'ambiente virtuale:

python -m venv .venv

Attivare l'ambiente virtuale:

Windows:

.venv\Scripts\activate

Linux/Mac:

source .venv/bin/activate

Installare le dipendenze:

pip install -r requirements.txt

Avviare il server:

python app.py

Aprire il browser:

http://127.0.0.1:5000

Premere "Scansiona rete" per rilevare i dispositivi presenti nella LAN locale.
