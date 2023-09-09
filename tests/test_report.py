import unittest

from log_analyzer.report.report import parse_line


class ReportGenerationTest(unittest.TestCase):
    def test_invalid_log_record(self):
        result = parse_line('WRONG FMT')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
