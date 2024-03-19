import logging
import os
from typing import Optional, Any

from asyncpg import Pool, create_pool


class Postgres:
    """Handle connection and interface with postgresql database"""

    def __init__(self) -> None:
        """Initialize a postgre database connection"""
        self._pool: Optional[Pool] = None

    async def _connect(self) -> None:
        """Connect to postgre database"""
        host = os.getenv("POSTGRES_HOST")
        user = os.getenv("POSTGRES_USER")
        passw = os.getenv("POSTGRES_PASSWORD")
        port = os.getenv("POSTGRES_PORT")
        database = os.getenv("POSTGRES_DB")

        logging.debug(f"Creating pool connection to host: {host}")
        self._pool = await create_pool(
            host=host,
            user=user,
            password=passw,
            port=port,
            database=database,
        )
    
    async def insert_row(self, values) -> Any:
        """Insert pokemon effect data to postgre database"""
        if not self._pool:
            err = "No connection pool to database found"
            logging.error(err)
            raise ConnectionError(err)

        async with self._pool.acquire() as connection:
            logging.info("Inserting data to DB")
            statement = """INSERT INTO 
                pokemon_effect (loan_id, user_id, pokemon_ability_id, effect, language, short_effect)
                VALUES($1, $2, $3, $4, $5, $6);"""
            try:
                await connection.executemany(statement, values)
            except Exception as e:
                return e

        return None

postgres = Postgres()
