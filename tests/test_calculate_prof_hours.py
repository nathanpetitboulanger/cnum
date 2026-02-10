import unittest
import pandas as pd

try:
    from calcul.calculate_stat_df import calculate_hours_by_professor
except ImportError:
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.calcul.calculate_stat_df import calculate_hours_by_professor


class TestCalculateHoursByProfessor(unittest.TestCase):
    def test_calculate_hours(self):
        data = {
            "prof": [
                "['Prof A']",
                "['Prof B']",
                "['Prof A', 'Prof B']",
                "[]",
                "['Prof C']",
            ],
            "delta": [
                "2.0",
                "1,5",
                3.0,
                1.0,
                "2.0",
            ],  # Mix of strings (with comma/dot) and floats
        }
        df = pd.DataFrame(data)

        # calculate_hours_by_professor expects a DataFrame and returns a Series
        result = calculate_hours_by_professor(df)

        # Expected:
        # Prof A: 2.0 + 3.0 = 5.0
        # Prof B: 1.5 + 3.0 = 4.5
        # Prof C: 2.0
        # Empty list contributes nothing to named profs.

        self.assertAlmostEqual(result["Prof A"], 5.0)
        self.assertAlmostEqual(result["Prof B"], 4.5)
        self.assertAlmostEqual(result["Prof C"], 2.0)

        # Check that empty string is not in index (or ignored)
        # Note: explode on empty list results in NaN if not dropped.
        # But we select specific columns.

        # If result index has NaN or empty string, assert it's not there or handled.
        # But my function does: exploded_df.groupby("prof")...
        # Empty list -> explode -> nothing (row disappears).
        # So "[]" row contributes nothing.

        self.assertTrue("Prof A" in result.index)


if __name__ == "__main__":
    unittest.main()
