import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql_relay.node.node import from_global_id
from .models import Message, Dialogue
from django.contrib.auth.models import User
from django.db.models import Q
from .permission_checkers import login_required


class MessageNode(DjangoObjectType):
    class Meta:
        model = Message
        interfaces = (graphene.relay.Node, )


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node, )
        only_fields = ['username', 'email']


class DialogueNode(DjangoObjectType):
    class Meta:
        model = Dialogue
        interfaces = (graphene.relay.Node, )


class MessageConnection(relay.Connection):
    class Meta:
        node = MessageNode


class UserConnection(relay.Connection):
    class Meta:
        node = UserNode


class DialogueConnection(relay.Connection):
    class Meta:
        node = DialogueNode


class Query(graphene.ObjectType):
    messages = relay.ConnectionField(MessageConnection, dialogue_id=graphene.String())
    me = graphene.Field(UserNode)
    users = relay.ConnectionField(UserConnection)
    my_dialogues = relay.ConnectionField(DialogueConnection)

    @login_required
    @staticmethod
    def resolve_messages(self, info, dialogue_id, **kwargs):
        user = info.context.user

        dialogue = Dialogue.objects.get(id=from_global_id(dialogue_id)[1])
        if dialogue.user1 != user and dialogue.user2 != user:
            raise Exception('Forbidden!')

        messages = Message.objects.filter(dialogue=dialogue)
        return messages

    @login_required
    @staticmethod
    def resolve_me(self, info, **kwargs):
        return info.context.user

    @staticmethod
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    @login_required
    @staticmethod
    def resolve_my_dialogues(self, info, **kwargs):
        user = info.context.user
        dialogues = Dialogue.objects.filter(Q(user1=user) | Q(user2=user))
        return dialogues


class SaveMessage(graphene.relay.ClientIDMutation):
    message = graphene.Field(MessageNode)

    class Input:
        dialogue_id = graphene.String()
        text = graphene.String()

    @login_required
    @staticmethod
    def mutate_and_get_payload(root, info, **input):
        user = info.context.user

        dialogue = Dialogue.objects.get(id=from_global_id(input.get('dialogue_id'))[1])
        if dialogue.user1 != user and dialogue.user2 != user:
            raise Exception('Forbidden!')

        message = Message(
            sender=user,
            dialogue=dialogue,
            text=input.get('text')
        )
        message.save()

        return SaveMessage(message=message)


class CreateDialogue(graphene.relay.ClientIDMutation):
    dialogue = graphene.Field(DialogueNode)

    class Input:
        receiver_id = graphene.String()

    @login_required
    @staticmethod
    def mutate_and_get_payload(root, info, **input):
        user = info.context.user

        dialogue = Dialogue(
            user1=user,
            user2=User.objects.get(id=from_global_id(input.get('receiver_id'))[1]),
        )
        dialogue.save()

        return CreateDialogue(dialogue=dialogue)


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
    save_message = SaveMessage.Field()
    create_dialogue = CreateDialogue.Field()
    create_user = CreateUser.Field()
