from typing import Optional, List, Union, Any, Type, Dict, Sequence
from fastapi.applications import BaseRoute, Response, JSONResponse, Middleware

from . import startup
from .types import AnyCallable


class Setup(startup.Setup):
    def __init__(
        self,
        debug: bool = False,
        routes: Optional[List[BaseRoute]] = None,
        title: Optional[str] = None,
        description: str = "",
        version: str = "0.1.0",
        openapi_url: Optional[str] = "/openapi.json",
        openapi_tags: Optional[List[Dict[str, Any]]] = None,
        servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
        default_response_class: Type[Response] = JSONResponse,
        docs_url: Optional[str] = "/docs",
        redoc_url: Optional[str] = "/redoc",
        swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
        swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,
        middleware: Optional[Sequence[Middleware]] = None,
        exception_handlers: Optional[
            Dict[Union[int, Type[Exception]], AnyCallable]
        ] = None,
        on_startup: Optional[Sequence[AnyCallable]] = None,
        on_shutdown: Optional[Sequence[AnyCallable]] = None,
        openapi_prefix: str = "",
        root_path: str = "",
        root_path_in_servers: bool = True,
        api_prefix: str = "",
        **extra: Any
    ):
        super().__init__(
            debug=debug,
            routes=routes,
            title=title,
            description=description,
            version=version,
            openapi_url=openapi_url,
            openapi_tags=openapi_tags,
            servers=servers,
            default_response_class=default_response_class,
            docs_url=docs_url,
            redoc_url=redoc_url,
            swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
            swagger_ui_init_oauth=swagger_ui_init_oauth,
            middleware=middleware,
            exception_handlers=exception_handlers,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            openapi_prefix=openapi_prefix,
            root_path=root_path,
            root_path_in_servers=root_path_in_servers,
            api_prefix=api_prefix,
            **extra
        )
