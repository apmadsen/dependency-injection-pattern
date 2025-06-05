from typing import Any, cast
from typingutils import AnyFunction
from types import FrameType, MethodType
from sys import modules
from inspect import Parameter as InspectParameter, FrameInfo, signature as get_signature, stack, unwrap

from di.core.reflection.undefined import Undefined
from di.core.reflection.signature import Signature
from di.core.reflection.parameter import Parameter
from di.core.reflection.parameter_kind import ParameterKind
from di.core.reflection.parameter_mapper import ParameterMapper


def resolve(
    annotation: str,
    globals: dict[str, Any] | None = None,
    builtins: dict[str, Any] | None = None,
    locals: dict[str, Any] | None = None
) -> Any:
    if globals: # pragma: no cover
        globals = { **globals , **(builtins or  __builtins__)}

        try:
            result = eval(annotation, globals, locals)
            return result
        except:
            pass

    # fallback
    for frame in stack()[1:]: # pragma: no cover
        if frame.filename == __file__:
            continue

        globals = { **frame.frame.f_globals , **frame.frame.f_builtins}
        locals = frame.frame.f_locals

        try:
            return eval(annotation, globals, locals)
        except:
            pass

    raise Exception(f"Unable to resolve {annotation}") # pragma: no cover




def get_frame(fn: Any, stack: list[FrameInfo], cls: Any | None) -> FrameType | None: # pragma: no cover
    module = None

    if hasattr(fn, "__module__"):
        module = modules[getattr(fn, "__module__")]
    elif cls and hasattr(cls, "__module__"):
        module = modules[getattr(cls, "__module__")]

    if module and hasattr(module, "__file__"):
        for frame in stack:
            if frame.filename == module.__file__:
                frame_locals = frame.frame.f_locals.values()
                if cls is not None and cls in frame_locals:
                    return frame.frame
                elif fn in frame_locals:
                    return frame.frame


def reflect_function(fn: AnyFunction, cls: object | None = None) -> Signature:
    fn = unwrap(fn)
    sig = get_signature(fn)

    if hasattr(fn, "__self__") and ( self := getattr(fn, "__self__") ):
        cls = self

    parameters = list(sig.parameters.values())
    globals: dict[str, Any] | None = getattr(fn, "__globals__") if hasattr(fn, "__globals__") else None
    builtins: dict[str, Any] | None = getattr(fn, "__builtins__") if hasattr(fn, "__builtins__") else None
    locals: dict[str, Any] | None = None

    if frame := get_frame(fn, stack()[1:], cls): # pragma: no cover
        locals = frame.f_locals

    if parameters:
        first_param = parameters[0].name.lower()

        if isinstance(fn, MethodType) and first_param in ("self", "cls"):
            parameters = parameters[1:] # pragma: no cover
        elif first_param in ("self", "cls") and hasattr(fn, "__self__"):
            parameters = parameters[1:] # pragma: no cover
        elif first_param == "self":
            if hasattr(fn, "__call__") and ( call := getattr(fn, "__call__") ): # pragma: no cover
                if hasattr(call, "__text_signature__") and ( text_sig := getattr(call, "__text_signature__") ):
                    if cast(str, text_sig).startswith("($self"):
                        parameters = parameters[1:]

    for index, parameter in enumerate(parameters):
        changed = False

        if isinstance(parameter.annotation, str):
            parameter_type = resolve(parameter.annotation, globals, builtins, locals)
            parameter = parameter.replace(annotation = parameter_type)
            changed = True

        if changed:
            parameters[index] = parameter

    if sig.return_annotation is InspectParameter.empty:
        return_type = Undefined
    elif isinstance(sig.return_annotation, str):
        return_type = resolve(sig.return_annotation, globals, builtins, locals)
    else:
        return_type = sig.return_annotation

    return Signature(
        ParameterMapper(
            [
                Parameter(
                    p.name,
                    ParameterKind(p.kind),
                    Undefined if p.annotation is InspectParameter.empty else p.annotation,
                    Undefined if p.default is InspectParameter.empty else p.default
                ) for p in parameters
            ]
        ), return_type
    )


def get_constructor(cls: type[Any]) -> Signature:
    return reflect_function(getattr(cls, "__init__"), cls)
