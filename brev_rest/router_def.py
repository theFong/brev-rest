from typing import Callable, Optional, List, Union, Any, Type, Dict, Sequence, TypeVar
from fastapi.applications import (
    Response,
    SetIntStr,
    DictIntStrAny,
    Depends,
)
import fastapi.routing
import starlette.routing
from . import route
from .types import AnyCallable

T = TypeVar("T", bound=AnyCallable)


class Router(route.Router):
    def __init__(
        self,
        path: str,
        name: Optional[str] = None,
        routes: Optional[List[starlette.routing.BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: Optional[fastapi.routing.ASGIApp] = None,
        dependency_overrides_provider: Optional[Any] = None,
        route_class: Type[fastapi.routing.APIRoute] = fastapi.routing.APIRoute,
        default_response_class: Optional[Type[Response]] = None,
        on_startup: Optional[Sequence[AnyCallable]] = None,
        on_shutdown: Optional[Sequence[AnyCallable]] = None,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        **kwargs: Any,
    ):

        super().__init__(
            path,
            name=name,
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=route_class,
            default_response_class=default_response_class,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            tags=tags,
            dependencies=dependencies,
            responses=responses,
            **kwargs,
        )

    def __call__(
        self,
        endpoint: T = None,
        *,
        path: str = route.default_sub_path,
        response_model: Optional[Type[Any]] = None,
        status_code: int = 200,
        tags: Optional[List[str]] = None,
        dependencies: Optional[Sequence[Depends]] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        response_description: str = "Successful Response",
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        deprecated: Optional[bool] = None,
        operation_id: Optional[str] = None,
        response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        name: Optional[str] = None,
        callbacks: Optional[List[fastapi.routing.APIRoute]] = None,
        route_class_override: Optional[Type[fastapi.routing.APIRoute]] = None,
    ) -> Union[T, Callable[[T], T]]:
        return super().__call__(
            endpoint=endpoint,
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            include_in_schema=include_in_schema,
            name=name,
            callbacks=callbacks,
            response_class=response_class,
            route_class_override=route_class_override,
        )
