import asyncio
import json
import logging

from aiohttp.client import ClientSession

from poke_api.lib.types import PokemonAbilityResponse, PokemonAbilityPayload
from poke_api.db.postgres import postgres

async def connect() -> None:
    """Connect to postgres DB."""
    logging.info("Connecting to the DB")
    dbs = []
    if not postgres._pool:
        dbs.append(postgres._connect())
    await asyncio.gather(*dbs)

async def get_ability(payload: PokemonAbilityPayload) -> PokemonAbilityResponse:
    """Get ability from Pokemon API and store the data to postgre DB"""
    # Get the data from Pokemon API
    url = f"https://pokeapi.co/api/v2/ability/{payload.pokemon_ability_id}"
    async with ClientSession() as session:
        logging.info(f"Get request to {url}")
        async with session.get(url) as res:
            if not res.ok:
                raise ConnectionError(
                    f"{res.status}: Failed connecting to Pokemon API: {res.reason}"
                    f"\nRequest url: {url}"
                )
            data = await res.json()

    result = PokemonAbilityResponse(
        loan_id=payload.loan_id,
        user_id=payload.user_id,
        returned_entries=data["effect_entries"],
        pokemon_list=[x["pokemon"]["name"] for x in data["pokemon"]]
    )

    # Inserting row to DB
    data = []
    for entry in result.returned_entries:
        value = (result.loan_id, result.user_id, payload.pokemon_ability_id, entry.effect, json.dumps(entry.language), entry.short_effect)
        data.append(value)
    err_insert = await postgres.insert_row(tuple(data))
    if err_insert:
        raise err_insert
    
    return result
