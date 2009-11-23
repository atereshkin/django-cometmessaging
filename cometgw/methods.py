from carrot.connection import DjangoBrokerConnection
from carrot.messaging import Publisher

conn = DjangoBrokerConnection()

def send(exchange, routing_key, msg):
    publisher = Publisher(connection=conn,
                          exchange=exchange,
                          routing_key=routing_key)
    publisher.send(msg)
    publisher.close()

