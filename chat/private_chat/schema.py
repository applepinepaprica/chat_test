import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from .models import Message
from django.contrib.auth.models import User


class MessageNode(DjangoObjectType):
    class Meta:
        model = Message
        interfaces = (graphene.relay.Node, )


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )
        only_fields = ['username', 'email']


class Query(graphene.ObjectType):
    messages = graphene.List(MessageNode, receiver_id=graphene.Int())
    me = graphene.Field(UserNode)
    users = graphene.List(UserNode)

    @staticmethod
    def resolve_messages(self, info, receiver_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        receiver = User.objects.get(id=receiver_id)
        messages = Message.objects.filter(Q(sender=user, receiver=receiver) | Q(sender=receiver, receiver=user))
        return messages

    @staticmethod
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user

    @staticmethod
    def resolve_users(self, info):
        return User.objects.all()


class SendMessage(graphene.relay.ClientIDMutation):
    message = graphene.Field(MessageNode)

    class Input:
        receiver_id = graphene.Int()
        text = graphene.String()

    @staticmethod
    def mutate_and_get_payload(root, info, **input):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        message = Message(
            sender=user,
            receiver=User.objects.get(id=input.get('receiver_id')),
            text=input.get('text')
        )
        message.save()

        return SendMessage(message=message)


class CreateUser(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserNode)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @staticmethod
    def mutate_and_get_payload(root, info, **input):
        user = User(
            username=input.get('username'),
            email=input.get('email')
        )
        user.set_password(input.get('password'))
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.AbstractType):
    send_message = SendMessage.Field()
    create_user = CreateUser.Field()
