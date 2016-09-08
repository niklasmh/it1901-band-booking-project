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

## Contributors

* Christoffer Almankaas
* Petter Bemelmans
* Embrik Einang
* Baldur Kjelsvik
* Odd Kristian Kvarmestøl
* Ingrid Medalen
* Niklas Molnes Hole

