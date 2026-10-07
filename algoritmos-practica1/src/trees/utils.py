"""Módulo de utilidades: Conversión y parsing entre JSON y objetos del tipo `Node`."""

from __future__ import annotations

import json
from pathlib import Path

from .trees import Node


def parse_json_to_node(data: str) -> Node:
    """Parsea una cadena JSON al objeto del modelo `Node`.

    Permite instanciar la entidad `Node` a partir del texto plano proporcionado
    en los comandos del intérprete.

    Args:
        data (str): Cadena en formato JSON con los atributos de un Node.

    Returns:
        Node: Instancia inmutable de la clase `Node` inicializada con los datos.

    Raises:
        json.JSONDecodeError: Si `data` no contiene un JSON sintácticamente válido.
        TypeError: Si los campos provistos no coinciden con los argumentos esperados por `Node`.
        KeyError: Si faltan campos requeridos en el diccionario.
    """
    return json.loads(data, object_hook=lambda d: Node(**d))


def load_json_file(filepath: str | Path) -> list[Node]:
    """Lee y deserializa un archivo JSON en una lista de objetos `Node`.

    Args:
        filepath (str | Path): Ruta al archivo JSON en el sistema.

    Returns:
        list[Node]: Lista de instancias de `Node`.

    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta dada.
        json.JSONDecodeError: Si el archivo no contiene un JSON bien formado.
    """
    path = Path(filepath)
    with path.open("r", encoding="utf-8") as f:
        content = json.load(f, object_hook=lambda d: Node(**d))
        return content
