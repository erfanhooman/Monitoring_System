import json
import os
import logging
from jsonschema import validate, ValidationError

logger = logging.getLogger("ms")

SCHEMA = {
    "type": "object",
    "patternProperties": {
        # Match any key (e.g., "system.cpu.num" or "system.cpu.load[all,avg15]")
        ".*": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "value": {
                    "type": "object",
                    "properties": {
                        "normal": {"type": "number"},
                        "warning": {"type": "number"}
                    },
                    "required": ["normal", "warning"],
                    "additionalProperties": False
                },
                "recommendations": {
                    "type": "object",
                    "properties": {
                        "normal": {"type": "string"},
                        "warning": {"type": "string"},
                        "critical": {"type": "string"}
                    },
                    "required": ["normal", "warning", "critical"],
                    "additionalProperties": False
                }
            },
            "required": ["name", "description"],
            "anyOf": [
                {"required": ["value", "recommendations"]},  # Type 2
                {}  # Type 1 (no additional fields)
            ],
            "additionalProperties": False
        }
    },
    "additionalProperties": False
}

def validate_json_config(config_data):
    try:
        validate(instance=config_data, schema=SCHEMA)
        return True
    except ValidationError as e:
        logger.error("JSON schema validation failed")
        return False