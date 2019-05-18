import graphene

import private_chat.schema


class Query(private_chat.schema.Query, graphene.ObjectType):
    pass


class Mutation(private_chat.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
