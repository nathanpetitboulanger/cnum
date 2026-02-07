import unittest
from src.utils.functions import parse_profs, clean_cours_name


class TestExtraction(unittest.TestCase):
    def test_parse_profs(self):
        """
        Tests the extraction of professor initials from a course string.
        """
        # Case 1: Standard case with initials in parentheses
        text1 = "Analyse de données (ML-CF)"
        self.assertEqual(parse_profs(text1), ["ML", "CF"])

        # Case 2: No initials
        text2 = "Analyse de données"
        self.assertEqual(parse_profs(text2), [])

        # Case 3: Only initials, no space
        text3 = "Maths (BP)"
        self.assertEqual(parse_profs(text3), ["BP"])

        # Case 4: Multiple spaces
        text4 = "Cours de test (  YG   DS  )"
        self.assertEqual(parse_profs(text4), ["YG", "DS"])

        # Case 5: Empty string
        text5 = ""
        self.assertEqual(parse_profs(text5), [])

        # Case 6: String with only parentheses
        text6 = "()"
        self.assertEqual(parse_profs(text6), [])

    def test_clean_cours_name(self):
        """
        Tests the cleaning of the course name by removing professor initials.
        """
        # Case 1: Standard case
        text1 = "Analyse de données (ML-CF)"
        self.assertEqual(clean_cours_name(text1), "Analyse de données")

        # Case 2: No initials to clean
        text2 = "Analyse de données"
        self.assertEqual(clean_cours_name(text2), "Analyse de données")

        # Case 3: Extra spacing
        text3 = "  Maths avancées   (BP)  "
        self.assertEqual(clean_cours_name(text3), "Maths avancées")

        # Case 4: Empty string
        text4 = ""
        self.assertEqual(clean_cours_name(text4), "")

        # Case 5: String with only initials
        text5 = "(YG-DS)"
        self.assertEqual(clean_cours_name(text5), "")


if __name__ == "__main__":
    unittest.main()
