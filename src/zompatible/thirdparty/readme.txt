profilehooks.py:
---------------
This is Marius Gedminas profiling decorator, distributed under a MIT licence.
You must:
- apt-get install python-profiler
- profile the wanted function with :

from zompatible.thirdparty.profilehooks import profile
@profile
def function(...)
    u"the function you want to profile"

The result will go on the console when zope is stopped.
One can get the immediate result by passing immediate=True to the decorator