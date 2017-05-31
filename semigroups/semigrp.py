'''
This module contains classes for representing semigroups.
'''
# pylint: disable = no-member, protected-access, invalid-name, len-as-condition

import libsemigroups
from semigroups.elements import Transformation
from libsemigroups import ElementABC, PythonElementNC


class Semigroup(libsemigroups.SemigroupNC):
    r'''
    A *semigroup* is a set :math:`S`, together with a binary operation :math:`*
    :S\times S\to S`, such that :math:`S` is *associative* under :math:`*`,
    that is :math:`\forall a, b, c \in S \quad a * (b * c) = (a * b) * c`.

    Let :math:`S` is a semigroup and :math:`X\subseteq S`. The *semigroup
    generated by* :math:`X` is defined as the set of all product of elements
    of :math:`X`, together with the same operation. The elements of :math:`X`
    are called the *generators*.

    This class allows semigroups generated by sets to be represented in Python.

    Args:
        args (list):   The generators of the semigroup.

    Raises:
        ValueError: If no arguments are given.

    Examples:
        >>> from semigroups import *
        >>> S = Semigroup(Transformation([1, 2, 0]),
        ... Transformation([2, 1, 0]))
        >>> # the symmetric group
        >>> S.size()
        6
        >>> Transformation([0, 1, 2]) in S
        True
        >>> Transformation([0, 1, 0]) in S
        False
        >>> # To find the generators
        >>> S[0], S[1]
        (Transformation([1, 2, 0]), Transformation([2, 1, 0]))
    '''

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], list):
            self.__init__(*args[0])
            return
        elif len(args) == 0:
            raise ValueError('there must be at least 1 argument')
        elif not all(map(lambda elt: isinstance(elt, type(args[0])), args)):
            raise TypeError('generators must be of the same type')

        err_msg = 'generators must have a multiplication defined on them'
        x = args[0]
        if not isinstance(x, ElementABC):
            try:
                x * x
            except:
                raise TypeError(err_msg)

        gens = [g if (isinstance(g, ElementABC) and str(type(g)) !=
                      "<class 'semigroups.semifp.FPSOME'>")
                else PythonElementNC(g) for g in args]
        libsemigroups.SemigroupNC.__init__(self, gens)

def FullTransformationMonoid(n):
    r'''
    A semigroup :math:`S` is a *moniod* if it has an *identity* element. That
    is, an element :math:`e\in S` such that :math:`ea = ae = a \quad \forall a
    \in S`.

    Let :math:`n\in\mathbb{N}`. The set of all transformations of degree
    :math:`n` forms a monoid, called the *full transformation monoid*.

    This function returns the full transformation monoid of degree :math:`n`,
    for any given :math:`n\in\mathbb{N}`.

    Args:
        n (int):    The degree of the full transformation monoid.

    Returns:
        semigroups.semigrp.Semigroup: The full transformation monoid.

    Raises:
        TypeError:  If the degree is not an int.
        ValueError: If the degree is not positive.

    Examples:
        >>> from semigroups import FullTransformationMonoid
        >>> S = FullTransformationMonoid(3)
        >>> S.size()
        27
    '''
    if not isinstance(n, int):
        raise TypeError('degree of transformation must be an int')
    if n < 1:
        raise ValueError('degree of transformation must be positive')

    if n == 1:
        return Semigroup(Transformation([0]))
    elif n == 2:
        return Semigroup(Transformation([1, 0]), Transformation([0, 0]))

    return Semigroup([Transformation([1, 0] + list(range(2, n))),
                      Transformation([0, 0] + list(range(2, n))),
                      Transformation([n - 1] + list(range(n - 1)))])
