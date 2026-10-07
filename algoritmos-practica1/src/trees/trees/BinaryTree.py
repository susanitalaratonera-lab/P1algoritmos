"""Módulo que define la estructura y comportamiento base de un Árbol Binario.

Este módulo proporciona la clase base `BinaryTree` y los enums de soporte para
especificar posiciones de hijos (`Child`) y órdenes de recorrido (`TreeTravelOrder`).
Sirve como fundamento para especializaciones como árboles de búsqueda (BST) y balanceados (AVL).
"""

from __future__ import annotations

import typing
from enum import Enum


class Child(Enum):
    """Enum para identificar la posición de un nodo hijo respecto a su padre.

    Attributes:
        LEFT: Identifica al hijo izquierdo.
        RIGHT: Identifica al hijo derecho.
    """

    LEFT = 0
    RIGHT = 1


class TreeTravelOrder(Enum):
    """Enum que define los órdenes estándar de recorrido en profundidad (DFS).

    Attributes:
        IN_ORDER: Recorrido Inorden (Izquierda, Raíz, Derecha).
        PRE_ORDER: Recorrido Preorden (Raíz, Izquierda, Derecha).
        POST_ORDER: Recorrido Postorden (Izquierda, Derecha, Raíz).
    """

    IN_ORDER = 1
    PRE_ORDER = 2
    POST_ORDER = 3


