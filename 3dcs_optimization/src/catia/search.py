

class Search:

    @staticmethod
    def search(doc, query):
        doc.Selection.Search(query)
        return doc.Selection
