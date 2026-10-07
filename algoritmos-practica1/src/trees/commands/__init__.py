"""Paquete que expone el catálogo de comandos ejecutables por el intérprete.

Cada módulo en este paquete implementa un comando concreto compatible con el intérprete.
El intérprete mapea la primera palabra de cada línea leída en un script (en minúsculas)
con la función correspondiente aquí exportada.

Comandos disponibles en la práctica:
    - LOAD <ruta_fichero>: Carga datos en formato JSON en el árbol.
    - PRINT: Imprime la estructura del árbol.
    - INSERT <valor>: Inserta un valor en el árbol balanceado.
    - REMOVE <valor>: Elimina un valor del árbol.
    - FIND <valor>: Busca un valor en el árbol e imprime el resultado.
    - UPDATE <key> <valor>: Actualiza el nodo correspondiente a key con el nuevo valor.
"""

from .find import find
from .insert import insert
from .load import load
from .print import print
from .remove import remove
from .update import update

__all__ = [
    "find",
    "insert",
    "load",
    "print",
    "remove",
    "update",
]