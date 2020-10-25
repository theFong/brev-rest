import os
import pathlib
from fastapi.testclient import TestClient

from brev_rest import __version__
from brev_rest import route_loader, route, app

test_app_name = "example_app"


def test_version():
    assert __version__ == "0.1.0"


def get_test_app_path():
    script_path = os.path.realpath(__file__)
    path = pathlib.Path(script_path).parent
    path = os.path.join(path, test_app_name)
    return path


def test_route_loader():
    test_app_path = get_test_app_path()

    route_loader.make_routes(app_path=test_app_path)

    assert len(route.all_routes) == 2


def test_brev_fastapi_app():
    test_app_path = get_test_app_path()

    server = app.get_server(app_path=test_app_path)

    tc = TestClient(server)
    resp = tc.get("/endpoint")

    resp.status_code == 200

    resp = tc.delete("/second_endpoint")

    resp.status_code == 200