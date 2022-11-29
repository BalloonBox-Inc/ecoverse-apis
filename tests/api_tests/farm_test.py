'''This module performs API tests on the following directory: ./apis/routers/farm.py'''

from starlette.testclient import TestClient

from apis.schemas.farm import Farm, FarmResponse
from config import get_settings
from main import app


client = TestClient(app)
settings = get_settings()
router_prefix = f'{settings.API.PREFIX}/farm'


def checker_200(response):
    keys_1 = ['items', 'total', 'page', 'size']
    keys_2 = FarmResponse.__fields__.keys()

    status_code = response.status_code
    json_response = response.json()

    # check response.status code
    assert status_code == 200

    # check response.json() keys
    for k in keys_1:
        assert k in json_response

    # check response.json() items type
    item = json_response['items'][0]
    assert isinstance(item, dict)

    # check response.json() items keys
    for k in item:
        assert k in keys_2


def checker_422(response, method):
    params = ['farmId']
    keys_1 = ['error', 'message']
    keys_2 = Farm.__fields__.keys()

    status_code = response.status_code
    json_response = response.json()

    # check response.status code
    assert status_code == 422

    # check response.json() keys
    for k in keys_1:
        assert k in json_response

    # check response.json() message type
    assert isinstance(json_response['message'], dict)

    # check response.json() message keys
    if method == 'post':
        for k in json_response['message'].keys():
            assert k in keys_2

    if method == 'get':
        for k in json_response['message'].keys():
            assert k in params


def test_200():
    # /farm router
    response = client.post(
        url=f'{router_prefix}',
        json={
            'country': 'Thailand',
            'resource': 'Rubber',
            'status': 'Active',
            'minSize': 100,
            'maxSize': 1000,
            'certifiedFSC': True
        }
    )
    checker_200(response)

    # /farm/{farmId} router
    response = client.get(
        url=f'{router_prefix}/1648192678575'
    )
    checker_200(response)


def test_422():
    # /farm router
    response = client.post(
        url=f'{router_prefix}',
        json={
            'resource': 12345,
            'status': 'Pending',
            'minSize': -100,
            'maxSize': -1000,
            'certifiedFSC': 'Certified'
        }
    )
    checker_422(response, 'post')

    # /farm/{farmId} router
    response = client.get(
        url=f'{router_prefix}/not-id'
    )
    checker_422(response, 'get')
