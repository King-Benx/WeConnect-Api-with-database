import unittest
from app.functions import make_json_reply, check_validity_of_mail, check_validity_of_username, check_validity_of_input


class TestFunctions(unittest.TestCase):
    def test_make_json_reply(self):
        self.assertTrue(make_json_reply('title', 'message'), 200)

    def test_check_correct_validity_of_mail(self):
        self.assertTrue(check_validity_of_mail('johndoe@mail.com'))

    def test_check_wrong_validity_of_mail(self):
        self.assertEqual(check_validity_of_mail('johnmail.com'), None)

    def test_check_correct_validity_of_username(self):
        self.assertTrue(check_validity_of_username('johndoe'))

    def test_check_wrong_validity_of_username(self):
        self.assertEqual(check_validity_of_username('.johndoe'), None)

    def test_check_correct_validity_of_input(self):
        self.assertEqual(
            check_validity_of_input(username='john', password='pass'), True)

    def test_check_wrong_validity_of_input(self):
        self.assertEqual(check_validity_of_input(username=''), False)
