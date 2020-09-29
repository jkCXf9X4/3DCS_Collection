

from catia.automation_element import CatiaAutomation
app = CatiaAutomation.get_catia_app()

print(app.Dialog.Static2.Texts()[0])