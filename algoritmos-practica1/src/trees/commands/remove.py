"""Comando del intérprete para eliminar un valor del árbol."""

from __future__ import annotations

from ..trees import AVLTree, Comparable, Node


def remove[T: Comparable](tree: AVLTree[T], key: str) -> AVLTree[T]:
    """Elimina una entidad del árbol AVL y rebalancea la estructura si es necesario.

    Si el dato no existía debe imprimirse el mensaje KEY <key> NOT PRESENT IN TREE. Por ejemplo:
        KEY Hubble NOT PRESENT IN TREE
    Si el dato existía debe imprimirse el mensaje VALUE <value> SUCCESSFULLY REMOVED. Ejemplo:
        VALUE {"name": "Hubble", "agency": "NASA/ESA", "orbit_type": "LEO", "launch_year": 1990,
        "x": 4800.0, "y": -3200.0, "z": 3600.0, "transmitter_power_w": 200.0, "status": "Active",
        "description": "Pioneering optical and ultraviolet space telescope exploring the deep
        universe."} SUCCESSFULLY REMOVED

    Nota pedagógica de implementación:
        El argumento `key` se recibe como una clave directa (p. ej. el nombre de un satelite)
        
    Sintaxis en el script:
        REMOVE "Darth Vader"

    Args:
        tree (AVLTree[T]): Árbol actual en memoria.
        key (str): Cadena identificativa de la entidad a eliminar.

    Returns:
        AVLTree[T]: La nueva raíz del árbol tras la eliminación.

    Complejidad temporal: O(log n).
    """
    # TODO: [Práctica Alumno]
    # 1. Utilizar la clave directamente
    # 2. Invocar tree.remove(...)
    # 3. Retornar la nueva raíz del árbol
    
    #si el árbol está vacío, el dato no existe
    if tree is None:
        print(f"KEY {key} NOT PRESENT IN TREE")
        return tree

    # 1. Utilizamos la clave directamente
    key_node = Node(name=key)
    # El árbol guarda objetos Node, así que buscamos con un Node que solo tiene la clave
    target_node = tree.find(key_node)

    if target_node is None:
        print(f"KEY {key} NOT PRESENT IN TREE")
        return tree
    else:
        # 2. Invocamos tree.remove
        new_root = tree.remove(key_node)
        # La salida de ejemplo (la correcta) imprime el Node construido a partir de la clave
        print(f"VALUE {key_node} SUCCESSFULLY REMOVED")

        # 3. Retornamos la nueva raíz del árbol
        return new_root