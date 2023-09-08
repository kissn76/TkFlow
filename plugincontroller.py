import importlib
import glob
from pathlib import Path


class Plugincontroller:
    def __init__(self):
        self.plugins_dir = "plugins"
        plugins_tmp = glob.glob(f'{self.plugins_dir}/*.py')
        self.__plugins = []
        for plugin in plugins_tmp:
            plugin_path = Path(plugin)
            plugin_name = plugin_path.stem
            self.__plugins.append(plugin_name)


    def list_plugins(self):
        return self.__plugins


    def new_object(self, plugin_name, **kwargs):
        if plugin_name in self.__plugins:
            return importlib.import_module(plugin_name, self.plugins_dir).Plugin(**kwargs)

