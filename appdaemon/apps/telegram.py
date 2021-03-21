import appdaemon.plugins.hass.hassapi as hass

SERVICE_SEND = 'telegram_bot/send_message'

class TelegramBot(hass.Hass):
    def initialize(self):
        self.listen_event(self.receive_telegram_text, 'telegram_text')

    def receive_telegram_text(self, event_id, payload_event, *args):
        self.log(payload_event)
        text = payload_event['text']
        user_id = payload_event['user_id']
        self.call_service(SERVICE_SEND, target=user_id, message='%s -> Pong' % text)
