from pywinauto.application import Application
import psutil


def get_pid(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if processName.lower() == pinfo['name'].lower():
                return pinfo["pid"]
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError):
            pass
    raise Exception("Process not found")


def connect_application(name):
    pid = get_pid(name)
    app = Application(backend="win32").connect(process=pid) # , allow_magic_lookup=False
    return app


class CatiaAutomation:
    app = connect_application("CNEXT.EXE")

    @staticmethod
    def get_catia_app() -> Application:
        return CatiaAutomation.app

    @staticmethod
    def get_catia_main_window():
        app = CatiaAutomation.get_catia_app()
        window = app.window(title_re=".*CATIA V5-6R2014 Veoneer.*")
        return window
