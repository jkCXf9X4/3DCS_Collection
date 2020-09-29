from .select import Select
from at_timeit import timeit

class Tree:

    
    @staticmethod
    #@timeit #800ms
    def get_products_name(doc) -> list:
        selection = Select.select_all(doc=doc)
        documents = Select.get_elements(selection=selection)
        prod_names = [i.LeafProduct.Name for i in documents]
        return prod_names

    
    @staticmethod
    #@timeit # 90ms
    def select_product(doc, string: str):
        Select.select_product(doc=doc, string=string)
