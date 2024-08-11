import environ

env = environ.Env()
environ.Env.read_env()

DEBUG = env.bool('DEBUG')

if DEBUG:
    from .base import *

else:
    from .production import *
