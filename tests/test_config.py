import unittest

from log_analyzer.report import Config, prepare_config


class ConfigTest(unittest.TestCase):
    def test_empty_config(self):
        config = prepare_config(config_path=None)
        self.assertIsInstance(config, Config)


if __name__ == '__main__':
    unittest.main()
