"""Migliora risposte ed elaborazioni sulla base di feedback osservato."""

def refine_response(raw, feedback):
    if "troppo complesso" in feedback:
        return "Versione semplificata: " + raw[:50]
    return raw