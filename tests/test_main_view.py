import unittest
from flask import url_for
from app import create_app, db
from app.main import main


class TestMain(unittest.TestCase):
    def test_index_page(self):
        self.assertTrue(url_for('main.index', _external=True), 200)

    def test_api_docs(self):
        self.assertTrue(str(url_for('main.index', _external=True)) + 'apidocs', 200)