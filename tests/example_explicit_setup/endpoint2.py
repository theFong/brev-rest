from brev_rest import Router

route = Router("/endpoint2")


@route
def get():
    return "get"


@route
def post():
    return "post"
