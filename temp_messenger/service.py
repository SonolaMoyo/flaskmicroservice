from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http
from temp_messenger.dependencies.redis import Redis

# class KonnichiwaService:
#     name = 'konnichiwa_service'

#     @rpc
#     def konnichiwa(self):
#         return 'Konnichiwa!'

class MessageService:
    name = 'message_service'
    redis = Redis()
    
    @rpc
    def get_message(self, message_id):
        return self.redis.get_message(message_id) 
    
    @rpc
    def konnichiwa(self):
        return 'Konnichiwa!'

class WebServer:
    name = 'web_server'
    konnichiwa_service = RpcProxy('konnichiwa_service')
    
    @http('GET', '/')
    def root(self, request):
        return self.konnichiwa_service.konnichiwa()

