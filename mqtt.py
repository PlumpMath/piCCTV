from paho.mqtt.client import Client

class Mqtt:
  def __init__(self, handler, topic, addr='localhost', id=None, pw=None):
    self._client = c = Client()
    self._topic_recv = '/control/' + topic
    self._topic_send = topic
    self._handler = handler
    c.on_connect = lambda c, d, r: c.subscribe(self._topic_recv)
    port = 1883
    if ':' in addr:
      addr, port = addr.strip().split(':')
      port = int(port)
    if id:
      c.username_pw_set(id, pw)
    c.connect(addr, port)
    c.message_callback_add(self._topic_recv, self._recv)
    c.loop_start()

  def send(self, msg):
    self._client.publish(self._topic_send, msg)

  def _recv(self, client, data, msg):
    try:
      self._handler(msg.payload.decode())
    except:
      pass