class BinaryTree[T]:
    """Tipo Abstracto de Datos (TAD) para un Árbol Binario genérico.

    Cada instancia representa tanto un nodo individual como el subárbol del cual es raíz.
    Mantiene referencias bidireccionales: cada nodo conoce a sus hijos izquierdo y derecho,
    así como a su nodo padre directo en la jerarquía.

    Invariantes de estructura:
        - Si un nodo `u` tiene un hijo izquierdo `v`, entonces `v.parent is u`.
        - Si un nodo `u` tiene un hijo derecho `w`, entonces `w.parent is u`.
        - Si un nodo es la raíz del árbol global, su `parent` es `None`.

    Parameters:
        value (T): Dato almacenado en el nodo.
        left (BinaryTree[T] | None, optional): Subárbol izquierdo. Por defecto None.
        right (BinaryTree[T] | None, optional): Subárbol derecho. Por defecto None.
        parent (BinaryTree[T] | None, optional): Nodo padre en el árbol. Por defecto None.
    """

    def __init__(
        self: typing.Self,
        value: T,
        left: typing.Self | None = None,
        right: typing.Self | None = None,
        parent: typing.Self | None = None,
    ) -> None:
        """Inicializa un nodo del árbol binario con enlaces a sus hijos y padre opcionales.

        Complejidad temporal: O(1).
        Complejidad espacial: O(1).
        """
        self.__value: T = value
        self.__parent: typing.Self | None = parent
        self.__left: typing.Self | None = None
        self.__right: typing.Self | None = None

        # Asignamos mediante los setters para asegurar que se enlace el puntero parent en los hijos
        self.left = left
        self.right = right

    @property
    def is_leaf(self: typing.Self) -> bool:
        """Indica si el nodo actual es una hoja (no posee descendientes directos).

        Returns:
            bool: True si carece tanto de hijo izquierdo como derecho, False en caso contrario.

        Complejidad temporal: O(1).
        """
        return self.left is None and self.right is None

    @property
    def is_root(self: typing.Self) -> bool:
        """Indica si el nodo actual es la raíz absoluta de la jerarquía (no tiene padre).

        Returns:
            bool: True si su padre es None, False si desciende de otro nodo.

        Complejidad temporal: O(1).
        """
        return self.parent is None

    @property
    def root(self: typing.Self) -> typing.Self:
        """Obtiene la raíz absoluta del árbol ascendiendo mediante los enlaces de parentesco.

        Returns:
            BinaryTree[T]: El nodo antecesor que no tiene padre (is_root == True).

        Complejidad temporal: O(h), donde h es la profundidad del nodo en el árbol.
        Complejidad espacial: O(h) por la pila de recursión (o O(1) si es iterativo).
        """
        return self if self.is_root else typing.cast(typing.Self, self.parent).root

    @property
    def weight(self: typing.Self) -> int:
        """Calcula el peso del árbol, definido como el número de hojas.

        Returns:
            int: Cantidad total de nodos hoja en el subárbol actual.

        Complejidad temporal: O(n), donde n es el número de nodos del subárbol.
        Complejidad espacial: O(h), donde h es la altura del subárbol por la pila de llamadas.
        """
        if self.is_leaf:
            return 1
        else:
            left_weight = self.left.weight if self.left is not None else 0
            right_weight = self.right.weight if self.right is not None else 0
            return left_weight + right_weight

    @property
    def height(self: typing.Self) -> int:
        """Calcula la altura del subárbol actual medida en número de niveles de nodos.

        Convención adoptada:
            - Un subárbol vacío (None) tiene altura 0.
            - Un nodo hoja individual tiene altura 1.
            - Un árbol general tiene altura 1 + max(altura(izq), altura(der)).

        Returns:
            int: Altura del subárbol (>= 1 para cualquier nodo instanciado).

        Complejidad temporal: O(n), visita recursivamente cada nodo del subárbol.
        Complejidad espacial: O(h), consumo de pila proporcional a la altura.
        """
        left_h = self.left.height if self.left is not None else 0
        right_h = self.right.height if self.right is not None else 0
        return 1 + max(left_h, right_h)

    @property
    def size(self: typing.Self) -> int:
        """Calcula el tamaño del subárbol, definido como el número total de nodos que contiene.

        Returns:
            int: Número total de nodos en el subárbol enraizado en este nodo.

        Complejidad temporal: O(n), donde n es la cantidad de nodos.
        Complejidad espacial: O(h), por la recursión.
        """
        left_size = self.left.size if self.left is not None else 0
        right_size = self.right.size if self.right is not None else 0
        return 1 + left_size + right_size

    @property
    def parent(self: typing.Self) -> typing.Self | None:
        """Referencia al nodo padre inmediato en el árbol, o None si es raíz."""
        return self.__parent

    @parent.setter
    def parent(self: typing.Self, parent: typing.Self | None) -> None:
        """Actualiza el enlace al nodo padre."""
        self.__parent = parent

    @property
    def left(self: typing.Self) -> typing.Self | None:
        """Referencia al subárbol / hijo izquierdo, o None si no existe."""
        return self.__left

    @left.setter
    def left(self: typing.Self, node: typing.Self | None) -> None:
        """Establece el hijo izquierdo, actualizando automáticamente el puntero `parent` del hijo."""
        self.__left = node
        if node is not None:
            node.parent = self

    @property
    def right(self: typing.Self) -> typing.Self | None:
        """Referencia al subárbol / hijo derecho, o None si no existe."""
        return self.__right

    @right.setter
    def right(self: typing.Self, node: typing.Self | None) -> None:
        """Establece el hijo derecho, actualizando automáticamente el puntero `parent` del hijo."""
        self.__right = node
        if node is not None:
            node.parent = self

    @property
    def value(self: typing.Self) -> T:
        """Valor contenido en el nodo actual."""
        return self.__value

    @value.setter
    def value(self: typing.Self, value: T) -> None:
        """Modifica el valor almacenado en el nodo."""
        self.__value = value

    def insert(self: typing.Self, value: T, position: Child) -> typing.Self:
        """Inserta un nuevo nodo como hijo directo del nodo actual en la posición indicada.

        Al tratarse de un árbol binario no ordenado genérico, la inserción se realiza de forma
        explícita especificando la rama deseada (Child.LEFT o Child.RIGHT).

        Args:
            value (T): Dato que se almacenará en el nuevo nodo hijo.
            position (Child): Posición relativa deseada (`Child.LEFT` o `Child.RIGHT`).

        Returns:
            typing.Self: La raíz absoluta del árbol tras efectuar la inserción.

        Raises:
            RuntimeError: Si la posición seleccionada ya está ocupada por otro hijo.

        Complejidad temporal: O(h) debido al ascenso hasta la raíz mediante `self.root`.
        Complejidad espacial: O(1) de memoria auxiliar.
        """
        if position == Child.LEFT and self.left is None:
            self.left = self.__class__(value, parent=self)
        elif position == Child.RIGHT and self.right is None:
            self.right = self.__class__(value, parent=self)
        else:
            raise RuntimeError(f"Trying to insert in {position}, but position is already occupied")

        return self.root

    def travel(
        self: typing.Self,
        order: TreeTravelOrder = TreeTravelOrder.IN_ORDER,
    ) -> list[T]:
        """Realiza un recorrido en profundidad (DFS) del subárbol según el orden solicitado.

        Variantes de recorrido disponibles:
            - `IN_ORDER`: Subárbol izquierdo -> Nodo actual -> Subárbol derecho.
            - `PRE_ORDER`: Nodo actual -> Subárbol izquierdo -> Subárbol derecho.
            - `POST_ORDER`: Subárbol izquierdo -> Subárbol derecho -> Nodo actual.

        Args:
            order (TreeTravelOrder): Estrategia de recorrido a emplear. Por defecto IN_ORDER.

        Returns:
            list[T]: Lista con los valores de los nodos en el orden visitado.

        Complejidad temporal: O(n), visita exactamente una vez cada nodo.
        Complejidad espacial: O(n) para construir la lista resultante + O(h) de pila recursiva.
        """
        left = self.left.travel(order) if self.left is not None else []
        this = [self.value]
        right = self.right.travel(order) if self.right is not None else []

        match order:
            case TreeTravelOrder.IN_ORDER:
                return left + this + right
            case TreeTravelOrder.PRE_ORDER:
                return this + left + right
            case TreeTravelOrder.POST_ORDER:
                return left + right + this

    def __str__(self: typing.Self) -> str:
        """Representación textual legible en formato anidado del subárbol."""
        node = f"{self.value}"
        left = f"{self.left}" if self.left is not None else None
        right = f"{self.right}" if self.right is not None else None

        return f"{self.__class__.__name__}(value = {node}, left = {left}, right = {right})"

    def __iter__(self: typing.Self) -> typing.Iterator[T]:
        return iter(self.travel(TreeTravelOrder.IN_ORDER))