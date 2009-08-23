# multimethods.py provides a simplistic implementation of Clojure-like
# multimethods for Python 2.4 or later.

# README:

# Included classes:
#  * Multimethod: instantiates to an object to which
#    implementing methods belong.  Methods are added via the
#    static Multimethod.add() decorator.  Methods can be removed
#    or prioritized using Multimethod.remove() and Multimethod.prefer()
#    respectively.
#
#  * NoMatchingMethodError: thrown when there is no implementing
#    method found for a call with some given arguments.  This implies
#    that no default method was added.

# Methods can only be defined at the top level global namespace.

# See tests.py for an example of usage.

# LICENSE:

# Copyright (c) 2009 Abhishek Reddy

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


class Error(Exception):
    pass

class NoMatchingMethodError(Error):
    name = None
    args = None
    
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return "%s %s " % (repr(self.name), repr(self.args))

class Multimethod:
    name = None
    methods = []
    default_method = None
    dispatch_fn = None

    def __init__(self, name, dispatch_fn):
        self.name = name
        self.dispatch_fn = dispatch_fn
        globals()[name] = self

    def __call__(self, *args, **kwargs):
        dispatch_key = tuple(self.dispatch_fn(*args, **kwargs))
        for meth in self.methods:
            if meth.__dispatch_key__ == dispatch_key:
                return meth(*args, **kwargs)
        if self.default_method:
            return self.default_method(*args, **kwargs)
        else:
            raise NoMatchingMethodError(self.name, args)

    @staticmethod
    def add(*args, **kwargs):
        def decorator(meth):
            multimethod = globals()[meth.__name__]
            if "default" in kwargs and kwargs["default"]:
                multimethod.default_method = meth
            if len(args) > 0:
                meth.__dispatch_key__ = args
                multimethod.methods.append(meth)
            return multimethod
        return decorator

    def remove(self, *args, **kwargs):
        for meth in self.methods:
            if meth.__dispatch_key__ == args:
                self.methods.remove(meth)
                return True
        return False

    def prefer(self, key1, key2, **kwargs):
        meth1_index = self.methods.index(tuple(key1))
        meth1 = self.methods[meth1_index]
        del self.methods[meth1]
        meth2_index = self.methods.index(tuple(key2))
        self.methods.insert(meth2_index, meth1)
        return True

