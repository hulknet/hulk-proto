from sanic import Sanic

from api.service import bp_service
from api.vm import bp_vm

app = Sanic("hulk")

app.blueprint([bp_vm, bp_service])

if __name__ == '__main__':
    app.run()
