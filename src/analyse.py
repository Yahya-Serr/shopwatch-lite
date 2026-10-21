
from src.contrat import Diagnostic


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


def diagnostiquer(sig, base, nb_incidents=0):
    """Construit un diagnostic à partir d'un signal et des fiches."""
    niveau = evaluer(sig, nb_incidents)
    fiches = chercher_fiches(sig, base)

    if fiches:
        cause = " ; ".join(fiches)
    else:
        cause = "Cause inconnue : verification manuelle"

    if sig.categorie == "FAILLE":
        action = f"Corriger la dependance {sig.service}"
    elif sig.categorie == "BUILD_ECHEC":
        action = f"Rejouer le build {sig.service}"
    elif niveau == "BLOQUANT":
        action = f"Isoler le service {sig.service}"
    else:
        action = "Observer"

    critique = action.startswith("Isoler")

    diagnostic = Diagnostic(
        sig.ref,
        niveau,
        cause,
        action,
        critique,
        [sig.origine]
    )

    sig.etat = "EVALUE"

    return diagnostic
