import cffi
import json
import os

class ArnelifyRouter:
  def __init__(self):
    srcDir: str = os.walk(os.path.abspath('venv/lib64'))
    libPaths: list[str] = []
    for root, dirs, files in srcDir:
      for file in files:
        if file.startswith('arnelify-router') and file.endswith('.so'):
          libPaths.append(os.path.join(root, file))

    self.ffi = cffi.FFI()
    self.lib = self.ffi.dlopen(libPaths[0])

    self.ffi.cdef("""
      typedef const char* cMethod;
      typedef const char* cPath;
      typedef const char* cPattern;
      typedef const char* cRouteOpt;

      void router_create();
      void router_any(cPattern);
      void router_get(cPattern);
      void router_post(cPattern);
      void router_put(cPattern);
      void router_patch(cPattern);
      void router_delete(cPattern);
      const char* router_find(cMethod, cPath);
      void router_free(cRouteOpt);
      void router_reset();
    """)

    self.controllers: list[callable] = []
    self.lib.router_create()

  def any(self, pattern: str, controller: callable) -> None:
    self.controllers.append(controller)
    cPattern = self.ffi.new("char[]", pattern.encode('utf-8'))
    self.lib.router_any(cPattern)

  def get(self, pattern: str, controller: callable) -> None:
    self.controllers.append(controller)
    cPattern = self.ffi.new("char[]", pattern.encode('utf-8'))
    self.lib.router_get(cPattern)

  def post(self, pattern: str, controller: callable) -> None:
    self.controllers.append(controller)
    cPattern = self.ffi.new("char[]", pattern.encode('utf-8'))
    self.lib.router_post(cPattern)

  def put(self, pattern: str, controller: callable) -> None:
    self.controllers.append(controller)
    cPattern = self.ffi.new("char[]", pattern.encode('utf-8'))
    self.lib.router_put(cPattern)

  def patch(self, pattern: str, controller: callable) -> None:
    self.controllers.append(controller)
    cPattern = self.ffi.new("char[]", pattern.encode('utf-8'))
    self.lib.router_patch(cPattern)

  def delete(self, pattern: str, controller: callable) -> None:
    self.controllers.append(controller)
    cPattern = self.ffi.new("char[]", pattern.encode('utf-8'))
    self.lib.router_delete(cPattern)

  def find(self, method: str, path: str) -> dict | None:
    cMethod = self.ffi.new("char[]", method.encode('utf-8'))
    cPath = self.ffi.new("char[]", path.encode('utf-8'))
    cRouteOpt = self.lib.router_find(cMethod, cPath)
    serialized: str = self.ffi.string(cRouteOpt).decode('utf-8')
    self.lib.router_free(cRouteOpt)
    route: dict | None = None
    if serialized == '{}':
      return None
    
    try: 
      route = json.loads(serialized)
    except json.JSONDecodeError as err:
      print(f"[ArnelifyRouter FFI] Python error: The cRouteOpt must be a valid JSON.")
      exit(1)

    return route
  
  def getController(self, id: str) -> callable:
    return self.controllers[id]
  
  def reset(self) -> None:
    self.lib.router_reset()