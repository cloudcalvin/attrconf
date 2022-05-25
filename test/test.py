import attr
import inspect

from pprint import pprint 

from attrs_strict import type_validator
from functools import wraps, partial
from typing import List
from fluxutil.functional import compose

from attrconf import config_node

@config_node
class Outer:
    @config_node
    class Inner:
        M0 : str = "m0"
        # M0 : str = attr.ib(default="m0")

    def print(self):
        print(self.__class__.__dict__)
        # print(inspect.getmembers(self))
    # some_setting: str = attr.ib(default="setting")
    some_setting: str = "setting"


@attr.s(auto_attribs=True)
class Inner:
    M0 : str = attr.ib(default="m0")

@attr.s(auto_attribs=True)
class Outer2:
    @attr.s(auto_attribs=True)
    class Inner2:
        M0 : str = attr.ib(default="m0")
    some_setting: str = attr.ib(default="setting")

print("testing")
print(type(Outer.__class__))
print(type(Outer2))
print(type(Outer2().__class__))
# print(attr.asdict(Outer, recurse=True))
print(Outer.__dict__)
# print(Outer.Inner.__dict__)
# print(getattr(Outer, "Inner").__dict__)
# print(Outer.Inner.M0)
# print(attr.asdict(Outer(), recurse=True, retain_collection_types=True))
print(Outer.keys())
print(Outer.values())
print(Outer.items())
print("done")


class Outer3:
    class Inner:
        M0 : str ="m0"
    some_setting: str ="setting"

# print(Outer3.Inner.outer)