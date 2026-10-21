
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
