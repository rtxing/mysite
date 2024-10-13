# import os
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from carshops.consumers import DriverConsumer  # Make sure to import your consumer

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             path('ws/driver_updates/', DriverConsumer.as_asgi()),
#         ])
#     ),
# })