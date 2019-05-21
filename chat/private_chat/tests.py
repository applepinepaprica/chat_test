from django.test import TestCase
from .data import *


class Tests(TestCase):

    def setUp(self):
        initialize()
        self.token = get_token()
        self.dialogue_id = get_dialogue_id(self.token)

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
        query = "{me {username email}}"
        expected = {
          "data": {
            "me": {
              "username": "user1",
              "email": "email@gmail.com"
            }
          }
        }
        assert_test_with_auth(query, expected, self.token)

    def test_get_users(self):
        query = '''{
          users {
            edges {
              node {
                username
                email
              }
            }
          }
        }'''
        expected = {
          "data": {
            "users": {
              "edges": [
                {
                  "node": {
                    "username": "user1",
                    "email": "email@gmail.com"
                  }
                },
                {
                  "node": {
                    "username": "user2",
                    "email": "email@gmail.com"
                  }
                }
              ]
            }
          }
        }
        assert_test_without_auth(query, expected)

    def test_get_messages(self):
        query = "{messages(dialogueId: \"%s\"){edges {node {text sender {username}}}}}" % self.dialogue_id
        expected = {
          "data": {
            "messages": {
              "edges": [
                {
                  "node": {
                    "text": "Text",
                    "sender": {
                      "username": "user1"
                    }
                  }
                },
                {
                  "node": {
                    "text": "Text",
                    "sender": {
                      "username": "user2"
                    }
                  }
                }
              ]
            }
          }
        }
        assert_test_with_auth(query, expected, self.token)
