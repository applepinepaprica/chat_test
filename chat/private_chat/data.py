from graphene.test import Client
from chat.schema import schema
from .models import Message, Dialogue
from django.contrib.auth.models import User
import django.test


def initialize():
    user1 = User(
        username="user1",
        email="email@gmail.com"
    )
    user1.set_password("password")
    user1.save()

    user2 = User(
        username="user2",
        email="email@gmail.com"
    )
    user2.set_password("password")
    user2.save()

    dialogue = Dialogue(
        user1=user1,
        user2=user2
    )
    dialogue.save()

    message1 = Message(
        sender=user1,
        dialogue=dialogue,
        text="Text"
    )
    message1.save()

    message2 = Message(
        sender=user2,
        dialogue=dialogue,
        text="Text"
    )
    message2.save()


def get_token():
    query = '''
       mutation {
          tokenAuth(username: "user1", password: "password") {
            token
          }
        }'''
    client = Client(schema)
    result = client.execute(query)
    return result.get('data').get('tokenAuth').get('token')


def get_dialogue_id(token):
    query = {"query": "{myDialogues(first: 1) {edges {node {id}}}}"}
    headers = {
        'HTTP_AUTHORIZATION': f'JWT {token}'
    }
    client = django.test.Client()
    response = client.get('/graphql/', query, content_type='application_json', **headers)
    return response.json().get('data').get('myDialogues').get('edges')[0].get('node').get('id')


def assert_test_without_auth(query, expected):
    client = Client(schema)
    result = client.execute(query)
    assert result == expected


def assert_test_with_auth(query, expected, token):
    headers = {
        'HTTP_AUTHORIZATION': f'JWT {token}'
    }
    client = django.test.Client()
    response = client.get('/graphql/', query, content_type='application_json', **headers)
    assert response.json() == expected
