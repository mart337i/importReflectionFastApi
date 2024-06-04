# Use of reflection for FastApi

The traversal works by using the `os.walk` function to recursively walk through the "addons" directory and its subdirectories, identifying all Python files:
1. **Directory Structure**:
   ```
   addons/
   ├── test1/
   │   ├── models/
   │   │   └── model.py
   │   └── routes/
   │       └── test1_service.py
   ├── test2/
   │   ├── models/
   │   │   └── model.py
   │   └── routes/
   │       └── test2_service.py
   ```

2. **Traversal Process**:
   - The `os.walk` function is called with the "addons" directory.
   - It recursively visits each subdirectory and collects all files.

3. **Example of `os.walk` Output**:
   - For the given structure, `os.walk` will generate:
     ```
     root = 'addons'
     dirs = ['test1', 'test2']
     files = []

     root = 'addons/test1'
     dirs = ['models', 'routes']
     files = []

     root = 'addons/test1/models'
     dirs = []
     files = ['model.py']

     root = 'addons/test1/routes'
     dirs = []
     files = ['test1_service.py']

     root = 'addons/test2'
     dirs = ['models', 'routes']
     files = []

     root = 'addons/test2/models'
     dirs = []
     files = ['model.py']

     root = 'addons/test2/routes'
     dirs = []
     files = ['test2_service.py']
     ```

4. **Processing Each File**:
   - For each file found, the relative path from "addons" is determined.
   - The file path is converted to a module path by replacing directory separators with dots (`.`) and removing the `.py` extension.

5. **Example of Module Path Conversion**:
   - `addons/test1/routes/test1_service.py` becomes `addons.test1.routes.test1_service`
   - `addons/test2/routes/test2_service.py` becomes `addons.test2.routes.test2_service`

6. **Including the Router**:
   - Each constructed module path is passed to the `include_router_from_module` function to import the module and include its router in the FastAPI application if it exists.

The `include_router_from_module` function is responsible for dynamically importing a module and checking if it contains a `router` attribute, which is then included in the FastAPI application. Here's a detailed explanation of how this function works:

1. **Function Definition**:
   ```python
   def include_router_from_module(module_name: str):
   ```

2. **Importing the Module**:
   - The function attempts to import the module using `importlib.import_module(module_name)`.
   ```python
   module = importlib.import_module(module_name)
   ```

3. **Checking for `router` Attribute**:
   - It checks if the imported module has an attribute named `router` using `hasattr(module, 'router')`.
   ```python
   if hasattr(module, 'router'):
   ```

4. **Including the Router**:
   - If the `router` attribute exists, the function includes it in the FastAPI application using `app.include_router`.
   ```python
   app.include_router(router=module.router)
   ```

5. **Logging the Success**:
   - A message is printed to the console indicating that the router from the module was successfully registered.
   ```python
   print(f"Registered router from module: {module_name}")
   ```

6. **Exception Handling**:
   - The function includes exception handling to manage cases where the module cannot be found or does not have a `router` attribute.
   - If a `ModuleNotFoundError` occurs, it prints an error message indicating that the module was not found.
   ```python
   except ModuleNotFoundError as e:
       print(f"Module not found: {module_name}, error: {e}")
   ```
   - If an `AttributeError` occurs because the module does not have a `router` attribute, it prints an error message.
   ```python
   except AttributeError as e:
       print(f"Module '{module_name}' does not have 'router' attribute, error: {e}")
   ```
