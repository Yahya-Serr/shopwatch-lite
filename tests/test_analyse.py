
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


if __name__ == "__main__":
    unittest.main()
