import unittest

from tests_code.my_code import MyCode


class SomethingTest(unittest.TestCase):

    def setUp(self):
        """
        Called each time before the test is run
        :return:
        """
        self.st = MyCode()

    def tearDown(self):
        """
        Release database or file connection (call after the test - if there is error in setUp then this is not called)
        :return:
        """
        pass

    def test_something(self):
        self.st.set_value("a", 10)
        self.assertEqual(self.st.get_value("a"), 10)

    def test_something_else(self):
        self.st.set_value("b", 10)
        self.assertEqual(self.st.get_value("b"), 10)
        with self.assertRaises(KeyError):
            self.st.get_value("a")
