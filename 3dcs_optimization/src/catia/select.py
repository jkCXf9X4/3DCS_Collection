
from .search import Search


class Select:

    @staticmethod
    def select_all(doc):
        return Search.search(doc, "'Product Structure'.Assembly+'Product Structure'.Part+'Product Structure'.Product,all")

    @staticmethod
    def select_product(doc, string: str):
        return Search.search(doc, f"'Product Structure'.Product.Name={string},all")

    @staticmethod
    def get_elements(selection):
        return [selection.Item2(i) for i in range(1, selection.Count + 1)]
