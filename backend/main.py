import strawberry
from api import v1
from config import app_config
from db.session import client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gql.context import get_context
from gql.router import Mutation, Query
from gql.types.core import PyObjectIdType
from models.core import PyObjectId
from strawberry.fastapi import GraphQLRouter

app = FastAPI(
    title="Sample API",
    swagger_ui_parameters={"deepLinking": False},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1.api_router, prefix=app_config.API_V1)

# GraphQL用のルータを追加
schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    enable_federation_2=True,
    scalar_overrides={PyObjectId: PyObjectIdType},
)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


@app.on_event("shutdown")
def shutdown_event():
    client.close()


@app.get("/")
def read_root():
    return "FastAPI-Nuxt3-GraphQL-Sample"
