from brev_rest import Router
from example_app import shared1  # type: ignore


router = Router("/endpoint")


@router
def get():
    return shared1.share1


@router(path="/{ep_id}")  # type: ignore
def get(ep_id: str):  # noqa: F811 | ignore redef
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
