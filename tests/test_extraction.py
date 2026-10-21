import unittest

from src.extraction import masquer_donnees


class TestExtraction(unittest.TestCase):
    def test_bearer(self):
        self.assertEqual(
            masquer_donnees("Authorization: Bearer eyJ.abc-1"),
            "Authorization: Bearer [MASQUE]",
        )


if __name__ == "__main__":
    unittest.main()