import importlib
import glob
from pathlib import Path


plugins_dir = "plugins"
plugins_tmp = glob.glob(f'{plugins_dir}/*.py')
__plugins = []
for plugin in plugins_tmp:
    plugin_path = Path(plugin)
    plugin_id = plugin_path.stem
    __plugins.append(plugin_id)


def list_plugins():
    return __plugins


def new_object(plugin_name, parent_id=None, master=None, **kwargs):
    if plugin_name in __plugins:
        return importlib.import_module(plugin_name, plugins_dir).Plugin(master, plugin_name, parent_id, **kwargs)

