import sys
import attr
import inspect
import types
import linecache

from pprint import pprint

from attr import NOTHING, _config
from attrs_strict import type_validator
from typing import List
from types import FunctionType
from fluxutil.print_function import print_function
from fluxutil.functional import compose
from functools import partial, wraps # This convenience func preserves name and docstring


def _create_init_script(init_name, args, lines):
    """
    Template for the __init__ method
    """
    return (
        """\
def {init_name}(self, {args}):
    {lines}
""".format(
            init_name=init_name,
            args=args,
            lines="\n    ".join(lines) if lines else "pass",
        )
    )


def _attrs_init_replace(cls):
    """
        Create a new __init__ method to replace the __init__ that is generated by attr.s 
        Our __init__ inherits the attribute defaults from parent classes that have attributes
    """

    attrs = cls.__attrs_attrs__
    init_attrs = [a for a in attrs if a.init]
    non_defaults = [a for a in init_attrs if a.default == attr.NOTHING]
    defaults = [a for a in init_attrs if a.default != attr.NOTHING]

    init_args = ("*args" + (", " if len(non_defaults) != 0 else "") 
        ) + ", ".join([
            f"{a.name}" for a in non_defaults
        ]) + (", " if len(defaults) else "") +  ", ".join([
            f"{a.name}=attr_dict['{a.name}'].default" for a in defaults
        ])
    init_body = ([
            f"self.{a.name} = {a.name}" for a in attrs
        ] + ([
            # TODO : fix "if _config._run_validators is True:"
            "if True is True:" 
            ] if (len(attrs) != 0) else []
        ) + [
            f"    __attr_validator_{a.name}(self, __attr_{a.name}, self.{a.name})" for a in attrs
        ]) if len(attrs) != 0 else []

    init_script = _create_init_script("__init__", init_args, init_body)

    globs = {}
    attr_dict = {}  
    annotations = {}

    for a in attrs:
        arg_name = a.name.lstrip("_")

        if a.type is not None and a.converter is None:
            annotations[arg_name] = a.type

        if not a.init and a.default is NOTHING:
            continue

        attr_dict[a.name] = a
        val_name = "__attr_validator_" + a.name
        attr_name = "__attr_" + a.name
        globs[val_name] = a.validator
        globs[attr_name] = a

    unique_filename = attr._make._generate_unique_filename(cls, "init")
    if cls.__module__ in sys.modules:
        # This makes typing.get_type_hints(CLS.__init__) resolve string types.
        globs.update(sys.modules[cls.__module__].__dict__)

    globs.update({"NOTHING": NOTHING, "attr_dict": attr_dict})

    init = attr._make._make_method(
        "__init__",
        init_script,
        unique_filename,
        globs
    )

    init.__annotations__ = annotations
    
    cls.__init__ = types.MethodType(init, cls)

    return cls


def _inner_classes_list(cls):
    """
    Get list of classes defined within this class
    """

    inner_classes = [(attr_name, attr_value) 
        for attr_name, attr_value in  dict(inspect.getmembers(cls)).items()
            if inspect.isclass(attr_value) and not attr_name.startswith("__")]

    return inner_classes


def attach(
    target,
):  
    def wrapper(func):
        setattr(target, func.__name__, func)
        return target
    return wrapper


def _dictify(
    cls,
    parent=None
):
    """
    Make a attr class' attributes and inner classes accessible like with a dict
    """

    setattr(cls, "__inner_classes__", {})
    for name, value in _inner_classes_list(cls):
        cls.__inner_classes__[name] = value
        setattr(cls, name, value())

    @wraps(cls)
    def wrap(cls):

        def _attributes(self):
            return dict(attr.asdict(self, retain_collection_types=True), **self.__class__.__inner_classes__)
        
        @attach(cls)
        def keys(self):
            return _attributes(self).keys()
        
        @attach(cls)
        def values(self):
            return _attributes(self).values()
        
        @attach(cls)
        def items(self):
            return _attributes(self).items()
        
        @attach(cls)
        def __getitem__(self, key):
            return getattr(self, key)
        
        @attach(cls)
        def __setitem__(self, key, value):
            setattr(self, key, value)
        
        return cls
    return wrap(cls)


def config_node(
    maybe_cls,
    *args,
    field_validator=type_validator,
    **kwargs
):
    '''
    '''
    
    # to allow usage without arguments
    if maybe_cls is None:
        return partial(config_node, maybe_cls, *args, field_validator=type_validator, **kwargs)
        
    def _validation_hook(cls: type, fields: List[attr.Attribute]) -> List[attr.Attribute]:
        results = []
        for f in fields:
            results.append(f.evolve(validator=field_validator()))
        return results

    def _default_update_hook(cls: type, fields: List[attr.Attribute]) -> List[attr.Attribute]:
        results = []
        for f in fields:
            if f.name in cls.__dict__.keys():
                results.append(f.evolve(default=cls.__dict__[f.name]))
            else:
                results.append(f)
        return results

    def _transform_hook(cls: type, fields: List[attr.Attribute]) -> List[attr.Attribute]:
        fields = _validation_hook(cls, fields)
        fields = _default_update_hook(cls, fields)
        return fields

    @wraps(maybe_cls)
    def wrap(cls):
        names = cls.__qualname__.split(".")
        has_outer = False
        if len(names) > 1:
            has_outer = True

        cls = compose(
                _attrs_init_replace,
                _dictify
            )(
                attr.s(
                    cls,
                    *args,
                    auto_attribs=True,
                    field_transformer=_transform_hook,
                    init=True,
                    collect_by_mro=True,
                    kw_only=True,
                    **kwargs)
            )

        if has_outer:
            return cls
        else:
            obj = cls()
            return obj

    return wrap(maybe_cls)