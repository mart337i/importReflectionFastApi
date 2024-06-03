import importlib
import os
import sys
from fastapi import FastAPI

app = FastAPI()

def include_router_from_module(module_name: str):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, 'router'):
            app.include_router(
                router=module.router
            )
            print(f"Registered router from module: {module_name}")
    except ModuleNotFoundError as e:
        print(f"Module not found: {module_name}, error: {e}")
    except AttributeError as e:
        print(f"Module '{module_name}' does not have 'router' attribute, error: {e}")

def register_routes():
    addons_dir = os.path.join(os.path.dirname(__file__), '../addons')
    base_module = 'addons'

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

    for root, dirs, files in os.walk(addons_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                relative_path = os.path.relpath(os.path.join(root, file), addons_dir)
                module_name = os.path.join(base_module, relative_path).replace(os.sep, '.')[:-3]
                include_router_from_module(module_name)

register_routes()

@app.get("/")
async def root():
    return {"message": "Hello World"}