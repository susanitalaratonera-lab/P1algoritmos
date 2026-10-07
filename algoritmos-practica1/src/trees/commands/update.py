"""Comando del intérprete para actualizar el valor asociado a un nodo."""

from __future__ import annotations

import dataclasses
import json

from ..trees import AVLTree, Node


def update(tree: AVLTree[Node] | None, key: str, value: str) -> AVLTree[Node] | None:
    """Actualiza la entidad identificada por `key` reemplazándola por el nuevo objeto deserializado de `value`.

    Si no existe un dato para la clave proporcionada se debe imprimir el mensaje KEY <key> NOT PRESENT. Ejemplo:
        KEY Hubble NOT PRESENT
    Si existe un dato para la clave proporcionada debe actualizarse el dato e imprimir por pantalla el mensaje 
    UPDATED ENTRY <key> IN TREE. ORIGINAL VALUE: <original value>. UPDATED VALUE: <updated value>. Ejemplo:
        UPDATED ENTRY Hubble IN TREE. ORIGINAL VALUE: {"name": "Hubble", "agency": "NASA/ESA", "orbit_type": "LEO",
        "launch_year": 1990, "x": 4800.0, "y": -3200.0, "z": 3600.0, "transmitter_power_w": 200.0, "status": "Active",
        "description": "Pioneering optical and ultraviolet space telescope exploring the deep universe."}. UPDATED
        VALUE: {"name": "Hubble", "agency": "NASA", "orbit_type": "LEO", "launch_year": 1990, "x": 5800.0,
        "y": -3200.0, "z": 3600.0, "transmitter_power_w": 200.0, "status": "Active", "description": "Pioneering 
        optical and ultraviolet space telescope exploring the deep universe."}
    
    Nota pedagógica de implementación:
        - `key` identifica el nodo actual a actualizar (ej: `"Luke Skywalker"`).
        - `value` es una cadena en formato JSON que representa la nueva versión de la entidad
          (o los nuevos datos a actualizar). Debe deserializarse con `utils.parse_json_to_character(value)`.
        - Si la nueva versión modifica la clave que determina el orden relativo en el árbol,
          el alumno debe considerar si procede actualizar el valor in-situ o eliminar y reinsertar
          para mantener la invariante de orden del ABB y el balanceo AVL.

    Sintaxis en el script:
        UPDATE "Luke Skywalker" '{"nome": "Luke Skywalker", "arma_principal": "Sable verde", ...}'

    Args:
        tree (AVLTree[T]): Árbol actual en memoria.
        key (str): Clave o identificador del nodo a buscar y actualizar.
        value (str): Cadena en formato JSON con la nueva información de la entidad.

    Returns:
        AVLTree[T]: La referencia a la raíz del árbol tras la actualización.

    Raises:
        KeyError: Si no existe ningún nodo con la clave `key` en el árbol.
        json.JSONDecodeError: Si `value` no es un JSON válido.
    """
    # TODO: [Práctica Alumno]
    # 1. Parsear el string JSON 'value' a un objeto del modelo (ej: new_obj = utils.parse_json_to_character(value))
    # 2. Localizar el nodo con clave 'key'
    # 3. Actualizar el contenido garantizando que se preserve la invariante AVL
    # 4. Retornar la raíz del árbol
    
    # Si el árbol está vacío, no existe la clave
    if tree is None:
        print(f"KEY {key} NOT PRESENT")
        return tree

    # 1. Parseamos el JSON value. Puede ser parcial (ej: '{"status": "Retired"}'),
    # así que lo leemos como diccionario para saber qué campos hay que cambiar
    new_fields = json.loads(value)

    # 2. Localizamos el nodo con clave 'key' (el árbol guarda objetos Node)
    target_node = tree.find(Node(name=key))

    if target_node is None:
        print(f"KEY {key} NOT PRESENT")
        return tree

    # Guardamos el objeto original para imprimirlo después
    original_value = target_node.value

    # Combinamos los datos originales con los campos nuevos (Node es inmutable)
    new_obj = dataclasses.replace(original_value, **new_fields)

    # 3. Actualizar el contenido garantizando que se preserve la invariante AVL
    if new_obj.name == original_value.name:
        # La clave no cambia: el orden del árbol se mantiene, actualizamos in situ
        target_node.value = new_obj
        new_root = tree
    else:
        # La clave cambia: eliminamos y reinsertamos para mantener el orden y el balanceo
        new_root = tree.remove(original_value)
        if new_root is None:
            new_root = AVLTree(new_obj)
        else:
            new_root = new_root.insert(new_obj)

    print(f"UPDATED ENTRY {key} IN TREE. ORIGINAL VALUE: {original_value}. UPDATED VALUE: {new_obj}")

    # 4. Retornamos la raíz del árbol
    return new_root