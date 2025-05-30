"""Gestione adattiva dello stile comunicativo."""

user_profile = {"tone": "neutro", "style": "tecnico"}

def set_style(tone, style):
    user_profile["tone"] = tone
    user_profile["style"] = style

def get_style():
    return user_profile