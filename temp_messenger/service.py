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
    
    # @rpc
    # def konnichiwa(self):
    #     return 'Konnichiwa!'
    
    @rpc
    def save_message(self, message):
        message_id = self.redis.save_message(message)
        return message_id
    
    @rpc
    def get_all_messages(self):
        messages = self.redis.get_all_messages()
        return messages

class WebServer:
    name = 'web_server'
    konnichiwa_service = RpcProxy('konnichiwa_service')
    
    @http('GET', '/')
    def root(self, request):
        return self.konnichiwa_service.konnichiwa()

