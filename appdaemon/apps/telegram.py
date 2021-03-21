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

"""
Cheatsheet
==========

https://www.home-assistant.io/integrations/telegram_bot/

Available services
==================

send_message, send_photo, send_video, send_animation,
send_voice, send_sticker, send_document, send_location,
edit_message, edit_caption, edit_replymarkup,
answer_callback_query, delete_message, leave_chat

Event triggering
================

telegram_command
----------------

A command looks like /thecommand or /othercommand with some args.

When received by Home Assistant it will fire a telegram_command event
on the event bus with the following event_data:

command: "/thecommand"
args: "<any other text following the command>"
from_first: "<first name of the sender>"
from_last: "<last name of the sender>"
user_id: "<id of the sender>"
chat_id: "<origin chat id>"
chat: "<chat info>"

telegram_text
-------------

Any other message not starting with / will be processed as simple text,
firing a telegram_text event on the event bus with the following event_data:

text: "some text received"
from_first: "<first name of the sender>"
from_last: "<last name of the sender>"
user_id: "<id of the sender>"
chat_id: "<origin chat id>"
chat: "<chat info>"

telegram_callback
-----------------

If the message is sent from a press from an inline button, for example,
a callback query is received, and Home Assistant will fire a telegram_callback
event with:

data: "<data associated to action callback>"
message: <message origin of the action callback>
from_first: "<first name of the sender>"
from_last: "<last name of the sender>"
user_id: "<id of the sender>"
id: "<unique id of the callback>"
chat_instance: "<chat instance>"
chat_id: "<origin chat id>"
"""
