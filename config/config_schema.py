"""Schema di validazione per config.yaml."""

CONFIG_SCHEMA = {
    "agents": {
        "type": "dict",
        "schema": {
            "enabled": {"type": "list", "schema": {"type": "string"}},
        },
    },
    "communication": {
        "type": "dict",
        "schema": {
            "feedback_loop": {"type": "boolean"},
            "max_retries": {"type": "integer", "min": 0},
            "retry_delay": {"type": "integer", "min": 0},
            "update_cycle_seconds": {"type": "integer", "min": 1},
        },
    },
    "mission_defaults": {
        "type": "dict",
        "schema": {
            "run_mode": {"type": "string"},
            "tasks": {"type": "list", "schema": {"type": "string"}},
        },
    },
    "paths": {
        "type": "dict",
        "schema": {
            "transcripts": {"type": "string"},
            "logs": {"type": "string"},
        },
    },
    "api_keys": {
        "required": False,
        "type": "dict",
        "schema": {"openai": {"type": "string"}},
    },
}
