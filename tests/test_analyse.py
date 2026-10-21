
import unittest

from src.analyse import est_repete, compter_incidents
from src.contrat import Signal


def sig(categorie="JOURNAL", gravite="MAJEUR",
        texte="timeout passerelle apres 30s", service="paiement"):
    return Signal(
        "SH-0001",
        "2026-11-27T17:00:00Z",
        "PAIEMENT",
        service,
        "production",
        categorie,
        gravite,
        texte
    )


class TestAnalyse(unittest.TestCase):

    def test_repete(self):
        vus = set()

        self.assertFalse(est_repete(sig(), vus))
        self.assertTrue(est_repete(sig(), vus))

    def test_compter_incidents(self):
        compteur = {}

        self.assertEqual(compter_incidents(sig(), compteur), 1)
        self.assertEqual(compter_incidents(sig(), compteur), 2)
        self.assertEqual(compteur["paiement"], 2)

    def test_compter_incidents_ignore_autres_signaux(self):
        compteur = {}
        signal = sig(categorie="FAILLE", gravite="MAJEUR")

        self.assertEqual(compter_incidents(signal, compteur), 0)
        self.assertEqual(compteur, {})


    def test_chercher_fiches(self):
        signal = sig(texte="Timeout pendant le BUILD")
        base = {
            "timeout": "Conseil timeout",
            "build": "Conseil build",
            "faille": "Conseil faille"
        }

        self.assertEqual(
            chercher_fiches(signal, base),
            ["Conseil timeout", "Conseil build"]
        )


    def test_evaluer_panne_en_boucle(self):
        signal = sig()

        self.assertEqual(evaluer(signal, 4), "BLOQUANT")
        self.assertEqual(evaluer(signal, 3), "MAJEUR")

    def test_evaluer_gravite_existante(self):
        signal = sig(gravite="MINEUR")

        self.assertEqual(evaluer(signal), "MINEUR")


    def test_diagnostiquer_faille(self):
        signal = sig(
            categorie="FAILLE",
            gravite="MAJEUR",
            texte="faille detectee",
            service="catalogue"
        )

        diagnostic = diagnostiquer(signal, {"faille": "Mettre a jour"})

        self.assertEqual(diagnostic.niveau, "MAJEUR")
        self.assertEqual(diagnostic.cause, "Mettre a jour")
        self.assertEqual(diagnostic.action, "Corriger la dependance catalogue")
        self.assertFalse(diagnostic.critique)
        self.assertEqual(diagnostic.origines, ["PAIEMENT"])
        self.assertEqual(signal.etat, "EVALUE")

    def test_diagnostiquer_service_bloquant(self):
        signal = sig(texte="probleme inconnu", service="paiement")

        diagnostic = diagnostiquer(signal, {}, nb_incidents=4)

        self.assertEqual(diagnostic.niveau, "BLOQUANT")
        self.assertEqual(
            diagnostic.cause,
            "Cause inconnue : verification manuelle"
        )
        self.assertEqual(diagnostic.action, "Isoler le service paiement")
        self.assertTrue(diagnostic.critique)

    def test_diagnostiquer_build(self):
        signal = sig(categorie="BUILD_ECHEC", service="catalogue")

        diagnostic = diagnostiquer(signal, {})

        self.assertEqual(diagnostic.action, "Rejouer le build catalogue")


if __name__ == "__main__":
    unittest.main()
