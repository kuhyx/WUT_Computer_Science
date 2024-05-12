# instalacja:
pip install -r requirements.txt

# uruchomienie:
(Z directory macierzystego)

python3 ai_front_connector/frontend_AI_connector.py

# gadanie z endpointami

GET http://localhost:8080/ - testowy domowy

GET http://localhost:8080//api/v3/get/<string:username> - info o userach

POST http://localhost:8080/api/v3/add/<string:oauth_ID>/<string:username> - dodawanie usera

GET http://localhost:8080/api/v3/ai/<string:oauth_ID> - wyciąganie rekomendacji od AI

