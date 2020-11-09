from brev_rest import Setup
from . import endpoint

setup = Setup()
setup.add_router(endpoint.router)


@Setup.app_before_setup
def app_before_setup(app):
    ...


@Setup.app_after_setup
def app_after_setup(app):
    ...
