import unittest

from log_analyzer.report.report import (
    URLStat,
    parse_line,
    prepare_stats,
    prepare_table,
)


class ReportGenerationTest(unittest.TestCase):
    def test_invalid_log_record(self):
        result = parse_line('WRONG FMT')
        self.assertIsNone(result)

    def test_valid_log_record(self):
        result = parse_line(
            '1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] '
            '"GET /api/v2/banner/16852664 HTTP/1.1" 200 19415 "-" '
            '"Slotovod" "-" "1498697422-2118016444-4708-9752769" '
            '"712e90144abee9" 0.199'
        )
        self.assertIsInstance(result, URLStat)
        self.assertEqual(result.url, '/api/v2/banner/16852664')
        self.assertEqual(result.request_time_sec, 0.199)

    def test_stats_generation(self):
        time_stats = [1, 2, 3, 4, 5]
        total_requests = 10
        total_requests_time_sec = 30
        stats = prepare_stats(
            time_stats, total_requests, total_requests_time_sec
        )
        self.assertIsInstance(stats, dict)
        self.assertEqual(stats['count'], 5)
        self.assertEqual(stats['count_perc'], 50)
        self.assertEqual(stats['time_sum'], 15)
        self.assertEqual(stats['time_perc'], 50)
        self.assertEqual(stats['time_avg'], 3)
        self.assertEqual(stats['time_max'], 5)
        self.assertEqual(stats['time_med'], 3)

    def test_table_generation(self):
        total_requests = 100
        total_request_time_sec = 1000
        raw_table = [
            ('url1', [1, 1, 1]),
            ('url2', [2, 2, 2]),
            ('url3', [10, 10, 20]),
        ]
        result = prepare_table(
            raw_table, total_requests, total_request_time_sec
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['time_med'], 1)
        self.assertEqual(result[1]['count_perc'], 3)
        self.assertEqual(result[2]['time_max'], 20)


if __name__ == '__main__':
    unittest.main()
