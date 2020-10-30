from brev_rest import Setup


from . import endpoint1
from . import endpoint2

setup = Setup(title="Explicit Setup")

setup.add_router(endpoint2.route)
setup.add_router(endpoint1.route)


@Setup.app_before_setup
def app_before_setup(app):
    ...


@Setup.app_after_setup
def app_after_setup(app):
    ...
