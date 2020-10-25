from brev_rest.route import Route


route = Route("/second_endpoint")


@route
def get(id: str):
    ...


@route
def delete():
    ...