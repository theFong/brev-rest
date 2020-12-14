import os
import pathlib
from sys import flags
import pytest
from fastapi.testclient import TestClient

from brev_rest import __version__
from brev_rest import loader, route, app

test_app_name = "example_app"


def test_version():
    assert __version__ == "0.1.0"


def get_test_app_path():
    script_path = os.path.realpath(__file__)
    path = pathlib.Path(script_path).parent
    path = os.path.join(path, test_app_name)
    return path


def get_test_explicit_app_path():
    script_path = os.path.realpath(__file__)
    path = pathlib.Path(script_path).parent
    path = os.path.join(path, "example_explicit_setup")
    return path


def test_loader():
    test_app_path = get_test_app_path()

    loader.init_setup(app_path=test_app_path)

    loader.make_routers(app_path=test_app_path)

    assert len(route.Router.get_all_routers()) == 3


def test_get_meta():
    test_app_path = get_test_app_path()

    test_app_path = get_test_explicit_app_path()

    meta = app.get_meta(app_path=test_app_path)

    app.reset(app_path=test_app_path)

    assert meta["openapi"] == "3.0.2"


@pytest.fixture
def brev_explicit_client():
    test_app_path = get_test_explicit_app_path()

    server = app.get_server(app_path=test_app_path)

    tc = TestClient(server)
    yield tc
    app.reset(app_path=test_app_path)


@pytest.fixture
def brev_client():
    test_app_path = get_test_app_path()
    app.reset(app_path=test_app_path)

    server = app.get_server(app_path=test_app_path)

    tc = TestClient(server)
    yield tc
    app.reset(app_path=test_app_path)


def test_brev_endpoint(brev_client: TestClient):
    resp = brev_client.get("/endpoint")

    assert resp.status_code == 200
    assert resp.json() == "shared1"


def test_brev_sub_path(brev_client: TestClient):
    resp = brev_client.delete("/endpoint/subpath")
    assert resp.status_code == 200


def test_brev_overload_get(brev_client: TestClient):
    ep_id = "1234"
    resp = brev_client.get(f"/endpoint/{ep_id}")

    assert resp.json() == ep_id


def test_brev_change_default_status(brev_client: TestClient):
    resp = brev_client.post("/endpoint")

    assert resp.status_code == 201


def test_brev_other_endpoint(brev_client: TestClient):
    resp = brev_client.delete("/second_endpoint")

    assert resp.status_code == 200


def test_brev_use_other_mod(brev_client: TestClient):
    resp = brev_client.get("/second_endpoint")

    assert resp.json() == "did thing"


def test_brev_sub_package(brev_client: TestClient):
    resp = brev_client.get("/subpackage")

    assert resp.status_code == 200


def test_open_api_json(brev_client: TestClient):
    resp = brev_client.get("/openapi.json")
    openapi_json = resp.json()

    assert openapi_json["info"]["title"] == "Tests"
    assert openapi_json["paths"]["/endpoint"]["get"]["tags"][0] == "Endpoint"


def test_explicit_endpoint(brev_explicit_client: TestClient):
    resp = brev_explicit_client.get("/api/ex/endpoint1")

    assert resp.status_code == 200
    assert resp.json() == "get_endpoint1"
    assert len(route.Router.get_all_routers()) == 2


def test_explicit_open_api_json(brev_explicit_client: TestClient):
    resp = brev_explicit_client.get("/openapi.json")
    openapi_json = resp.json()

    assert openapi_json["info"]["title"] == "Explicit Setup"


def test_ordering_of_routes(brev_explicit_client: TestClient):
    resp = brev_explicit_client.get("/openapi.json")
    openapi_json = resp.json()

    i = 2
    for p in openapi_json["paths"].keys():
        assert str(i) in p
        i -= 1
