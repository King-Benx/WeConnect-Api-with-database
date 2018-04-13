import unittest
from app.functions import make_json_reply


class TestFunctions(unittest.TestCase):
    def test_inbuilt_functions(self):
        self.assertTrue(make_json_reply('message'), 200)
