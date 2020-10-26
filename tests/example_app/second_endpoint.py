from brev_rest.route import Router


route = Router("/second_endpoint")


@route
def get(id: str):
    ...


@route
def delete():
    ...