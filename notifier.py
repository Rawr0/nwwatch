from abc import ABCMeta, abstractmethod
from multiprocessing.dummy import Pool as ThreadPool
import threading
import sys


# Imports used by plugins
import requests         # NotifyByPushover, NotifyByDiscord
import datetime         # NotifyByPushover

import json             # NotifyBySMS


# Import Custom Classes
import config as cfg

class Notifier:
    """Base class for all plugins. Singleton instances of subclasses are created automatically and stored in Notifier.plugins class field."""
    plugins = []   

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.plugins.append(cls())

    def internalNotify(self, obj):
        try:
            self.log("Triggering plugin: " + type(obj).__name__)
            obj.notify()
        except Exception as exc:
            self.log('Unexpected exception while processing {}. Error: {}'.format(type(obj).__name__, exc))

    def triggerNotificationThreaded(self):
        enabledPlugins = []

        if len(cfg.PLUGINS_ENABLED) == 0:
            self.log("You haven't enabled any notifications. Follow the README to get started")
            return

        # Get enabled plugins
        for plugin in self.plugins:
            if type(plugin).__name__ in cfg.PLUGINS_ENABLED:
                enabledPlugins.append(plugin)

        pool = ThreadPool(4)      
        pool.map(self.internalNotify, enabledPlugins)
        pool.close()
        pool.join()

    def triggerNotification(self):
        for plugin in self.plugins:
            if type(plugin).__name__ in cfg.PLUGINS_ENABLED:
                try:
                    self.log("Triggering plugin: " + type(plugin).__name__)
                    plugin.notify()
                except Exception as exc:
                    self.log('Unexpected exception while processing {}. Error: {}'.format(type(plugin).__name__, exc))

    def log(self, message):
        sys.stdout.write(message + "\n")

    @abstractmethod
    def notify(self, *test):
        raise NotImplementedError       

#######################################
## ADD NEW SUBCLASSES BELOW THE LINE
#######################################

# class NotifyByEmail(Notifier):
#     def notify(self):
#       [Put your python code here]

class NotifyByPushover(Notifier):
    def getMessage(self):
        message = "It\'s game time"
        return message

    def notify(self):
        # Send a notification
        time = datetime.datetime.now().strftime("%H:%M:%S")
        priority = (1 if cfg.PUSHOVER_HIGHPRIORITY else 0)

        postdata = {'token':cfg.PUSHOVER_TOKEN,
            'user':cfg.PUSHOVER_USER,
            'title':"New World",
            'message':'🆕🌎 ' + self.getMessage() + ' (' + time + ')',
            'device':cfg.PUSHOVER_DEVICE,
            'priority':priority
        }
        requests.post('https://api.pushover.net/1/messages.json', postdata)


class NotifyByDiscord(Notifier):
    def getMessage(self):
        message = "It\'s game time"
        return message

    def notify(self):
        # Send a notification
        postdata = {
            'content':self.getMessage(),
            'tts': cfg.DISCORD_TTS
        }
        requests.post(cfg.DISCORD_WEBHOOKURL, postdata)            

class NotifyBySMS(Notifier):
    debug = False

    def getMessage(self):
        message = "It\'s game time"
        return message

    def notify(self):
        # Send a notification
        time = datetime.datetime.now().strftime("%H:%M:%S")

        postdata = {
            'from':cfg.SMS_SOURCE,
            'to':[cfg.SMS_TARGET],
            'body':'🆕🌎 ' + self.getMessage() + ' (' + time + ')'
        }
        
        headers = {
            'Content-Type':'application/json',
            'Authorization': 'Bearer {}'.format(cfg.SMS_TOKEN)
        }

        res = requests.post('https://api.clxcommunications.com/xms/v1/{}/batches'.format(cfg.SMS_PLAN_ID), data=json.dumps(postdata), headers=headers)
        if(self.debug): self.log(res.text)
