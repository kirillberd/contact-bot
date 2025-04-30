import asyncpg
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="postgres_")
    user: str
    password: str
    dbname: str
    host: str
    port: int = 5432

    @property
    def dsn(self):
        user_escaped = quote_plus(self.user)
        password_escaped = quote_plus(self.password)
        return f"postgres://{user_escaped}:{password_escaped}@{self.host}:{self.port}/{self.dbname}"


class PostgresClient:
    def __init__(self, table_name: str = ""):
        self._settings = PostgresSettings()
        self._table_name = table_name
        self._pool = None

    async def _ensure_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(self._settings.dsn)
            print("Connection to PostgreSQL established")

    async def add_data(self, data: dict):
        await self._ensure_pool()
        async with self._pool.acquire() as conn:
            columns = data.keys()
            placeholders = ", ".join([f"${i+1}" for i in range(len(data))])
            query = f"INSERT INTO {self._table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            await conn.execute(query, *data.values())

    async def add_data_list(self, data: List[dict]):
        if not data:
            return
        await self._ensure_pool()
        columns = data[0].keys()
        for d in data[1:]:
            if d.keys() != columns:
                raise ValueError("All dictionaries must have the same keys")
        values = [tuple(d.values()) for d in data]
        async with self._pool.acquire() as conn:
            placeholders = ", ".join([f"${i+1}" for i in range(len(columns))])
            query = f"INSERT INTO {self._table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            await conn.executemany(query, values)

    async def get_data(self):
        await self._ensure_pool()
        async with self._pool.acquire() as conn:
            query = f"SELECT name, email, tags, notes, region FROM {self._table_name}"
            rows = await conn.fetch(query)
            return [dict(row) for row in rows]

    async def close(self):
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
