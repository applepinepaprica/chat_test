from django.test import TestCase
from .data import *


class Tests(TestCase):

    def setUp(self):
        initialize()
        self.token = get_token()

    def test_create_user(self):
        query = '''
            mutation {
              createUser(input: {username: "user", password: "password", email: "email@gmail.com"}) {
                user {
                  username
                  email
                }
              }
            }
            '''
        expected = {
          "data": {
            "createUser": {
              "user": {
                "username": "user",
                "email": "email@gmail.com"
              }
            }
          }
        }
        assert_test_without_auth(query, expected)

    def test_get_me(self):
        query = {"query": "{me {username email}}"}
        expected = {
          "data": {
            "me": {
              "username": "user1",
              "email": "email@gmail.com"
            }
          }
        }
        assert_test_with_auth(query, expected, self.token)
