import importlib.util
import sys
spec = importlib.util.spec_from_file_location("faam_data", "/home/daspr/vcs/faam-data/faam_data/__init__.py")
faam_data = importlib.util.module_from_spec(spec)
sys.modules["faam_data"] = faam_data
spec.loader.exec_module(faam_data)

print(faam_data)


spec = importlib.util.spec_from_file_location("faam_data.defaults", "/home/daspr/vcs/faam-data/faam_data/defaults.py")
defaults = importlib.util.module_from_spec(spec)
sys.modules["faam_data.defaults"] = defaults
spec.loader.exec_module(defaults)

print(defaults)
print(dir(defaults))

print(faam_data.models.Dataset)
