# Auktionsseite

## Beschreibung
Dieses Projekt wurde im Rahmen meines Online-Kurses mit Zertifikat **[CS50’s Web Programming with Python and JavaScript](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript)** erstellt.
Es handelt sich um eine eBay-ähnliche Auktionsseite, welche es Nutzern erlaubt, Autkionen zu erstellen, Produkte auf eine Beobachtungsliste zu setzen und Gebote auf Produkte zu setzen und diese zu kommentieren.

## Link zur Website
https://auction-django.herokuapp.com/

## Django-Projekt lokal starten
- Im Root Verzeichnis folgenden Befehl eingeben:
  -`python .\manage.py runserver`
- vorgefertigter Account zum Testen:
  - Username: test
  - Password: 123456

## Struktur
Das Projekt ist ein reines Django-Projekt und besitzt eine Django-App namens auctions in der die Views, Templates und Models erstellt wurden. 
Es gibt 4 verschiedene Models:
- User: für Authentifizierung
- Listing: um die Informationen über die angebotenen Produkte zu speichern (z.B. Startpreis, Besitzer, Kategorie, ...)
- Bid: für die Speicherung der Daten der Gebote (wie Bieter, Gebotspreis, zugehöriges Produkt)
- Comment: für Speicherung der Kommentare

## Vorführung
[![Project Showcase](https://i.ibb.co/vvvT7B1/commerce.png)](https://youtu.be/Od2tL7d0JGs)
