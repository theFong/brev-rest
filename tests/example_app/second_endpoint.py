from brev_rest.route import Router
from . import shared2


route = Router("/second_endpoint")


@route
def get():
    return shared2.do_thing()


@route
def delete():
    return "delete"
