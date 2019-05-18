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
        only_fields = ['username']


class Query(graphene.ObjectType):
    messages = graphene.List(MessageNode, receiver_id=graphene.Int())

    @staticmethod
    def resolve_messages(self, info, receiver_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        receiver = User.objects.get(id=receiver_id)
        messages = Message.objects.filter(Q(sender=user, receiver=receiver) | Q(sender=receiver, receiver=user))
        return messages


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


class Mutation(graphene.AbstractType):
    send_message = SendMessage.Field()
