"""Comando del intérprete para imprimir la estructura del árbol."""

from __future__ import annotations

from ..trees import AVLTree, Comparable

import builtins     #lo importamos para que no sea una función recursiva (al escribir print estaría llamándose la función a si misma.)


def print[T: Comparable](tree: AVLTree[T]) -> AVLTree[T]:
    """Imprime por consola la representación del árbol actual.

    Debe imprimir un mensaje con el patron TREE CONTENT: AVLTree(value = ..., left = ..., right = ...). Ejemplo:
        TREE CONTENT: AVLTree(value = 2, left = AVLTree(value = 1, left = None, right = None) right = AVLTree(value = 3, left = None, right = None))

    Importante: Retorna el árbol intacto para preservar el estado en el intérprete.

    Sintaxis en el script:
        PRINT

    Args:
        tree (AVLTree[T]): Árbol actual en memoria.

    Returns:
        AVLTree[T]: La misma referencia al árbol recibida.
    """
    # TODO: [Práctica Alumno]
    if tree is None:
        builtins.print("NO TREE FOUND")
    else:
        builtins.print(f"TREE CONTENT: {tree}")

    return tree