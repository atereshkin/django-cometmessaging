import uuid

from django import template

register = template.Library()

@register.inclusion_tag('cometgw/queue.html')
def subscribe(exchange, routing_key, callback):
    return { 'exchange' : exchange,
             'queue' : uuid.uuid4(),
             'routing_key' : routing_key,
             'callback' : callback }
