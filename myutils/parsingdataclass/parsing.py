from dataclasses import dataclass
import regex
from typing import Callable, get_type_hints, get_args, Any

GenericAliasClass = type(list[int])
UnionTypeClass = type(int | None)
NoneTypeClass = type(None)


class ParsingException(Exception):
    pass


def parsing(pattern: str):
    """ This is a decorator for a class (declared like a dataclass would be) that serves
    the purpose of changing the source class' constructor into a new one, which accepts a
    string.

    If a field is marked as T | None, it will receive value none if the group failed to match 
    and instance of T otherwise. If a field is marked as list[T], all matches of its respective
    group will be collected into a list. If a field is marked as just T, its respective group
    needs to match exactly once.

    Any failures to parse the given string will result in a :class:`ParsingException`.

    Args:
        pattern (regex.Pattern): pattern, whose respective groups match to this class'
        attributes. 
    """

    def __decorator(cls):
        dataclass(cls)

        def init_generator(previousinit: Callable[[Any, str], None]):
            def newInit(self, input: str):
                m: regex.Match[str] | None = regex.fullmatch(pattern, input)
                annotations: dict = cls.__annotations__
                if m is None:
                    raise ParsingException(f"Matching failed for string {repr(input)} and pattern {repr(pattern)}")
                _re_group_count = len(m.allcaptures()) - 1
                if _re_group_count != len(annotations.values()):
                    raise ParsingException(
                        f"The regex has {_re_group_count} groups but the class has only {len(annotations.values())} fields."
                    )
                fullitr = iter(m.allcaptures())
                "Iterator over groups of a match"
                next(fullitr)  # skip the first match - which matches the whole string
                args = []
                # iterate over all annotations in a class and over all 
                for attrname, typename in annotations.items():
                    value: list[str] = next(fullitr)  # value - list of matches for that group
                    _type: type = get_type_hints(cls)[attrname]
                    if isinstance(_type, GenericAliasClass):
                        # this group was declared to be quantifiable 
                        typelist: tuple[type] = get_args(_type)
                        if len(typelist) != 1:
                            raise ParsingException(f"Annotation {typename} does not have exactly one parameter")
                        innertype = typelist[0]
                        args.append([innertype(x) for x in value])
                    elif isinstance(_type, UnionTypeClass):
                        # this group was declared to be nullable 
                        # digression: how would one replace Java/SQL lingo? (None-able??)
                        if len(value) > 1:
                            raise ParsingException(
                                f"Group representing a nullable type should match 1 or 0, not {len(value)} times.")
                        uniontypes = get_args(_type)
                        if len(uniontypes) != 2 or NoneTypeClass not in uniontypes:
                            raise ParsingException("Only union types of a type and None are supported")
                        realtype = uniontypes[int(uniontypes[0] == None)]  # the non-None type
                        if len(value) == 0:
                            args.append(None)
                        else:
                            args.append(realtype(value[0]))
                    else:
                        # this group was declared to be not quantifiable and not nullable
                        if (len(value)) != 1:
                            raise ParsingException(
                                "Annotation that is not quantifiable nor nullable should exactly one item.")
                        args.append(_type(value[0]))

                previousinit(self, *args)

            return newInit

        cls.__init__ = init_generator(cls.__init__)
        return cls

    return __decorator

# possibility matrix:
#
#       |  0  |  1  | 2++ | <-- how many substrings were matched
# ------|-----|-----|-----| 
# maybe |  +  |  +  |  !  | <-- T | None           
# one   |  !  |  +  |  !  | <-- T
# many  |  +  |  +  |  +  | <-- list[T]
# ------|-----|-----|-----|     ^^^^^^^  where T is a type that has a
# ^                             constructor taking exactly one string   
# |       + ok, ! not ok         
# |
# with which quantity was this field annotated