import pytest
import pandas as pd
from unittest.mock import patch
from main import (
    main,
    benford_distribution,
    first_digit,
    occurrence_count,
    percentage_of_total,
    draw_histogram,
)
from extras.checkers import file_exists, list_datasource_files, data_load, extension_checker


class TestBenfordDistribution:
    def test_returns_nine_values(self):
        assert len(benford_distribution()) == 9

    def test_sums_to_100(self):
        assert abs(sum(benford_distribution()) - 100) < 0.001

    def test_first_digit_probability(self):
        # P(d=1) = log10(2) ≈ 30.1%
        assert abs(benford_distribution()[0] - 30.103) < 0.001

    def test_decreasing_probabilities(self):
        b = benford_distribution()
        assert all(b[i] > b[i + 1] for i in range(len(b) - 1))


class TestFirstDigit:
    def test_integers(self):
        assert first_digit(1) == 1
        assert first_digit(5) == 5
        assert first_digit(123) == 1
        assert first_digit(999999) == 9

    def test_floats(self):
        assert first_digit(3.7) == 3
        assert first_digit(9.999) == 9
        assert first_digit(1.0001) == 1

    def test_numpy_scalar(self):
        import numpy as np
        assert first_digit(np.float64(4.5)) == 4
        assert first_digit(np.int64(7)) == 7


class TestOccurrenceCount:
    def test_always_returns_nine_values(self):
        assert len(occurrence_count([1, 2, 3])) == 9

    def test_ordered_1_to_9(self):
        result = occurrence_count([1, 1, 2, 3])
        assert result[0] == 2  # digit 1
        assert result[1] == 1  # digit 2
        assert result[2] == 1  # digit 3
        assert result[3] == 0  # digit 4 — missing, should be 0

    def test_missing_digit_gets_zero(self):
        result = occurrence_count([1, 9])
        assert result[0] == 1  # digit 1
        assert result[7] == 0  # digit 8 — missing
        assert result[8] == 1  # digit 9


class TestPercentageOfTotal:
    def test_equal_split(self):
        result = percentage_of_total([1, 1, 1, 1])
        assert all(abs(x - 25.0) < 0.001 for x in result)

    def test_sums_to_100(self):
        result = percentage_of_total([10, 20, 30, 40])
        assert abs(sum(result) - 100) < 0.001

    def test_proportions(self):
        result = percentage_of_total([1, 3])
        assert abs(result[0] - 25.0) < 0.001
        assert abs(result[1] - 75.0) < 0.001


class TestDrawHistogram:
    def test_renders_without_error(self):
        benford = benford_distribution()
        user_data = [100 / 9] * 9
        draw_histogram(benford, user_data)


class TestCheckers:
    def test_file_exists_true(self):
        path = data_load(extension_checker('hydrology_areas'))
        assert file_exists(path)

    def test_file_exists_false(self):
        path = data_load('nonexistent.csv')
        assert not file_exists(path)

    def test_list_datasource_files_returns_csvs(self):
        files = list_datasource_files()
        assert len(files) > 0
        assert all(f.endswith('.csv') for f in files)

    def test_list_datasource_files_is_sorted(self):
        files = list_datasource_files()
        assert files == sorted(files)


class TestMain:
    def test_returns_false_for_negative_values(self, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text("amount\n-100\n200\n300\n")
        with patch("builtins.input", return_value="amount"):
            result = main(str(csv))
        assert result is False

    def test_returns_true_for_valid_data(self, tmp_path):
        csv = tmp_path / "test.csv"
        csv.write_text("amount\n100\n200\n300\n150\n250\n120\n110\n320\n180\n")
        with patch("builtins.input", return_value="amount"):
            result = main(str(csv))
        assert result is True


class TestIntegration:
    def test_pipeline_with_dataframe(self):
        """End-to-end: extract first digits from a DataFrame column and compare distributions."""
        df = pd.DataFrame({"amount": [100, 200, 150, 300, 120, 250, 110, 320, 180]})
        df["first_d"] = df["amount"].apply(first_digit)
        digits = list(df["first_d"])
        digits = [d for d in digits if d != 0]

        counts = occurrence_count(digits)
        percentages = percentage_of_total(counts)

        assert abs(sum(percentages) - 100) < 0.001
        assert all(p >= 0 for p in percentages)
