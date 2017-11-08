class event(list):
    """Event subscription.

    https://stackoverflow.com/questions/1092531/event-system-in-python

    A list of callable objects. Calling an instance of this will cause a
    call to each item in the list in ascending order by index.

    Example Usage:

    >>> def f(x):
    ...     print 'f(%s)' % x
    >>> def g(x):
    ...     print 'g(%s)' % x
    >>> e = event()
    >>> e()
    >>> e.append(f)
    >>> e(123)
    f(123)
    >>> e.remove(f)
    >>> e()
    >>> e += (f, g)
    >>> e(10)
    f(10)
    g(10)
    >>> del e[0]
    >>> e(2)
    g(2)

    """
    def __call__(self, *args, **kwargs):
        for f in self:
            f(*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % list.__repr__(self)

e = event()
def f(x):
    print 'f(%s)' %x
def g(x):
    print 'g(%s)' %x
def h():
    print 'I was called'

# e()
# e.append(f)
# e.append(g)
# e.append(g)
# e.remove(g)
# e.remove(g)
# e.remove(f)
#
#
# e += (f, g)
# del e[0]
# del e[0]
# e.append(h)
# e()
# print(e)