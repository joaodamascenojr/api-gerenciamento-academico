import os
import sys
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context

# Permite importar o pacote "app" que está dentro de src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import models  # noqa: F401  (registra as tabelas no Base.metadata)
from app.db.session import Base

# Carrega as variáveis do ficheiro .env situado na raiz
load_dotenv()

# Objeto de configuração do Alembic (lê o alembic.ini)
config = context.config

# Injeta a URL da base de dados do .env na configuração do Alembic
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Configuração de logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadados usados pelo --autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Executa as migrações em modo 'offline' (gera só o SQL)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executa as migrações em modo 'online' (conectado ao banco)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
