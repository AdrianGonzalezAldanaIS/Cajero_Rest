import os
from models import tarjetas
from jsonschema import Draft7Validator
from json import load

with open('schema.json') as f:
    schema = load(f)



validador = Draft7Validator(schema)

print(list(validador.iter_errors(tarjetas)))









