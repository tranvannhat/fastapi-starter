#! /usr/bin/env bash

# Let the DB start
uvicorn app.main:app --reload