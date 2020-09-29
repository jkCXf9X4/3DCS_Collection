
from catia.automation_element import CatiaAutomation
from catia.tree import Tree
from at_timeit import timeit

import re


class ListDialog:

    def __init__(self, doc, button_text, dialog_re, prod_name: str):
        self.doc = doc
        self.button_text = button_text
        self.dialog_re = dialog_re
        self.prod_name = prod_name

        self._dialog = self._find_dialog()

    def ensure_dialog(func):
        def wrapper(self, *args, **kwargs):
            self.open_dialog()
            if self.exists is False:
                raise Exception(f"Cant find window, {self.dialog_re}")
            return func(self, *args, **kwargs)
        return wrapper

    @property
    # @timeit # 500ms
    def exists(self):
        return self._dialog is not None and self._dialog.exists()

    # @timeit 1500ms
    def open_dialog(self):
        if self.exists:
            return
        Tree.select_product(doc=self.doc, string=self.prod_name)
        window = CatiaAutomation.get_catia_main_window()
        window.wait('exists')
        button = window[self.button_text]
        button.click()

    def _find_dialog(self):
        app = CatiaAutomation.get_catia_app()
        dialog = app.window(title_re=self.dialog_re)
        return dialog

    @ensure_dialog
    def close_dialog(self):
        self._dialog.child_window(best_match="OK").click()

    @ensure_dialog
    def get_items(self):
        listview = self._dialog.child_window(best_match="ListView")
        items = listview.items()
        items_text = [i.text() for i in items if i.subitem_index == 1]
        return(items_text)

    @ensure_dialog
    def open_list_object(self, name):
        listview = self._dialog.child_window(best_match="ListView")
        items = listview.items()
        _ = [i.deselect() for i in items]

        matched_items = [i for i in items if i.subitem_index == 1 and name == i.text()]

        if len(matched_items) == 1:
            matched_items[0].select()
            self._dialog.child_window(best_match="Modify").click()
            return True
        return False

    @ensure_dialog
    def debug(self):
        self._dialog.print_control_identifiers()


class MoveListDialog(ListDialog):
    def __init__(self, doc, prod_name: str):
        super().__init__(doc=doc, button_text='3DCS Move', dialog_re=f".*Moves In {prod_name}.*", prod_name=prod_name)


class ToleranceListDialog(ListDialog):
    def __init__(self, doc, prod_name: str):
        super().__init__(doc=doc, button_text='3DCS Tolerance', dialog_re=f".*Tolerances In {prod_name}.*", prod_name=prod_name)


class MeasurementListDialog(ListDialog):
    def __init__(self, doc, prod_name: str):
        super().__init__(doc=doc, button_text='3DCS Measurement', dialog_re=f".*Measurements In {prod_name}.*", prod_name=prod_name)


class GDATListDialog(ListDialog):
    def __init__(self, doc, prod_name: str):
        super().__init__(doc=doc, button_text='GD&Ts', dialog_re=".*GD.T.*", prod_name=prod_name) # {prod_name}.*
