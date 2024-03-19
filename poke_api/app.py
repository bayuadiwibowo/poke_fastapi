import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from poke_api.lib.types import TestResponse, PokemonAbilityResponse, PokemonAbilityPayload
from poke_api.usecase import pokemon


# Setup
logging.basicConfig(
    filename=f"/tmp/poke_api.log",
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)
app = FastAPI(redoc_url=None, docs_url=None)

# Exception Handler
@app.exception_handler(Exception)
async def value_error_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Middleware for handling returned exceptions."""
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": str(exc)
        }
    )

# Main Routes
@app.get("/health", response_model=TestResponse)
async def test() -> TestResponse:
    """This is the test function, use this to check if the server is indeed running."""
    logging.info("Running health endpoint")
    return TestResponse()

@app.post("/api/v1/ability", response_model=PokemonAbilityResponse)
async def get_ability(payload: PokemonAbilityPayload) -> PokemonAbilityResponse:
    """This function will get the ability from Pokemon API, return to user and store to DB."""
    logging.info("Start to get pokemon ability")
    await pokemon.connect()
    abilities = await pokemon.get_ability(payload)
    return abilities

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
