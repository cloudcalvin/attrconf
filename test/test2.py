import inspect 
import attr

from fluxutil.dictify import dictify, strict
from fluxutil.print_function import print_function

from attrconf import config_node

from pprint import pprint
from typing import Optional, List, Union, Dict, Tuple, DefaultDict, Any


def handler(helloEvent: HelloEvent):
    hello(name = helloEvent.name, surname = helloEvent.surname)
    hello(**helloEvent)

def hello(name: string, surname: string, thir =  ):
    raise NameError


# global get_technology
Layer = Tuple[int, int]

@strict
class LayerMap:
    def reverse_lookup(self, layer: Layer):
        assert type(layer) is tuple
        _dict = attr.asdict(self, retain_collection_types=True)
        for k, v in list(_dict.items()):
            print("key: ", k)
            print("valeu: ", v)
            if(v == layer):
                return k
        raise NameError

    # def reverse_lookup(self, layer: Layer):
    #     for key, value in self.items():
    #         if layer == value:
    #             return key

@strict
class ProcessProperties:
    IC          : Optional[Union[float, int]] = None
    IC_LEN      : Optional[Union[float, int]] = None
    DESCRIPTION : str
    THICKNESS   : Union[float, int] 
    LAMBDA      : Optional[Union[float, int]] = None
    ORDER       : int 
    MASK        : Optional[int] = None
    FILMTYPE    : str
    HFILAMENTS  : Optional[int] = None


MinSpaceToDefaultDict = DefaultDict[Tuple[int, int],  Any]
MinSpaceToDict = Dict[Tuple[int, int],  Union[Union[float, int], Dict[str, Union[float, int]]]]


MIN_SPACE_TO__DEFAULTS : MinSpaceToDict = dict()

T = Tuple[int, int]
U = Union[float, Dict[str, float]]

def min_space_to(tuples : List[Tuple[T, U]]) -> MinSpaceToDict: 
    return {**MIN_SPACE_TO__DEFAULTS, **dict(tuples)}

@strict
class ProcessConstraints:
    MIN_DENSITY       : Optional[Union[float, int]] = None
    MAX_LOCAL_DENSITY : Optional[Union[float, int]] = None
    MIN_SIZE          : Optional[Union[float, int]] = None
    MAX_SIZE          : Optional[Union[float, int]] = None
    MIN_OVERLAP       : Optional[Union[float, int]] = None
    MIN_SPACE_TO      : MinSpaceToDict = dict()
    MIN_SPACE         : Optional[Union[float, int]] = None
    MIN_SPACING       : Optional[Union[float, int]] = None
    MIN_SURROUND      : Optional[Union[float, int]] = None
    MIN_SURROUND_BY   : Dict[Layer, Union[float, int]] = dict()
    MIN_SURROUND_OF   : Dict[Layer, Union[float, int]] = dict()
    MAX_SURROUND_BY   : Dict[Layer, Union[float, int]] = dict()
    MAX_SURROUND_OF   : Dict[Layer, Union[float, int]] = dict()
    NOFILL            : Optional[Union[float, int]] = None
    GRIDSIZE          : Optional[int] = None
    SPACING           : Optional[Union[float, int]] = None

@strict
class ProcessLayerTree:
    pass

@strict
class ProcessRuleTree:
    MIN_SPACE_TO__DEFAULTS : MinSpaceToDict = MIN_SPACE_TO__DEFAULTS
    SCALE_FACTOR : Union[float, int] = 1000


@strict
class Base:
    A : int = 3
    B : str 

@strict
class Base2:
    A : int = 3
    BASE : Base

# try:
#     @config_node
#     class NODE_BROKEN:
#         A : int = 3
#         B : str 
# except:
#     pass

@config_node
class INHERITED(Base):
    B  = '5'


@config_node
class INHERITED2(Base):
    B = "asdf"

pprint(Base.__attrs_attrs__)
pprint(INHERITED.__attrs_attrs__)
pprint(INHERITED2.__attrs_attrs__)

# exit()

@config_node
class BASE:
    A = 123
    B = "base"

@config_node
class DERIVED(Base):
    A = 1
    B = "base derived"

@config_node
class DERIVED2(Base2):
    A = 2
    B = "base2 derived"
    BASE = Base(B="asdf")

# BASE2 = Base2(B)

pprint(DERIVED.__dict__)

# print(BASE2.A)
# print(BASE2.BASE)

# print(NODE_BROKEN.A)
# print(NODE_BROKEN.B)

print(DERIVED.A)
print(DERIVED.B)
print(DERIVED2.A)
print(DERIVED2.B)
DERIVED2.BASE = BASE
print(DERIVED2.BASE.A)
print(DERIVED2.BASE['A'])


@config_node
class ROOT:

    @config_node
    class NESTED_DERIVED(Base):
        A = 7
        B = "hello"
    
    DERIVED2 = DERIVED2

    @config_node
    class NESTED_DERIVED2(Base2):
        A = 12
        B = "world"
        BASE = DERIVED
        
    
    
print(ROOT.NESTED_DERIVED.A)
print(ROOT.NESTED_DERIVED.B)
print(ROOT.DERIVED2.A)
print(ROOT.DERIVED2.B)
print(ROOT.DERIVED2.BASE)
print(ROOT.DERIVED2.BASE.A)
print(ROOT.DERIVED2.BASE.B)
print(ROOT.NESTED_DERIVED2.A)
print(ROOT.NESTED_DERIVED2.B)
print(ROOT.NESTED_DERIVED2.BASE)
print(ROOT.NESTED_DERIVED2.BASE.A)
print(ROOT.NESTED_DERIVED2.BASE.B)

MinSpaceToDict = Dict[Tuple[int, int],  Union[float, Dict[str, float]]]


@config_node
class CONFIG:
    
    @config_node
    class PROCESS(ProcessLayerTree):
        
        @config_node
        class M0(ProcessProperties):
            IC          = 2
            IC_LEN      = 2
            DESCRIPTION = "asd"
            THICKNESS   = 2
            LAMBDA      = 2
            ORDER       = -1
            MASK        = 0
            FILMTYPE    = "asd"

    @config_node
    class RULES(ProcessRuleTree):
        SCALE_FACTOR = 1000
        MIN_SPACE_TO__DEFAULTS: MinSpaceToDict = dict()

        @config_node
        class M0(ProcessConstraints):
            MIN_SIZE = 0.5
            MAX_SIZE = 20.0
            MIN_DENSITY = 15.0
            MIN_SPACE_TO : MinSpaceToDict = min_space_to([
                    ((0 , 3), {"short": 0.5}),
                    ((0 , 3), {"long": 1.0}),
                ])
            MIN_SURROUND_OF : Dict[Layer, float] = dict([ 
                    ((0, 5) , 0.30)
                ])
            MAX_LOCAL_DENSITY = 85.0
            MAX_GLOBAL_DENSITY = 80.0
            GRIDSIZE = 25


print(CONFIG.PROCESS.M0.IC)
print(CONFIG.RULES.M0.MIN_SIZE)
print_function(CONFIG.RULES.__init__)
print(CONFIG.RULES.__dict__)
print(CONFIG.RULES.SCALE_FACTOR)

