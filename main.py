from fastapi import FastAPI
import graphene
from starlette_graphene3 import GraphQLApp, make_graphiql_handler


class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()
    age = graphene.Int()

    def resolve_id(self, info):
        return self.id

    def resolve_name(self, info):
        return self.name

    def resolve_age(self, info):
        return self.age

def get_users():
    users = [
        User(id="1", name="John", age=23),
        User(id="2", name="Jane", age=34),
    ]
    return users

class Query(graphene.ObjectType):
    hello = graphene.String()
    bye = graphene.String()
    user = graphene.Field(User, id=graphene.ID(required=True))
    users = graphene.List(User)


    def resolve_hello(self, info):
        return "Hello World"

    def resolve_bye(self, info):
        return "Goodbye World"

    def resolve_user(self, info, id):
        for user in get_users():
            if user.id == id:
                return user
        return None

    def resolve_users(self, info):
        return get_users()





app = FastAPI()
app.mount("/",
          GraphQLApp(
              schema=graphene.Schema(query=Query),
              on_get=make_graphiql_handler()))
