import base64
import json
import pathlib
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import app

TEST_DIR = pathlib.Path(__file__).parent


def load_json_from_file(filename):
    path = (TEST_DIR / filename).resolve()

    with open(path, encoding='utf-8') as file:
        return json.load(file)


def decode_base64_patch(data):
    return json.loads(base64.b64decode(data.encode()).decode())


class TestEndpoints(TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.test_data_a = load_json_from_file('test_data_a.json')
        self.test_data_b = load_json_from_file('test_data_b.json')
        self.test_data_c = load_json_from_file('test_data_c.json')

    def test_health(self):
        response = self.client.get('/healthz')
        assert response.status_code == 204

    def test_mutate_endpoint_with_test_data_a(self, *args, **kwargs):  # noqa
        response = self.client.post('/mutate', data=json.dumps(self.test_data_a))
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['kind'] == 'AdmissionReview'
        assert response_json['apiVersion'] == 'admission.k8s.io/v1'
        assert response_json['response']['uid'] == '22105493-679e-4223-8a75-35da267d4ec7'
        assert response_json['response']['allowed'] is True
        assert response_json['response']['patchType'] == 'JSONPatch'
        response_patch = decode_base64_patch(response.json()['response']['patch'])
        assert response_patch == []

    def test_mutate_endpoint_with_test_data_b(self, *args, **kwargs):  # noqa
        response = self.client.post('/mutate', data=json.dumps(self.test_data_b))
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['kind'] == 'AdmissionReview'
        assert response_json['apiVersion'] == 'admission.k8s.io/v1'
        assert response_json['response']['uid'] == '260d46e9-7307-4c8b-b05f-eeefaa972b69'
        assert response_json['response']['allowed'] is True
        assert response_json['response']['patchType'] == 'JSONPatch'
        response_patch = decode_base64_patch(response.json()['response']['patch'])
        assert response_patch == []

    def test_mutate_endpoint_with_test_data_c(self, *args, **kwargs):  # noqa
        response = self.client.post('/mutate', data=json.dumps(self.test_data_c))
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['kind'] == 'AdmissionReview'
        assert response_json['apiVersion'] == 'admission.k8s.io/v1'
        assert response_json['response']['uid'] == 'b44f01b7-2dee-41da-ba64-8552e18b6d60'
        assert response_json['response']['allowed'] is True
        assert response_json['response']['patchType'] == 'JSONPatch'
        response_patch = decode_base64_patch(response.json()['response']['patch'])
        assert response_patch == []
