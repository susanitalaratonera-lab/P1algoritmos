"""Comando del intérprete para cargar datos desde un archivo JSON en el árbol."""

from __future__ import annotations

from pathlib import Path

from ..trees import AVLTree, Node

from .. import utils


def load(tree: AVLTree[Node] | None, filepath: str | Path) -> AVLTree[Node] | None:
    """Carga los datos contenidos en un archivo JSON en el árbol AVL.

    Comportamiento:
        - Si el árbol recibido (`tree`) es `None`, crea un nuevo árbol AVL cuyo primer
          nodo es el primer elemento del JSON y añade el resto secuencialmente.
          Tras crear el arbol debe imprimir un mensaje "TREE CREATED WITH <n> ITEMS", donde 
          <n> representa el numero de elementos insertado en el arbol. Ejemplo: 
                TREE CREATED WITH 12 ITEMS
        - Si el árbol ya existe (`tree is not None`), inserta todos los elementos
          del archivo en la estructura existente mediante `insert`, preservando el balanceo AVL.
          Tras insertar los datos en el arbol debe imprimir un mensaje "INSERTED <n> NEW ELEMENTS 
          IN TREE", donde <n> representa el numero de elementos insertados en el arbol. Ejemplo:
                INSERTED 3 NEW ELEMENTS IN TREE

    Nota pedagógica de implementación:
        El archivo indicado en `filepath` contiene registros en formato JSON que deben
        deserializarse en instancias del modelo definido en `model.py` (mediante `utils.load_json_file`).

    Sintaxis en el script:
        LOAD data.json
        LOAD "ruta con espacios/personaxes.json"

    Args:
        tree (AVLTree[T] | None): Árbol actual en memoria o None si aún no se ha inicializado.
        filepath (str | Path): Ruta al archivo JSON que contiene las entidades a cargar.

    Returns:
        AVLTree[T]: El árbol AVL resultante con los nuevos datos cargados.

    Raises:
        FileNotFoundError: Si el archivo especificado no existe en el sistema.
        json.JSONDecodeError: Si el contenido del archivo no es un JSON válido.
    """
    # TODO: [Práctica Alumno]
    # 1. Leer y parsear las instancias del modelo desde 'filepath' (ej: utils.load_json_file(filepath))
    # 2. Si tree es None, crear el AVLTree con la primera instancia e insertar las demás
    # 3. Si tree ya existe, insertar secuencialmente cada una de las instancias en tree
    # 4. Retornar la raíz del árbol resultante
    
    # 1. Leemos y parseamos las instancias del modelo desde 'filepath'
    data = utils.load_json_file(filepath)

    n_items = len(data)
    if tree is None:
        is_new_tree = True
    else:
        is_new_tree = False

    # 2 y 3. Creamos el árbol con la primera instancia o insertamos secuencialmente
    for item in data:
        if tree is None:
            tree = AVLTree(item)
        else:
            tree = tree.insert(item)

    if is_new_tree:
        print(f"TREE CREATED WITH {n_items} ITEMS")
    else:
        print(f"INSERTED {n_items} NEW ELEMENTS IN TREE")

    # 4. Retornar la raíz del árbol resultante
    return tree