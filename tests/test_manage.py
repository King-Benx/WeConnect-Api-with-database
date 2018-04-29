import unittest
from flask import url_for
from manage import deploy, make_shell_context


class TestManageFunctions(unittest.TestCase):
    def test_deploy(self):
        self.assertEquals(deploy(), None)

    def test_make_shell_context(self):
        self.assertEquals(len(make_shell_context()), 5)
