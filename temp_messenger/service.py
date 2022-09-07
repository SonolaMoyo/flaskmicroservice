import json
from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http
from temp_messenger.dependencies.redis import Redis
from temp_messenger.dependencies.jinja2 import Jinja2
from werkzeug.wrappers import Response

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
    # konnichiwa_service = RpcProxy('konnichiwa_service')
    
    # @http('GET', '/')
    # def root(self, request):
    #     return self.konnichiwa_service.konnichiwa()
    
    message_service = RpcProxy('message_service')
    templates = Jinja2()
    
    @http('GET', '/')
    def home(self, request):
        messages = self.message_service.get_all_messages()
        rendered_template = self.templates.render_home(messages)
        html_response = create_html_response(rendered_template)
        return html_response
    
    @http('POST', '/')
    def post_message(self, request):
        try:
            data = get_request_data(request)
        except json.JSONDecodeError:
            return 400, 'JSON payload expected'
        
        try: 
            message = data['message']
        except KeyError:
            return 400, 'No message given'
        
        self.message_service.save_message(message)
        
        return 204, ''


def create_html_response(content):
    headers = {'Content-Type': 'text/html'}
    return Response(content, status=200, headers=headers)

def get_request_data(request):
    data_as_text = request.get_data(as_text=True)
    return json.loads(data_as_text)
    
