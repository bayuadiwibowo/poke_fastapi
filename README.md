# Pokemon FastAPI
Simple API to get pokemon information. API will run in `8000` port.

# Instructions
## Build the image
```sh
docker compose build
```
## Run API and database
```sh
docker compose up -d
```
## Stop API and database
```sh
docker compose down
```

# API Contract
## Get Pokemon Ability
```sh
curl --location 'localhost:8000/api/v1/ability' \
--header 'Content-Type: application/json' \
--data '{
   "loan_id": "9594641568",
   "user_id": "5199434",
   "pokemon_ability_id": "150"
}'
```
## Get API Health Status
```sh
curl --location 'localhost:8000/health'
```
