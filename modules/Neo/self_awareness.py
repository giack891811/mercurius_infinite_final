"""Modulo per tracciare stati interni, scopi e operazioni in corso."""

self_state = {"active_task": None, "last_reflection": None}

def update_state(task):
    self_state["active_task"] = task

def get_current_state():
    return self_state