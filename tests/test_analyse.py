
import unittest

from src.analyse import est_repete
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


if __name__ == "__main__":
    unittest.main()
