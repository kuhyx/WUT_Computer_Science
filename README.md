# Projekt z ERSMS


## Backend

### budowanie i uruchamianie obrazu z bazą danych oraz serwerem:
docker compose up

### gadanie z endpointami

GET http://localhost:8090/ - testowy domowy

GET http://localhost:8090//api/v3/get/<string:username> - info o userach

GET http://localhost:8090//api/v3/get_movie/<int:movie_ID> - info o filmie

POST http://localhost:8090/api/v3/add/<string:oauth_ID>/<string:username> - dodawanie usera

GET http://localhost:8090/api/v3/ai/<string:oauth_ID> - wyciąganie rekomendacji od AI