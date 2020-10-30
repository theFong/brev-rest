from brev_rest import Router

route = Router("/endpoint1")


@route
def get():
    return "get_endpoint1"


@route
def post():
    return "post"