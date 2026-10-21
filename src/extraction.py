import re
from src.contrat import Signal

def masquer_donnees(texte: str) -> str:
    # Masquage des clés spécifiques (insensible à la casse) : password, pwd, token, secret, card, iban[cite: 3]
    # Format nom=valeur ou nom: valeur jusqu'au séparateur d'arrêt[cite: 3]
    pattern_cles = r'(?i)\b(password|pwd|token|secret|card|iban)([:=])\s*([^&\s,;]+)'
    texte_masque = re.sub(pattern_cles, r'\1\2[MASQUE]', texte)
    
    # Masquage spécifique du jeton Bearer (hotfix de l'exercice 5)[cite: 15]
    pattern_bearer = r'(?i)\b(Bearer)\s+([^&\s,;]+)'
    texte_masque = re.sub(pattern_bearer, r'\1 [MASQUE]', texte_masque)
    
    return texte_masque

def lire_journal(ligne: str, numero: int, origine: str = "PAIEMENT", env: str = "production") -> Signal:
    champs = ligne.split(" ", 4)
    if len(champs) < 5:
        raise ValueError("La ligne de journal doit contenir au moins 5 champs.") #[cite: 3]
        
    date_str = f"{champs[0]}T{champs[1]}Z" #[cite: 3]
    service = champs[2]
    niveau = champs[3].upper()
    texte_brut = champs[4]
    
    # Évaluation de la gravité[cite: 3]
    if niveau in ("FATAL", "CRITICAL"):
        gravite = "BLOQUANT"
    elif niveau == "ERROR":
        gravite = "MAJEUR"
    elif niveau in ("WARN", "WARNING"):
        gravite = "MODERE"
    else:
        gravite = "MINEUR"
        
    ref = f"SH-{numero:04d}" #[cite: 3]
    texte_securise = masquer_donnees(texte_brut) #[cite: 3]
    
    return Signal(ref=ref, date=date_str, origine=origine, service=service, 
                  env=env, categorie="JOURNAL", gravite=gravite, texte=texte_securise)

def lire_scan(rapport: dict, numero: int, env: str = "production") -> Signal:
    cles_requises = {"id_faille", "paquet", "risque", "date"}
    if not cles_requises.issubset(rapport.keys()):
        raise ValueError("Clés manquantes dans le rapport de scan.") #[cite: 4]
        
    risque = rapport["risque"].lower()
    # Évaluation de la gravité[cite: 4]
    if risque == "critique":
        gravite = "BLOQUANT"
    elif risque == "haut":
        gravite = "MAJEUR"
    elif risque == "moyen":
        gravite = "MODERE"
    else:
        gravite = "MINEUR"
        
    ref = f"SH-{numero:04d}"
    texte = f"Faille {rapport['id_faille']} dans {rapport['paquet']}" #[cite: 4]
    
    return Signal(ref=ref, date=rapport["date"], origine="SCANNER", service=rapport["paquet"], 
                  env=env, categorie="FAILLE", gravite=gravite, texte=texte)

def lire_build(rapport: dict, numero: int, env: str = "production") -> Signal:
    cles_requises = {"etape", "resultat", "date"}
    if not cles_requises.issubset(rapport.keys()):
        raise ValueError("Clés manquantes dans le rapport de build.") #[cite: 4]
        
    resultat = rapport["resultat"].lower()
    # Évaluation de la catégorie et de la gravité[cite: 4]
    if resultat == "echec":
        categorie = "BUILD_ECHEC"
        gravite = "MAJEUR"
    else:
        categorie = "BUILD_OK"
        gravite = "MINEUR"
        
    ref = f"SH-{numero:04d}"
    texte = f"Build {rapport['etape']} {rapport['resultat']}" 
    
    return Signal(ref=ref, date=rapport["date"], origine="BUILD", service=rapport["etape"], 
                  env=env, categorie=categorie, gravite=gravite, texte=texte)