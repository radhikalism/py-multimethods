from multimethods import Multimethod, NoMatchingMethodError

#### Example usage

def split_prefix(text):
    return text.split(' ')[:2]

Multimethod('respond', split_prefix)

@Multimethod.add("counting", "sheep")
def respond(text):
    return text + " put you to sleep"

@Multimethod.add("flying", "pigs")
def respond(text):
    return text + " are rare"

@Multimethod.add("walking", "fish")
def respond(text):
    return text + " would be surprising"

@Multimethod.add(default=True)
def respond(text):
    return "I have no idea"


#### Tests

def test_happy_case():
    return [respond("counting sheep"),
            respond("walking fish in the garden"),
            respond("unexpected")]

def test_bad_input():
    try:
        return respond("too", "many", "args")
    except Exception, e:
        return e

def test_missing_method():
    try:
        return respond("foo")
    except Exception, e:
        return e    

def test_removal():
    respond.remove("counting", "sheep")
    return respond("counting sheep")

# test_happy_case()
# => ['counting sheep put you to sleep',
#     'walking fish in the garden would be surprising',
#     'I have no idea']

# test_bad_input()
# => TypeError('split_prefix() takes exactly 1 positional argument (3 given)',)

# test_removal():
# => 'I have no idea'

