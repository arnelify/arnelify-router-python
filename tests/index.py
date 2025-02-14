from arnelify_router import ArnelifyRouter
import json

def main() -> int:
  router = ArnelifyRouter()
  
  def controller(ctx: dict) -> dict:
    return ctx

  router.get("/", controller)
  router.get("/:id", controller)

  routeOpt: dict | None = router.find("GET", "/1")
  if not routeOpt:
    print("[Arnelify Router]: Route not found.")
    return 0

  route: dict = routeOpt
  print("[Arnelify Router]: Route serialized: " + json.dumps(route))

  controllerOpt: callable | None = router.getController(route["id"])
  if not controllerOpt:
    print("[Arnelify Router]: Controller not found.")

  controller: callable = controllerOpt

  ctx = {
    "code": 200,
    "success": "Welcome to Arnelify Router"
  }

  res: dict = controller(ctx)
  print("[Arnelify Router]: Response: " + json.dumps(res))

if __name__ == "__main__":
  main()