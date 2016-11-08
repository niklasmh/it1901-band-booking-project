Band Booking
============

Group 5 project for IT1901.

## Setup

Installèr python v3 og klon repo med `git clone https://github.com/okknor/band_booking.git`.

```bash
$ cd band_booking/ # Gå inn i mappen.
$ sudo pip3 install virtualenv # Hent virtualenv fra python pakke.
$ virtualenv env # Lag et virtuelt miljø.
$ source env/bin/activate # Aktivere virtualenv.
$ pip install requests # Installere pakker til miljøet.
$ pip install -r requirements.txt # Installerer avhengigheter til prosjektet.
$ cp doc/settings_local.dev.py band_booking/settings_local.py # Setter instillinger for et utviklingsmiljø (for windows erstatt cp med copy)
$ python manage.py migrate
$ python manage.py createsuperuser # Følg instruksjonene.
```

Nå er alt satt opp. For å gå ut:

```bash
$ deactivate
```

## Run

I mappen til prosjektet:

```bash
$ source env/bin/activate # For å aktivere.
$ python manage.py runserver 0.0.0.0:8000 # Dette er den lokale serveren på http://localhost:8000
```

Så for å avslutte:

```bash
$ deactivate # For å deaktivere.
```

## API
Systemet bruker et API (Application Programming Interface) over HTTP/HTTPS slik at utviklere kan få tak i informasjon fra databasen, uavhengig av teknologi. Av sikkerhetsgrunner trenger man en sessionid-cookie for å både hente og legge inn data. Kallene vi har åpnet for i API'et er skrevet under. Om flere kall trengs senere kan man ta kontakt med system-administratorene. Systemet returnerer bare JSON-format foreløpig.

#### API kall

`GET /band/:[id|navn]`

Gir ut data om band basert på enten id eller navn på band.

`GET /venue/:id`

Gir ut en venue basert på id.

## Contributors

* Baldur Kjelsvik
* Christoffer Almankaas
* Embrik Einang
* Ingrid Medalen
* Niklas Molnes Hole
* Odd Kristian Kvarmestøl
* Petter Bemelmans
