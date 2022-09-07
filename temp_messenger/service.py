from nameko.rpc import rpc

class KonnichiwaService:
    name = 'konnichiwa_service'

    @rpc
    def konnichiwa(self):
        return 'Konnichiwa!'


