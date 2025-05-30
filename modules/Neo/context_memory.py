"""Memoria contestuale temporanea, per analisi conversazioni recenti."""

context_stack = []

def add_context(fragment):
    context_stack.append(fragment)
    if len(context_stack) > 20:
        context_stack.pop(0)

def get_recent_context():
    return context_stack[-5:]