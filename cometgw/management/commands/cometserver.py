import uuid
import simplejson

from django.core.management.base import BaseCommand
from django.conf import settings

from carrot.connection import DjangoBrokerConnection
from carrot.messaging import Consumer

import tornado.httpserver
import tornado.ioloop
import tornado.web



class Command(BaseCommand):
    help = "Starts comet server."
    
    def handle(self, addrport='', *args, **options):
        addr = '127.0.0.1'
        port = 8888
        if addrport:
            try:
                addr, port = addrport.split(':')
                port = int(port)
            except ValueError:
                port = int(addrport)
                
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(port, addr)
        tornado.ioloop.IOLoop.instance().start()




class CometHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, exchange_name, queue_name, routing_key):
        def msg_callback(message_data, message):
            message.ack()
            self.write(simplejson.dumps(message_data))
            self.finish()

        consumer = Consumer(connection=conn, queue=queue_name,
                            exchange=exchange_name, routing_key=routing_key)
        consumer.register_callback(msg_callback)
        try:
            consumer.wait(1)
        except StopIteration:
            consumer.close()
        

conn = DjangoBrokerConnection()


application = tornado.web.Application([
    (r"/comet/(\w+)/([(a-f)(A-F)(0-9)-]+)/(\w+)", CometHandler),
])

