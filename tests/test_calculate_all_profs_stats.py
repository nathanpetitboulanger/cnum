import unittest
import pandas as pd
import sys
import os
from unittest.mock import MagicMock

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Mock utils.fetch_data before importing calcul.calculate_stat_df
mock_fetch_data = MagicMock()
mock_fetch_data.get_df_from_sheet_index.return_value = pd.DataFrame(
    {"prof": [], "delta": []}
)
sys.modules["utils.fetch_data"] = mock_fetch_data

# Now import the module to test
# We need to use importlib or just import it now that sys.modules has the mock
# But since we use 'from ... import ...', we need to make sure 'utils' is also mocked if it's a top level package
# The import in calculate_stat_df is 'from utils.fetch_data import get_df_from_sheet_index'
# So we need 'utils' in sys.modules too if it's not there, but usually mocking the leaf is enough if parent is not imported directly.
# Let's mock 'utils' as well to be safe.
mock_utils = MagicMock()
mock_utils.fetch_data = mock_fetch_data
sys.modules["utils"] = mock_utils

from calcul.calculate_stat_df import calculate_all_profs_stats


class TestCalculateAllProfsStats(unittest.TestCase):
    def test_simple_case(self):
        data = {"prof": ["Prof A", "Prof B", "Prof A"], "delta": ["1,5", "2", "3"]}
        df = pd.DataFrame(data)
        stats = calculate_all_profs_stats(df)

        # Check if index is correct (reset_index makes it 0, 1, ...)
        # Check values
        prof_a = stats[stats["prof"] == "Prof A"]["delta"].values[0]
        self.assertEqual(prof_a, 4.5)
        prof_b = stats[stats["prof"] == "Prof B"]["delta"].values[0]
        self.assertEqual(prof_b, 2.0)

    def test_comma_separated(self):
        data = {"prof": ["Prof A, Prof B", "Prof C"], "delta": ["2", "1"]}
        df = pd.DataFrame(data)
        stats = calculate_all_profs_stats(df)

        prof_a = stats[stats["prof"] == "Prof A"]["delta"].values[0]
        prof_b = stats[stats["prof"] == "Prof B"]["delta"].values[0]
        prof_c = stats[stats["prof"] == "Prof C"]["delta"].values[0]

        self.assertEqual(prof_a, 2.0)
        self.assertEqual(prof_b, 2.0)
        self.assertEqual(prof_c, 1.0)

    def test_comma_separated_with_spaces(self):
        data = {"prof": ["Prof A ,  Prof B"], "delta": ["2"]}
        df = pd.DataFrame(data)
        stats = calculate_all_profs_stats(df)

        prof_a = stats[stats["prof"] == "Prof A"]["delta"].values[0]
        prof_b = stats[stats["prof"] == "Prof B"]["delta"].values[0]

        self.assertEqual(prof_a, 2.0)
        self.assertEqual(prof_b, 2.0)

    def test_duplicate_prof_in_row(self):
        # Case where a prof is mentioned twice in the same entry
        data = {"prof": ["Prof A, Prof A", "Prof B"], "delta": ["2", "1"]}
        df = pd.DataFrame(data)
        stats = calculate_all_profs_stats(df)

        prof_a = stats[stats["prof"] == "Prof A"]["delta"].values[0]
        self.assertEqual(prof_a, 2.0)  # Should be 2.0, not 4.0

    def test_duplicate_columns(self):
        # Simulate duplicate columns which caused the crash
        data = {
            "prof": ["Prof A"],
            "delta": ["2"],
            "": ["dummy1"],
            " ": ["dummy2"],  # slight variation to avoid direct dict key collision
        }
        df = pd.DataFrame(data)
        # Force duplicate column names
        df.columns = ["prof", "delta", "", ""]

        # This should not raise ValueError
        stats = calculate_all_profs_stats(df)

        prof_a = stats[stats["prof"] == "Prof A"]["delta"].values[0]
        self.assertEqual(prof_a, 2.0)


if __name__ == "__main__":
    unittest.main()
