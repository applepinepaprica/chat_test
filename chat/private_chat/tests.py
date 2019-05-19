from django.test import TestCase
from .data import *


class Tests(TestCase):

    def setUp(self):
        initialize()
        self.token = get_token()
        self.receiver_id = get_receiver_id()

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
        query = {"query":
                 "{messages(receiverId: \"%s\"){edges {node {text receiver {username} sender {username}}}}}"
                 % self.receiver_id}
        expected = {
          "data": {
            "messages": {
              "edges": [
                {
                  "node": {
                    "text": "Text",
                    "sender": {
                      "username": "user1"
                    },
                    "receiver": {
                      "username": "user2"
                    }
                  }
                },
                {
                  "node": {
                    "text": "Text",
                    "sender": {
                      "username": "user2"
                    },
                    "receiver": {
                      "username": "user1"
                    }
                  }
                }
              ]
            }
          }
        }
        assert_test_with_auth(query, expected, self.token)
