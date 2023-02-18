from typing import List, Set, Tuple, Dict, Optional

#Tipos de datos simples.
#int / float / bool / bytes.
def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes):
    return item_a, item_b, item_c, item_d, item_d, item_e


#Listas.
def process_items(items: List[str]):
    for item in items:
        print(type(item))

#Set and tuples.
def process_items(items_t: Tuple[int, int, str], items_s: Set[bytes]):
    return items_t, items_s


#Diccionarios.
def process_items(prices: Dict[str, float]):
    for item_name, item_price in prices.items():
        print(type(item_name))
        print(type(item_price))

#Opcional.
def say_hi(name: Optional[str] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")


#Clase y Objeto.
class Persona:
	def __init__(self, name: str):
		self.name = name


def get_person_name(one_person:Persona):
	return one_person.name


if __name__ == '__main__':
	#process_items([1,"a", 2, "b"])
	process_items({"hola": 10.0, "Mundo": 12.0})
	say_hi("Yilver")
	persona = Persona("Biagni")
	print(get_person_name(persona))