import json
from rest_framework.test import APISimpleTestCase
from django.urls import reverse


class TestSetUp(APISimpleTestCase):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_create_access_token_with_bad_request_model(self):
        url = reverse('create')
        response = self.client.post(url, data=None,  follow=True, secure=False)
        self.assertEqual(response.status_code, 400)

    def test_create_access_token_with_good_request_model(self):
        url = reverse('create')
        request_model = [1,2,3]
        response = self.client.post(url, data=json.dumps(request_model), follow=True, secure=False)
        self.assertEqual(response.status_code, 200)

    def test_validate_door_access_with_bad_request_model(self):
        url = reverse('validate')

        # completely bad model
        request_model = {
            'XXXX': "AAAA",
            'YYYY': 99
        }
        response = self.client.post(url, data=json.dumps(request_model), follow=True, secure=False)
        self.assertEqual(response.status_code, 400)

        # missing access token
        request_model = {
            'XXXX': "AAAA",
            'door_id': "ABC"
        }
        response = self.client.post(url, data=json.dumps(request_model), follow=True, secure=False)
        self.assertEqual(response.status_code, 400)

        # access token is a number
        request_model = {
            'access_token': 9999999,
            'door_id': 1
        }
        response = self.client.post(url, data=json.dumps(request_model), follow=True, secure=False)
        self.assertEqual(response.status_code, 400)

        # door is a alpha
        request_model = {
            'access_token': "a85f96c2-f26b-4a0f-bff6-e8f83c6d6559",
            'door_id': "abc"
        }
        response = self.client.post(url, data=json.dumps(request_model), follow=True, secure=False)
        self.assertEqual(response.status_code, 400)

    def test_create_access_token_and_validate_door_will_open(self):
        url = reverse('create')

        # create an access token for doors 1, 2 and 3
        request_model = [1, 2, 3]
        response = self.client.post(url, data=json.dumps(request_model), follow=True, secure=False)
        self.assertEqual(response.status_code, 200)

        # get the access token just created
        response_model = json.loads(response.content.decode())
        access_token = response_model['access_token']

        # request to open door 99 using the above access token ... expect access to be denied
        url = reverse('validate')
        request_model = {
            'access_token': access_token,
            'door_id': 99
        }
        response = self.client.post(url, data=json.dumps(request_model), follow=True, secure=False)
        self.assertEqual(response.status_code, 200)
        response_model = json.loads(response.content.decode())
        self.assertEqual(request_model['access'], False)

        # request to open door 1 but with the token ... expect access to be granted
        request_model = {
            'access_token': access_token,
            'door_id': 1
        }
        response = self.client.post(url, data=json.dumps(request_model), follow=True, secure=False)
        self.assertEqual(response.status_code, 200)
        response_model = json.loads(response.content.decode())
        self.assertEqual(request_model['access'], True)
