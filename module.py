import importlib
import glob
from pathlib import Path


class Module:
    def __init__(self):
        self.modules_dir = "modules"
        modules_tmp = glob.glob(f'{self.modules_dir}/*.py')
        self.__modules = []
        for module in modules_tmp:
            module_path = Path(module)
            module_name = module_path.stem
            self.__modules.append(module_name)


    def list_modules(self):
        return self.__modules


    def new_object(self, module_name, master):
        if module_name in self.__modules:
            return importlib.import_module(module_name, self.modules_dir).Plugin(master=master)

