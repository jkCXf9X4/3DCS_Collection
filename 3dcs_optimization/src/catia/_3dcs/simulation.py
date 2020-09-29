

from catia.automation_element import CatiaAutomation
from catia.tree import Tree
from at_timeit import timeit

import re
import time

class SimulationDialog:

    def __init__(self):
        self.dialog_re = ".*Run Analysis.*"
        self._dialog = self._find_dialog()

    def ensure_dialog(func):
        def wrapper(self, *args, **kwargs):
            self._open_dialog()
            if self.exists is False:
                raise Exception(f"Cant find window, {self.dialog_re}")
            return func(self, *args, **kwargs)
        return wrapper

    @property
    # @timeit
    def exists(self):
        return self._dialog is not None and self._dialog.exists()

    def run(self):
        app = CatiaAutomation.get_catia_app()

        self._open_dialog()
        self._press_start()

        while re.search(".*Results.*overwritten.*", app.Dialog.Static2.texts()[0]):
            app.Dialog.OK.click()

    # @timeit
    def _open_dialog(self):
        if self.exists:
            return

        window = CatiaAutomation.get_catia_main_window()
        window.wait('exists')
        button = window["3DCS Build"]
        button.click()

        button = window["TBDCSContainerRunLoadAnalysisId"]
        button.click()

    def _find_dialog(self):
        app = CatiaAutomation.get_catia_app()
        dialog = app.window(title_re=self.dialog_re)
        return dialog

    @ensure_dialog
    def _press_start(self):
        self._dialog.child_window(best_match="Start>>").click()

    @ensure_dialog
    def debug(self):
        self._dialog.print_control_identifiers()