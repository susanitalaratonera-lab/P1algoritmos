"""Módulo que implementa un Árbol Binario de Búsqueda (ABB / BST).

Extiende `BinaryTree` imponiendo la propiedad de ordenación binaria
sobre los elementos contenidos en los nodos.
"""

from __future__ import annotations

import typing

from . import Comparable
from .BinaryTree import BinaryTree


class BinarySearchTree[T: Comparable](BinaryTree[T]):
    """Árbol Binario de Búsqueda (Binary Search Tree - BST).

    Especialización de `BinaryTree` donde los elementos se organizan según la
    invariante de ordenación:
        - Para todo nodo `u`, todos los nodos `v` en su subárbol izquierdo satisfacen `v.value < u.value`.
        - Para todo nodo `u`, todos los nodos `w` en su subárbol derecho satisfacen `w.value > u.value`.
        - En esta implementación no se admiten elementos con claves duplicadas.

    Parameters:
        value (T): Valor del nodo.
        left (BinarySearchTree[T] | None, optional): Subárbol izquierdo. Por defecto None.
        right (BinarySearchTree[T] | None, optional): Subárbol derecho. Por defecto None.
        parent (BinarySearchTree[T] | None, optional): Nodo padre. Por defecto None.
    """

    def __init__(
        self: typing.Self,
        value: T,
        left: typing.Self | None = None,
        right: typing.Self | None = None,
        parent: typing.Self | None = None,
    ) -> None:
        """Inicializa un nodo del árbol binario de búsqueda."""
        super().__init__(value, left, right, parent)

    def __contains__(self: typing.Self, value: T) -> bool:
        """Determina si un determinado valor existe dentro del subárbol.

        Aprovecha la propiedad de búsqueda binaria para descartar la mitad del árbol
        en cada comparación si el árbol está balanceado.

        Args:
            value (T): Valor o clave buscada.

        Returns:
            bool: True si el valor está presente, False en caso contrario.

        Complejidad temporal:
            - Mejor caso: O(1) si el valor coincide con la raíz.
            - Caso promedio: O(log n) en árboles aleatorios/balanceados.
            - Peor caso: O(n) si el árbol está degenerado en lista enlazada.
        Complejidad espacial: O(h) por llamadas recursivas, donde h es la altura.
        """
        if self.value == value:
            return True
        elif value < self.value and self.left is not None:
            return value in self.left
        elif value > self.value and self.right is not None:
            return value in self.right
        else:
            return False

    def find(self: typing.Self, value: T) -> typing.Self | None:
        """Localiza y retorna la referencia al nodo que contiene el valor especificado.

        Args:
            value (T): Valor buscado.

        Returns:
            BinarySearchTree[T] | None: El nodo que almacena dicho valor, o None si no existe.

        Complejidad temporal: O(h), donde h es la altura del árbol (O(log n) promedio, O(n) peor).
        Complejidad espacial: O(h) de pila recursiva.
        """
        if self.value == value:
            return self
        elif value < self.value and self.left is not None:
            return self.left.find(value)
        elif value > self.value and self.right is not None:
            return self.right.find(value)
        return None

    def insert(self: typing.Self, value: T) -> typing.Self:
        """Inserta un nuevo valor en la posición que preserva la propiedad de búsqueda binaria.

        Si el valor ya está presente, la operación no realiza ninguna modificación
        (no se permiten claves duplicadas).

        Args:
            value (T): Valor a insertar en el árbol.

        Returns:
            typing.Self: La raíz absoluta del árbol tras la inserción.

        Complejidad temporal: O(h), recorre una única rama hasta encontrar el punto de inserción.
        Complejidad espacial: O(h) por la recursión.
        """
        if value not in self:
            if value < self.value:
                if self.left is None:
                    self.left = self.__class__(value=value, parent=self)
                else:
                    self.left.insert(value)
            elif value > self.value:
                if self.right is None:
                    self.right = self.__class__(value=value, parent=self)
                else:
                    self.right.insert(value)

        # Retorna la raíz absoluta del árbol
        return self.root

    def remove(self: typing.Self, value: T) -> typing.Self | None:
        """Elimina el nodo que contiene el valor dado conservando la invariante del ABB.

        El algoritmo contempla tres casos estructurales:
            1. **Nodo hoja**: Se desvincula directamente de su padre. Si era la raíz única, el árbol queda vacío (None).
            2. **Nodo con un único hijo**: Dicho hijo asciende y toma el lugar del nodo eliminado,
               enlazándose adecuadamente con el padre.
            3. **Nodo con dos hijos**: Se localiza su sucesor inorden (el nodo con menor clave
               del subárbol derecho), se copia su valor en el nodo actual y se elimina
               el sucesor original (que tendrá a lo sumo un hijo derecho).

        Args:
            value (T): Valor a eliminar.

        Returns:
            BinarySearchTree[T] | None: La nueva raíz del árbol, o None si el árbol quedó vacío.

        Complejidad temporal: O(h), donde h es la altura del árbol.
        Complejidad espacial: O(h) para la búsqueda y localización del sucesor.
        """
        if value not in self:
            return self.root

        target = self.find(value)
        if target is None:
            return self.root

        parent = target.parent

        # Caso 1: El nodo a eliminar es una hoja
        if target.is_leaf:
            if parent is None:
                # El árbol constaba únicamente de este nodo
                return None
            if target == parent.left:
                parent.left = None
            else:
                parent.right = None
            return self.root

        # Caso 2a: El nodo tiene únicamente hijo izquierdo
        elif target.left is not None and target.right is None:
            child = target.left
            if parent is None:
                child.parent = None
                return child
            if target == parent.left:
                parent.left = child
            else:
                parent.right = child

            return child.root

        # Caso 2b: El nodo tiene únicamente hijo derecho
        elif target.left is None and target.right is not None:
            child = target.right
            if parent is None:
                child.parent = None
                return child
            if target == parent.left:
                parent.left = child
            else:
                parent.right = child

            return child.root

        # Caso 3: El nodo tiene dos hijos
        # Localizamos el sucesor inorden (nodo con valor mínimo del subárbol derecho)
        else:
            replacement = typing.cast(typing.Self, target.right)
            while replacement.left is not None:
                replacement = replacement.left

            # Copiamos el valor del sucesor inorden al nodo actual
            target.value = replacement.value

            # Eliminamos recursivamente el nodo sucesor (que ahora está duplicado)
            # Nótese que replacement a lo sumo tiene hijo derecho
            replacement_parent = typing.cast(typing.Self, replacement.parent)
            replacement_child = replacement.right

            if replacement == replacement_parent.left:
                replacement_parent.left = replacement_child
            else:
                replacement_parent.right = replacement_child

            return self.root
