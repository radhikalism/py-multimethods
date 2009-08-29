import unittest
from multimethods import Multimethod, NoMatchingMethodError


def split_prefix(text):
    """Returns a 2-tuple of the initial words in TEXT."""
    return text.split(' ')[:2]


Multimethod('respond1', split_prefix)
"""respond1 has no default method"""

@Multimethod.add("counting", "sheep")
def respond1(text):
    return text + " put you to sleep"

@Multimethod.add("flying", "pigs")
def respond1(text):
    return text + " are rare"

@Multimethod.add("walking", "fish")
def respond1(text):
    return text + " would be surprising"


Multimethod('respond2', split_prefix)
"""respond2 has a default method that is used"""

@Multimethod.add("incredible", "clouds")
def respond2(text):
    return text + " - fluffy things"

@Multimethod.add(default=True)
def respond2(text):
    return "I have no idea"


Multimethod('respond3', split_prefix)
"""respond3 has a default method that is removed and unused"""

@Multimethod.add("gold", "bars")
def respond3(text):
    return text + " are golden and bar-like"

@Multimethod.add(default=True)
def respond3(text):
    return "Default method to be removed."


class TestMultimethods(unittest.TestCase):

    def test_happy_case(self):
        self.assertEqual([respond1("counting sheep"),
                          respond1("walking fish in the garden")],
                         ['counting sheep put you to sleep',
                          'walking fish in the garden would be surprising'])

    def test_bad_input(self):
        outcome = None
        try:
            outcome = respond1("too", "many", "args")
        except Exception, e:
            outcome = e
        self.assertEqual(type(outcome), TypeError)
                        
    def test_removal(self):
        self.assertEqual(respond2.remove("incredible", "clouds"), True)
        self.assertEqual(respond2("incredible clouds"),
                         'I have no idea')

    def test_nonexisting_default_removal(self):
        self.assertEqual(respond1.remove(default=True), False)
        self.assertEqual(respond1.default_method, None)

    def test_existing_default_removal(self):
        self.assertEqual(respond3.remove(default=True), True)
        self.assertEqual(respond3.default_method, None)

    def test_missing_method(self):
        outcome = None
        try:
            outcome = respond1("foo")
        except Exception, e:
            outcome = e
        self.assertEqual(type(outcome), NoMatchingMethodError)


suite = unittest.TestLoader().loadTestsFromTestCase(TestMultimethods)
unittest.TextTestRunner(verbosity=2).run(suite)        
