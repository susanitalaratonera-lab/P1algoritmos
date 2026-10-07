"""Módulo que define el esqueleto de un Árbol AVL.

Un Árbol AVL es un árbol binario de búsqueda auto-balanceable donde la diferencia
de alturas entre los subárboles izquierdo y derecho de cualquier nodo (factor de equilibrio)
nunca difiere en más de una unidad.

Complejidades garantizadas:
    - Búsqueda: O(log n) en el peor caso.
    - Inserción: O(log n) en el peor caso.
    - Eliminación: O(log n) en el peor caso.
"""

from __future__ import annotations

import typing

from . import Comparable
from .BinarySearchTree import BinarySearchTree


class AVLTree[T: Comparable](BinarySearchTree[T]):
    """Árbol Binario de Búsqueda Auto-balanceado (Árbol AVL).

    Invariante AVL:
        Para todo nodo `u` del árbol:
            |altura(u.derecho) - altura(u.izquierdo)| <= 1

    Convención del Factor de Equilibrio (FE / Balance Factor):
        FE(u) = altura(u.derecho) - altura(u.izquierdo)
        - FE in {-1, 0, 1}: Nodo balanceado.
        - FE > 1: Nodo desbalanceado con sobrecarga en el subárbol derecho.
        - FE < -1: Nodo desbalanceado con sobrecarga en el subárbol izquierdo.

    Parameters:
        value (T): Valor almacenado.
        left (AVLTree[T] | None, optional): Subárbol izquierdo.
        right (AVLTree[T] | None, optional): Subárbol derecho.
        parent (AVLTree[T] | None, optional): Nodo padre.
    """

    def __init__(
        self: typing.Self,
        value: T,
        left: typing.Self | None = None,
        right: typing.Self | None = None,
        parent: typing.Self | None = None,
    ) -> None:
        """Inicializa un nodo del árbol AVL."""
        super().__init__(value, left, right, parent)

    @property
    def balance(self: typing.Self) -> int:
        """Calcula el factor de equilibrio (FE) del nodo actual.

        Fórmula:
            FE = altura(hijo_derecho) - altura(hijo_izquierdo)
            (Un subárbol inexistente / None tiene altura 0).

        Returns:
            int: Factor de equilibrio del nodo.

        Complejidad temporal: O(n) si height recorre el subárbol (o O(1) si la altura se almacena en el nodo).
        """
        return (self.right.height if self.right else 0) - (self.left.height if self.left else 0)

    def insert(self: typing.Self, value: T) -> typing.Self:
        """Inserta un nuevo valor en el árbol AVL y reestablece el balance si es necesario.

        Pasos del algoritmo:
            1. Realizar la inserción estándar de un ABB (super().insert(value)).
            2. Localizar el nodo recién insertado.
            3. Ascender a través de los enlaces `parent` comprobando el factor de equilibrio.
            4. En el primer nodo donde |balance| > 1, determinar el tipo de desbalance
               y aplicar la rotación correspondiente:
               - Izquierda-Izquierda (LL): rotación simple a la derecha.
               - Derecha-Derecha (RR): rotación simple a la izquierda.
               - Izquierda-Derecha (LR): rotación doble (izq en hijo, der en nodo).
               - Derecha-Izquierda (RL): rotación doble (der en hijo, izq en nodo).
            5. Retornar la raíz absoluta del árbol resultante.

        Args:
            value (T): Valor a insertar.

        Returns:
            AVLTree[T]: La raíz del árbol tras la inserción y el posible rebalanceo.

        Complejidad temporal: O(log n) garantizado.
        """
        # 1 y 2. Inserción estándar de un ABB, localizando a la vez el nodo insertado.
        # Se hace de forma iterativa: super().insert() llama recursivamente a insert()
        # sobre los hijos, que al ser AVLTree volverían a ejecutar este método y
        # rebalancear en cada nivel, dejando `self` fuera de la raíz tras una rotación.
        parent = self.root
        while True:
            if value == parent.value:
                # Clave duplicada: no se modifica el árbol
                return parent.root
            if value < parent.value:
                if parent.left is None:
                    parent.left = self.__class__(value=value, parent=parent)
                    current = parent.left
                    break
                parent = parent.left
            else:
                if parent.right is None:
                    parent.right = self.__class__(value=value, parent=parent)
                    current = parent.right
                    break
                parent = parent.right

        # 3. Ascendemos comprobando el factor de equilibrio
        while current is not None:
            fe = current.balance

            # 4. Determinamos el desbalance y aplicamos la rotación que corresponda
            # Desbalance hacia la izquierda (fe < -1)
            if fe < -1:
                #Caso ID
                if current.left and current.left.balance > 0:
                    current = current.__rotate_left_right()
                #Caso II
                else:
                    current = current.__rotate_right()

            #Desbalance hacia la derecha (fe > 1)
            elif fe > 1:
                #Caso DI
                if current.right and current.right.balance < 0:
                    current = current.__rotate_right_left()
                # Caso DD
                else:
                    current = current.__rotate_left()

            current = current.parent

        # 5. Devolvemos la raíz del árbol resulrante
        root = self
        while root.parent is not None:
            root = root.parent
        return root
    

    def remove(self: typing.Self, value: T) -> typing.Self | None:
        """Elimina un valor del árbol AVL y rebalancea los nodos afectados.

        Pasos del algoritmo:
            1. Identificar el nodo objetivo y el punto de partida para el rebalanceo
               (el padre del nodo físicamente desacoplado).
            2. Realizar la eliminación estándar de ABB (super().remove(value)).
            3. Si el árbol queda vacío, retornar None.
            4. Ascender desde el punto de desacople hacia la raíz revisando el factor de equilibrio
               y aplicando las rotaciones necesarias (a diferencia de la inserción, una eliminación
               puede requerir múltiples rotaciones a lo largo del camino hacia la raíz).
            5. Retornar la nueva raíz absoluta.

        Args:
            value (T): Valor a eliminar.

        Returns:
            AVLTree[T] | None: La nueva raíz del árbol, o None si el árbol quedó vacío.

        Complejidad temporal: O(log n) garantizado.
        """
        # 1. Identificamos el nodo objetivo y el punto de partida
        target = self
        while target is not None and target.value != value:
            if value < target.value:
                target = target.left
            else:
                target = target.right

        start_node = None
        if target is not None:
            if target.left is None or target.right is None:
                start_node = target.parent
            else:
                # Si tiene dos hijos, buscamos el nodo más pequeño del subárbol derecho
                sucesor = target.right
                while sucesor.left is not None:
                    sucesor = sucesor.left
                start_node = sucesor.parent
                if start_node == target:
                    start_node = target

        # 2. Eliminación estándar de ABB
        new_root = super().remove(value)

        # 3. Si el arbol queda vacio, devuelve None
        if new_root is None:
            return None

        # 4. Ascendemos hasta la raíz revisando el equilibrio
        current = start_node
        while current is not None:
            fe = current.balance

            #Mismas comprobaciones que en el insert para las rotaciones:
            if fe < -1:
                if current.left and current.left.balance > 0:
                    current = current.__rotate_left_right()
                else:
                    current = current.__rotate_right()
            elif fe > 1:
                if current.right and current.right.balance < 0:
                    current = current.__rotate_right_left()
                else:
                    current = current.__rotate_left()

            current = current.parent

        # 5. Devuelve la nueva raíz
        root = new_root
        while root.parent is not None:
            root = root.parent
        return root

        
    def __rotate_right(self: typing.Self) -> typing.Self:
        """Realiza una rotación simple a la derecha (Caso Izquierda-Izquierda / LL).

        Se aplica cuando un nodo `self` está sobrecargado a la izquierda (FE <= -2)
        y su hijo izquierdo tiene FE <= 0.

        Diagrama de la transformación:
                 self (Z)                    new_root (Y)
                 /      \\                     /          \\
              new_root (Y)  T3      ===>     T1          self (Z)
              /         \\                               /      \\
            T1           T2                             T2       T3

        Returns:
            AVLTree[T]: La nueva raíz local del subárbol rotado (`new_root`).
        """
        parent = self.parent
        new_root = self.left

        if new_root is None:
            raise RuntimeError("No se puede rotar a la derecha sin un subárbol izquierdo")

        # 1. El subárbol derecho de new_root (T2) pasa a ser el hijo izquierdo de self
        self.left = new_root.right

        # 2. self pasa a ser el hijo derecho de new_root
        new_root.right = self

        # 3. Enlazar new_root con el padre original del subárbol
        new_root.parent = parent
        if parent is not None and parent.value is not None and new_root.value is not None:
            if new_root.value < parent.value:
                parent.left = new_root
            else:
                parent.right = new_root

        return new_root

    def __rotate_left(self: typing.Self) -> typing.Self :
        """Realiza una rotación simple a la izquierda (Caso Derecha-Derecha / RR).

        Se aplica cuando un nodo `self` está sobrecargado a la derecha (FE >= 2)
        y su hijo derecho tiene FE >= 0.

        Diagrama de la transformación:
               self (Z)                                new_root (Y)
              /        \\                                /          \\
            T1       new_root (Y)       ===>         self (Z)       T3
                     /          \\                     /     \\
                   T2            T3                  T1       T2

        Returns:
            AVLTree[T]: La nueva raíz local del subárbol rotado (`new_root`).
        """
        parent = self.parent
        new_root = self.right

        if new_root is None:
            raise RuntimeError("No se puede rotar a la izquierda sin un subárbol derecho")

        # 1. El subárbol izquierdo de new_root pasa a ser el hijo derecho de self
        self.right = new_root.left

        #2. self pasa a ser el hijo izquierdo de new_root
        new_root.left = self

        #3. Enlazar new_root con el padre original del subárbol
        new_root.parent = parent
        if parent is not None and parent.value is not None and new_root.value is not None:
            if new_root.value < parent.value:
                parent.left = new_root
            else:
                parent.right = new_root

        return new_root

    def __rotate_left_right(self: typing.Self) -> typing.Self:
        """Realiza una rotación doble Izquierda-Derecha (Caso LR).

        Se aplica cuando un nodo está desbalanceado a la izquierda (FE <= -2)
        pero su hijo izquierdo está cargado a la derecha (FE > 0).

        Pasos:
            1. Rotación simple a la izquierda sobre el hijo izquierdo.
            2. Rotación simple a la derecha sobre el nodo actual (`self`).

        Returns:
            AVLTree[T]: La nueva raíz local del subárbol tras la rotación doble.
        """
        if self.left is None:
            raise RuntimeError("No se puede rotar izquierda-derecha sin un subárbol izquierdo")

        # 1. Rotación simple a la izquierda sobre el hijo izquierdo
        self.left.__rotate_left()

        # 2. Rotación simple a la derecha sobre self
        return self.__rotate_right()


    def __rotate_right_left(self: typing.Self) -> typing.Self:
        """Realiza una rotación doble Derecha-Izquierda (Caso RL).

        Se aplica cuando un nodo está desbalanceado a la derecha (FE >= 2)
        pero su hijo derecho está cargado a la izquierda (FE < 0).

        Pasos:
            1. Rotación simple a la derecha sobre el hijo derecho.
            2. Rotación simple a la izquierda sobre el nodo actual (`self`).

        Returns:
            AVLTree[T]: La nueva raíz local del subárbol tras la rotación doble.
        """
        if self.right is None:
            raise RuntimeError("No se puede rotar derecha-izquierda sin un subárbol derecho")

        # 1. Rotación simple a la derecha sobre el hijo derecho
        self.right.__rotate_right()

        # 2. ROtación simple a la izquierda sobre self
        return self.__rotate_left()