from litestar import Litestar, Router
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin

from litestar_todo.auth.controllers import AuthController
from litestar_todo.auth.utils import jwt_auth
from litestar_todo.core.database import sqlalchemy_config
from litestar_todo.todo.controllers import NoteController


def create_app() -> Litestar:
    """Create the Litestar application."""
    return Litestar(
        route_handlers=[
            Router(path="", route_handlers=[NoteController, AuthController]),
        ],
        on_app_init=[jwt_auth.on_app_init],
        openapi_config=OpenAPIConfig(
            title="Litestar TODO",
            version="1.0.0",
            description="Simple TODO",
            path="/docs",
            render_plugins=[SwaggerRenderPlugin()],
        ),
        debug=True,
        dependencies={
            "db_session": Provide(
                sqlalchemy_config.provide_session,
                sync_to_thread=True,
            ),
        },
        plugins=[SQLAlchemyPlugin(config=sqlalchemy_config)],
    )


app = create_app()
