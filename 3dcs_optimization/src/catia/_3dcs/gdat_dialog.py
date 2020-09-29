
from catia.automation_element import CatiaAutomation
from .list_dialog import ListDialog

import re


class GdatDialog:

    def __init__(self, pre_dialog: ListDialog, item_re: str):
        self.pre_dialog = pre_dialog
        self.item_re = item_re

        self._dialog = self._find_dialog()

    def ensure_dialog(func):
        def wrapper(self, *args, **kwargs):
            self.open_dialog()
            if self.exists is False:
                raise Exception(f"Cant find window, {self.item_re}")
            return func(self, *args, **kwargs)
        return wrapper

    @property
    def exists(self):
        return self._dialog is not None and self._dialog.exists()

    def open_dialog(self):
        if self.exists:
            return
        self.pre_dialog.open_list_object(self.item_re)

    def _find_dialog(self):
        app = CatiaAutomation.get_catia_app()
        new_match = self.item_re.replace("[", r"\[").replace("]", r"\]")
        new_match = f".*{new_match}.*"
        dialog = app.window(title_re=new_match)
        return dialog

    @ensure_dialog
    def set_tolerance(self, value):
        self._dialog.TabControl.Select(2)
        self._dialog.child_window(best_match="MinusEdit").set_text(str(- value / 2))
        self._dialog.child_window(best_match="NormalEdit").set_text(str(value / 2))

    @ensure_dialog
    def save_and_exit(self):
        self._dialog.child_window(best_match="OK").click()

    @ensure_dialog
    def debug(self):
        self._dialog.print_control_identifiers(self.item_re)


# class MoveListDialog(ListDialog):
#     def __init__(self, doc, prod_name: str):
#         super().__init__(doc=doc, button_text='3DCS Move', dialog_re=f".*Moves In {prod_name}.*", prod_name=prod_name)

# class ToleranceListDialog(ListDialog):
#     def __init__(self, doc, prod_name: str):
#         super().__init__(doc=doc, button_text='3DCS Tolerance', dialog_re=f".*Tolerances In {prod_name}.*", prod_name=prod_name)

# class MeasurementListDialog(ListDialog):
#     def __init__(self, doc, prod_name: str):
#         super().__init__(doc=doc, button_text='3DCS Measurement', dialog_re=f".*Measurements In {prod_name}.*", prod_name=prod_name)

# class GDATListDialog(ListDialog):
#     def __init__(self, doc, prod_name: str):
#         super().__init__(doc=doc, button_text='GD&Ts', dialog_re=f".*GD&Ts In {prod_name}.*", prod_name=prod_name)

