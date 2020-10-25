from brev_rest import route


route = route.Route("/endpoint")


@route
def get():
    ...


@route
def put():
    ...