import appdaemon.plugins.hass.hassapi as hass

class TelegramBot(hass.Hass):
    def initialize(self):
        self.listen_event(self.receive_telegram_callback, 'telegram_callback')
        self.listen_event(self.receive_telegram_command, 'telegram_command')
        self.listen_event(self.receive_telegram_text, 'telegram_text')

    def receive_telegram_callback(self, event_id, payload_event, *args):
        self.log('%s [%s]' % (payload_event, event_id))

    def receive_telegram_command(self, event_id, payload_event, *args):
        self.log('%s [%s]' % (payload_event, event_id))

    def receive_telegram_text(self, event_id, payload_event, *args):
        self.log('%s [%s]' % (payload_event, event_id))
        self.call_service('telegram_bot/send_message', target=payload_event['user_id'], message='You wrote: %s' % payload_event['text'])
