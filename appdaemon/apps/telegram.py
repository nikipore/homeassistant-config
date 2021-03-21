from collections import namedtuple
from appdaemon.plugins.hass import hassapi

TELEGRAM_BOT = 'telegram_bot/%s'

class TelegramBot(hassapi.Hass):
    COMMANDS = {'/menu'}

    def initialize(self):
        self.listen_event(self.receive_telegram_callback, 'telegram_callback')
        self.listen_event(self.receive_telegram_command, 'telegram_command')
        self.listen_event(self.receive_telegram_text, 'telegram_text')

    def receive_telegram_command(self, event_id, payload_event, *args):
        self.log('%s [%s]' % (payload_event, event_id))
        if payload_event['command'] not in self.COMMANDS:
            return
        
        inline_keyboard = [[
            ('Ping', '/ping')
            , ('Pong', '/pong')
        ]]
        self.send_message(
            'Please choose:'
            , inline_keyboard=inline_keyboard
            , target=payload_event['user_id']
        )

    def receive_telegram_callback(self, event_id, payload_event, *args):
        self.log('%s [%s]' % (payload_event, event_id))
        self.answer_callback_query(
            'You chose: `%s`' % payload_event['command']
            , payload_event['id']
        )

    def receive_telegram_text(self, event_id, payload_event, *args):
        self.log('%s [%s]' % (payload_event, event_id))
        self.send_message(
            payload_event['text']
            , title='You wrote:'
            , target=payload_event['user_id']
        )
    
    def send_message(self, message, **kwargs):
        self.call_service(TELEGRAM_BOT % 'send_message', message=message, **kwargs)

    def answer_callback_query(self, message, callback_query_id, **kwargs):
        self.call_service(TELEGRAM_BOT % 'send_message', message=message, callback_query_id=callback_query_id, **kwargs)

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

"""
