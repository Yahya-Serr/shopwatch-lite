
def est_repete(sig, vus):
    """Retourne True si le signal a déjà été vu, sinon l'ajoute à vus."""
    cle = (
        sig.date,
        sig.origine,
        sig.service,
        sig.categorie,
        sig.texte
    )

    if cle in vus:
        return True

    vus.add(cle)
    return False


def compter_incidents(sig, compteur):
    """Compte les incidents JOURNAL de gravité MAJEUR ou BLOQUANT."""
    if sig.categorie == "JOURNAL" and sig.gravite in ("MAJEUR", "BLOQUANT"):
        compteur[sig.service] = compteur.get(sig.service, 0) + 1
        return compteur[sig.service]

    return 0


def chercher_fiches(sig, base):
    """Retourne les conseils dont le mot-clé apparaît dans le texte."""
    texte = sig.texte.lower()
    resultats = []

    for mot_cle, conseil in base.items():
        if mot_cle.lower() in texte:
            resultats.append(conseil)

    return resultats


def evaluer(sig, nb_incidents=0):
    """Passe le niveau à BLOQUANT à partir de quatre incidents."""
    if nb_incidents >= 4:
        return "BLOQUANT"

    return sig.gravite
