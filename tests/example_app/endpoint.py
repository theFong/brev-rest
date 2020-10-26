from brev_rest.route import Router
from example_app import shared1  # type: ignore


router = Router("/endpoint")


@router
def get():
    return "original"


@router(path="/{ep_id}")
def get(ep_id: str):
    return ep_id


@router()
def put():
    return


@router(status_code=201)
def post():
    return


@router(path="/subpath")
def delete():
    return