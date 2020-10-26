from brev_rest.route import Router


route = Router("/endpoint")


@route
def get():
    return "original"


@route(path="/{ep_id}")
def get(ep_id: str):
    return ep_id


@route()
def put():
    return


@route(status_code=201)
def post():
    return


@route(path="/subpath")
def delete():
    return