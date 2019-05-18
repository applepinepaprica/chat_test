import graphene
import graphql_jwt
import private_chat.schema


class Query(private_chat.schema.Query, graphene.ObjectType):
    pass


class Mutation(private_chat.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
