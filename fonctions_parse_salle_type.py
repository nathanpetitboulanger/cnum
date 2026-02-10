def parse_profs(text: str) -> list[str] | None:
    bracket_match = re.search(r"\(([^a-z]+)\)", text)
    if bracket_match:
        content = bracket_match.group(1)
        initiales = re.findall(r"[A-Z]{2}", content)
        return initiales
    else:
        return


import re


def parse_room(text: str) -> str | None:
    """
    Extrait le nom de la salle situé entre crochets et ne conserve
    que les caractères en majuscules (et chiffres).
    """
    bracket_match = re.search(r"\[([^\]]+)\]", text)

    if bracket_match:
        content = bracket_match.group(1)
        room_parts = re.findall(r"[A-Z0-9]+", content)

        return "".join(room_parts) if room_parts else None

    return None


def parse_type_cours(text: str) -> str | None:
    """
    Extrait le type de cours (CM, TD, TP, etc.) situé entre guillemets
    et ne conserve que les caractères en majuscules.
    """
    # On cherche le contenu entre guillemets " "
    # [^"]+ capture tout ce qui n'est pas un guillemet fermant
    quote_match = re.search(r"\"([^\"]+)\"", text)

    if quote_match:
        content = quote_match.group(1)
        # On ne récupère que les lettres majuscules (A-Z)
        # Cela permet d'ignorer les espaces ou minuscules accidentelles
        type_parts = re.findall(r"[A-Z]+", content)

        return "".join(type_parts) if type_parts else None

    return None


print(parse_type_cours('Séance de "TD"'))  # Sortie: "TD"
print(parse_type_cours('Cours magistral " CM "'))  # Sortie: "CM"
print(parse_type_cours('Format "td spécial"'))  # Sortie: None (car pas de majuscules)
