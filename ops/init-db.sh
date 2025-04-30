#!/bin/bash
set -e


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO
    \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'postgres') THEN
            CREATE ROLE postgres WITH LOGIN SUPERUSER PASSWORD '${POSTGRES_PASSWORD}';
        END IF;
    END
    \$\$;
EOSQL

