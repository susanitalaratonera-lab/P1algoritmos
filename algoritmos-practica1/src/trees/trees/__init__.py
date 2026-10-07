import typing


class Comparable(typing.Protocol):
    def __lt__(self: typing.Self, other: typing.Self, /) -> bool:
        ...

    def __gt__(self: typing.Self, other: typing.Self, /) -> bool:
        ...

    def __eq__(self: typing.Self, other: typing.Self, /) -> bool:
        ...


from .AVLTree import AVLTree
from .BinarySearchTree import BinarySearchTree
from .BinaryTree import BinaryTree, Child, TreeTravelOrder
from .Node import Node

__all__ = [
    "AVLTree",
    "BinarySearchTree",
    "BinaryTree",
    "Child",
    "Node",
    "TreeTravelOrder",
]
