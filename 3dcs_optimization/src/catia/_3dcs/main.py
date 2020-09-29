
import time
import win32com.client
import re

from catia._3dcs.list_dialog import MoveListDialog, GDATListDialog, ToleranceListDialog, MeasurementListDialog
from catia._3dcs.gdat_dialog import GdatDialog
from catia._3dcs.simulation import SimulationDialog

from catia.automation_element import CatiaAutomation
from catia.tree import Tree

class _3dcs_tolerance:
    def __init__(self, name):
        self.name = name
        
    def get_bounds(self):
        m = re.search(r"\[R(?P<lb>\d*)_(?P<ub>\d*)\]", self.name)
        lower_bound = m.group('lb')
        upper_bound = m.group('ub')

        return [lower_bound, upper_bound]

    def is_match(self, pattern):
        if re.search(pattern=pattern, string=self.name):
            return True
        return False

class _3dcs_product:
    def __init__(self, name):
        self.name = name
        self.tolerances = []

    def collect_tolerances(self, catia_document):
        gdat_dlg = GDATListDialog(doc=catia_document, prod_name=self.name)
        names = gdat_dlg.get_items()
        gdat_dlg.close_dialog()

        tolerances = [_3dcs_tolerance(i) for i in names]
        _ = [self.tolerances.append(i) for i in tolerances]
    
    def get_tolerance(self, pattern):
        match = [i for i in self.tolerances if i.is_match(pattern)]
        if match != None and len(match) == 1:
            return match[0]
        return None


class _3DCS:

    def __init__(self):
        self.catia_application = win32com.client.Dispatch('CATIA.Application')

        self.catia_document = self.catia_application.ActiveDocument

        self.products = []

    def collect_products(self):
        part_names = Tree.get_products_name(doc=self.catia_document)
        self.products = [_3dcs_product(i) for i in part_names]

    def collect_tolerances(self):
        for i in self.products:
            i.collect_tolerances(self.catia_document)

    def get_tolerances(self):
        l = []
        _ = [l.extend(i.tolerances) for i in self.products]
        return l

    def set_tolerances(self, tolerances: list):
        if sum([len(i.tolerances) for i in self.products]) != len(tolerances):
            raise Exception("Number of values need to match number of tolerances")
        for counter, product in enumerate(self.products):
            gdat_list = GDATListDialog(doc=self.catia_document, prod_name=product.name)
            for tol in product.tolerances:
                dialog = GdatDialog(gdat_list, tol.name)
                dialog.set_tolerance(tolerances[counter])
                dialog.save_and_exit()
            gdat_list.close_dialog()

    def get_bounds(self):
        bounds = [i.get_bounds() for i in self.get_tolerances()]
        return bounds

    def run_simulation(self):
        app = CatiaAutomation.get_catia_app()
        dialog = app.window(title="Analysis")
        if dialog.exists():
            dialog.close()

        simulation = SimulationDialog()
        simulation.run()

        dialog.wait("visible", timeout=15*60, retry_interval=10)

        dialog.menu_select('File->Save Simu As...')  # does not work

        dialog.close()




