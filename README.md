# Projekt z ERSMS


## Backend

### instalacja:
pip install -r requirements.txt

### budowanie i uruchamianie obrazu z bazą danych:
docker compose up (ewentualnie można też z GUI)

### uruchomienie:
(Z directory macierzystego)
python3 ai_front_connector/frontend_AI_connector.py

### gadanie z endpointami

GET http://localhost:8090/ - testowy domowy

GET http://localhost:8090//api/v3/get/<string:username> - info o userach

GET http://localhost:8090//api/v3/get_movie/<int:movie_ID> - info o filmie

POST http://localhost:8090/api/v3/add/<string:oauth_ID>/<string:username> - dodawanie usera

GET http://localhost:8090/api/v3/ai/<string:oauth_ID> - wyciąganie rekomendacji od AI