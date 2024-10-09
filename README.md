## Requirements
- Python 3.9
- PostgresSQL 16
- Redis 


## Install
Install Poetry - Tool for dependency management and packaging in Python

```
poetry install
poetry shell
```

```
alembic stamp head
alembic revision --autogenerate -m "update db" 
alembic upgrade head
```

```
sh start.sh
```
