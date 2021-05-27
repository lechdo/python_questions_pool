# encoding:utf-8
"""
Une question de confort.

J'ai un lot de données de paramétrage pour une application, en json. Ce json est considéré trop dynamique et
évolutif pour envisager la création de classes lui correspondant.

Les critères de constructions sont:

 - le contenu de l'objet est un dict-like
 - l'objet doit pouvoir fournir par attribut son contenu : une clé de dict >>> un attribut
 - le modèle des attributs est récursif
 - l'objet doit être un singleton
 - les éléments constituant le code son de type class (on évite les decorators)
 - A la fin, on doit obtenir une simple instanciation d'objet, qui prendra des paramètres au 1er appel

Pour du paramétrage, j'aurai pu capter depuis le json directement les données dans le __init__ de la class. Mais
ce n'est pas l'objectif du script, aussi la dernière situation "tenter d'instancier à nouveau l'objet avec de nouveaux
paramètres" n'est pas prise en compte, une telle action envoie simplement les paramètres au garbage collector,
sans avertissement.

"""
from collections import abc
from keyword import iskeyword


class FrozenJson:
    """
    Get any dict-like object. return any key dict with attribute-like expression.
    """

    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += '_'
            if not key.isidentifier():
                key = 'v_' + key
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJson(self.__data[name])

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

    def __repr__(self):
        return str(self.__data)

    def __str__(self):
        return self.__repr__()


class Singleton(type):
    """
    Meta class to generate singletons.

    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Params(metaclass=Singleton):
    """
    Wrapper for FrozenJson, it can be a singleton without touching FrozenJson.__new__ parameters.

    """
    __slots__ = ("__data",)

    def __init__(self, data=None):
        self.__data = FrozenJson(data)

    def __getattr__(self, name):
        return getattr(self.__data, name)

