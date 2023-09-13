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
            plugin_id = plugin_path.stem
            self.__plugins.append(plugin_id)


    def list_plugins(self):
        return self.__plugins


    def new_object(self, plugin_id, **kwargs):
        if plugin_id in self.__plugins:
            return importlib.import_module(plugin_id, self.plugins_dir).Plugin(**kwargs)

