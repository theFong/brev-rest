import os
import json
import pathlib
import pytest
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

    assert len(route.Router.get_all_routes()) == 3


@pytest.fixture()
def brev_client():
    test_app_path = get_test_app_path()

    server = app.get_server(app_path=test_app_path)

    tc = TestClient(server)
    yield tc
    app.reset()


def test_brev_endpoint(brev_client: TestClient):
    resp = brev_client.get("/endpoint")

    assert resp.status_code == 200
    assert resp.json() == "original"


def test_brev_sub_path(brev_client: TestClient):
    resp = brev_client.delete("/endpoint/subpath")
    assert resp.status_code == 200


def test_brev_overload_get(brev_client: TestClient):
    ep_id = "1234"
    resp = brev_client.get(f"/endpoint/{ep_id}")

    assert resp.json() == ep_id


def test_brev_change_default_status(brev_client: TestClient):
    resp = brev_client.post(f"/endpoint")

    assert resp.status_code == 201


def test_brev_other_endpoint(brev_client: TestClient):
    resp = brev_client.delete("/second_endpoint")

    assert resp.status_code == 200


def test_brev_sub_package(brev_client: TestClient):
    resp = brev_client.get("/subpackage")

    assert resp.status_code == 200