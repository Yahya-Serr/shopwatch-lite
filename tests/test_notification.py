import unittest
from src.contrat import Diagnostic, Signal
from src.notification import approuver, choisir_canal

def exemple(critique=True, niveau="BLOQUANT"):
    s = Signal("SH-0125", "2026-11-27T17:02:11Z", "PAIEMENT", "paiement",
               "production", "JOURNAL", "MAJEUR", "timeout passerelle apres 30s")
    d = Diagnostic("SH-0125", niveau, "Passerelle lente",
                   "Isoler le service paiement", critique, ["PAIEMENT"])
    return s, d

class TestNotification(unittest.TestCase):
    def test_canaux(self):
        self.assertEqual(choisir_canal("BLOQUANT"), "SLACK")
        self.assertEqual(choisir_canal("MINEUR"), "TABLEAU")

    def test_approbation(self):
        _, d = exemple()
        self.assertTrue(approuver(d, " OUI "))
        self.assertFalse(approuver(d, "n"))