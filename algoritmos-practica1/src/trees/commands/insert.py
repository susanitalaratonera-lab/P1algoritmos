"""Comando del intérprete para insertar un nuevo valor en el árbol."""

from __future__ import annotations

from ..trees import AVLTree, Comparable

from .. import utils


def insert[T: Comparable](tree: AVLTree[T], value: str) -> AVLTree[T]:
    """Inserta una nueva entidad en el árbol AVL manteniendo la propiedad de balanceo.

    Nota pedagógica de implementación:
        El argumento `value` se recibe como una cadena de texto en formato JSON.
        Debe deserializarse al objeto definido en `model.py` (usando `utils.parse_json_to_character(value)`)
        antes de invocar el método `tree.insert(...)`.
        Si ya existe un dato con la misma clave en el arbol debe imprimirse un mensaje con el patron
        VALUE FOR KEY <key> ALREADY EXISTS. Ejemplo:
            VALUE FOR KEY Hubble ALREADY EXISTS
        Si se hace la inserción correctamente debe imprimir un mensaje con el patron VALUE <value>
        INSERTED SUCCESSFULLY. Ejemplo:
            VALUE {"name": "Hubble", "agency": "NASA/ESA", "orbit_type": "LEO", "launch_year": 1990,
            "x": 4800.0, "y": -3200.0, "z": 3600.0, "transmitter_power_w": 200.0, "status": "Active",
            "description": "Pioneering optical and ultraviolet space telescope exploring the deep
            universe."} SUCCESSFULLY INSERTED

    Sintaxis en el script:
        INSERT '{"nome": "Yoda", "especie": "Desconocida", ...}'

    Args:
        tree (AVLTree[T]): Árbol actual en memoria sobre el cual insertar.
        value (str): Cadena en formato JSON que representa la entidad a insertar.

    Returns:
        AVLTree[T]: La nueva raíz del árbol tras la inserción y las posibles rotaciones AVL.

    Raises:
        json.JSONDecodeError: Si la cadena `value` no es un JSON válido.
        TypeError: Si la estructura de campos no coincide con la del modelo.

    Complejidad temporal: O(log n).
    Complejidad espacial: O(log n) por la recursión.
    """
    # TODO: [Práctica Alumno]
    # 1. Parsear el string JSON 'value' a un objeto del modelo (ej: obj = utils.parse_json_to_character(value))
    # 2. Insertar el objeto en el árbol: tree = tree.insert(obj)
    # 3. Retornar la nueva raíz
    
    # 1. Parseamos el string JSON 'value' a un objeto del modelo
    obj = utils.parse_json_to_node(value)
    key = obj.name

    # Si el árbol está vacío, creamos e instanciamos la raíz directamente
    if tree is None:
        print(f"VALUE {value} SUCCESSFULLY INSERTED")
        return AVLTree(obj)

    # 2. busqueda manual
    target_node = tree
    while target_node is not None:
        current_name = getattr(target_node.value, "name")
        
        # Si la clave coincide, paramos de buscar
        if current_name == key:
            break
            
        # Si no, decidimos por qué rama bajar
        if key < current_name:
            target_node = target_node.left
        else:
            target_node = target_node.right

    # Comprobamos si el dato ya existe
    if target_node is not None:
        print(f"VALUE FOR KEY {key} ALREADY EXISTS")
        return tree

    # 3. Insertamos el objeto en el árbol con la lógica del AVL
    new_root = tree.insert(obj)
    print(f"VALUE {value} SUCCESSFULLY INSERTED")
    
    return new_root