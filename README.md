# Projekt z ERSMS


## Backend

### budowanie i uruchamianie obrazu z bazą danych oraz serwerem:
docker compose up

w przypadku zmian w bazie danych, usunąć kontener oraz dołączone do niego volumy

### stronka administracyjna do bazy danych

Najpierw wpisujemy w przeglądarce http://localhost:8080/
Przy logowaniu wpisujemy:
* login - admin@admin.com 
* hasło - admin

Po zalogowaniu się poraz pierwszy od zbudowania obrazu, widzimy stronę główną. Klikamy na niej duży przycisk "Add New Server" i pojawia się okienko z menu dodawania serwera.

W nazwie można napisać cokolwiek, jednak w zakładce "Connection" piszemy następujące rzeczy:
* host name - db
* login - root
* password - root

Reszta pozostaje jak była. Po zapisaniu ustawień, mamy już dostęp do narzędzi administratora dla naszej bazy danych.

### gadanie z endpointami

GET http://localhost:8090/ - testowy domowy

GET http://localhost:8090//api/v3/get/<string:username> - info o userach

GET http://localhost:8090//api/v3/get_movie/<int:movie_ID> - info o filmie

POST http://localhost:8090/api/v3/add/<string:oauth_ID>/<string:username> - dodawanie usera

POST http://localhost:8090/api/v3/add/<string:oauth_ID>/<string:movie_ID>/<int:rating> - dodawanie oceny do filmu przez usera

GET http://localhost:8090/api/v3/ai/<string:oauth_ID> - wyciąganie rekomendacji od AI