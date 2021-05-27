# encoding: utf-8
"""
Le magic square. La question était "comment créer un code qui certifie qu'un carré est magique". Un test unitaire
à mon sens donc. J'ai d'abord pensé "il me faut une liste de carrés magiques pour éprouver la vérification".

Voici une classe permettant d'en construire un. Elle hérite de la classe collection.UserList pour le confort
d'utilisation, notamment au niveau du slicing.

La construction de l'instance se fait depuis une valeur "side", le coté du carré, et un "base_number" optionnel, qui
détermine la valeur de départ dans le carré.

La ventilation des données depuis ces deux paramètres jusqu'aux carrés se fait via un générateur, selon trois règles
de constructions prises comme axiomes :

 - on commence par le milieu de la ligne supérieure, le coté du carré doit donc être impair
 - on incrémente le carré supérieur droit de 1. Si on atteint une extrémité on reprend depuis le coté opposé.
 - si le carré supérieur droit est déjà ventilé, on incrémente le carré inférieur.

"""

from random import randint
from collections import namedtuple, UserList

Position = namedtuple('Position', 'row column')


class MagicSquare(UserList):
    """
    Construit un magic square.

    Le coté est la valeur de référence pour sa construction. Le basenumber est altenatif et permet
    de déterminer la plus petite valeur dans le carré.

    Les données doivent être des ints de valeur strictement positives.
    L'algorithme du magic square est tiré du site :
    https://www.logamaths.fr/carres-magiques-une-methode-simple-pour-creer-un-carre-magique-mathematique-de-toute-taille/

    """

    def __init__(self, side, base_number=None):
        assert int(side) % 2, "The side must be odd."
        self.base_number = int(base_number) if base_number else randint(1, 100)
        self.side = int(side)
        super().__init__([[None for _ in range(self.side)] for _ in range(self.side)])
        self.__populate()

    def __populate(self):
        initial_position = Position(0, int(self.side / 2))
        number = self.base_number

        for position in self.__position_generator(initial_position):
            self[position.row][position.column] = number
            number +=1

    def __position_generator(self, initial_pos):
        current_case = initial_pos

        for _ in range(self.side ** 2):
            yield current_case
            up_right = Position((current_case.row - 1) % self.side, (current_case.column + 1) % self.side)
            down = Position((current_case.row + 1) % self.side, current_case.column)
            if not self[up_right.row][up_right.column]:
                res = up_right
            else:
                res = down
            current_case = res
        return

    def pretty_repr(self):
        head, tail = f'{" ___" * self.side}\n', f'{" ---" * self.side}\n'
        row_format = f'{"|{:3}" * self.side}|\n'
        res = str()
        for row in range(self.side):
            res += row_format.format(*self[row])
        return head + res + tail


if __name__ == '__main__':
    c = MagicSquare(5, 41)
    print(c.pretty_repr())
