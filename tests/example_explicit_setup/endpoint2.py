from brev_rest import Router

route = Router("/ex/endpoint2")


@route
def get():
    return "get"


@route
def post():
    return "post"
