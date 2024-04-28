import os
import yaml
import json


def load_application(prefix: str = './') -> dict:
    params = load_params(prefix=prefix)
    prompts = load_prompts(prefix=prefix)
    personas = load_personas(prefix=prefix)

    return {
        'config': params,
        'prompts': prompts,
        'personas': personas
    }


def load_params(path: str = 'params.yaml', prefix: str = './') -> dict:
    with open(f'{prefix}{path}') as f:
        return yaml.safe_load(f)


def load_prompts(folder: str = 'src/prompts', prefix: str = './') -> dict:
    prompts = {}
    full_path = f'{prefix}{folder}'
    for file in os.listdir(full_path):
        if file.endswith('.prompt'):
            with open(f'{full_path}/{file}') as f:
                name = file.split('.')[0]
                prompts[name] = f.read()
    return prompts


def load_personas(folder: str = 'src/personas', prefix: str = './') -> dict:
    personas = {}
    full_path = f'{prefix}{folder}'
    for file in os.listdir(full_path):
        if file.endswith('.json'):
            with open(f'{full_path}/{file}') as f:
                name = file.split('.')[0]
                personas[name] = json.load(f)
    return personas
