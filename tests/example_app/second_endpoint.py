from brev_rest.route import Router
from . import shared2


route = Router("/second_endpoint")


@route
def get(id: str):
    ...


@route
def delete():
    ...