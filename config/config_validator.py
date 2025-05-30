# config_validator.py
import yaml
from cerberus import Validator
from config.config_schema import CONFIG_SCHEMA

def load_and_validate_config(path="config/config.yaml"):
    with open(path) as f:
        config = yaml.safe_load(f)
    v = Validator(CONFIG_SCHEMA)
    if not v.validate(config):
        raise ValueError(v.errors)
    return config
