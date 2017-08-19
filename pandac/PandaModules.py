# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: pandac.PandaModules
try:
    from panda3d.core import *
except ImportError as err:
    if 'No module named core' not in str(err):
        raise

try:
    from panda3d.physics import *
except ImportError as err:
    if 'No module named physics' not in str(err):
        raise

try:
    from panda3d.fx import *
except ImportError as err:
    if 'No module named fx' not in str(err):
        raise

try:
    from panda3d.direct import *
except ImportError as err:
    if 'No module named direct' not in str(err):
        raise

try:
    from panda3d.egg import *
except ImportError as err:
    if 'No module named egg' not in str(err):
        raise

try:
    from panda3d.ode import *
except ImportError as err:
    if 'No module named ode' not in str(err):
        raise