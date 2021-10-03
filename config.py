#!/usr/bin/env python
import os

LOGFILE = os.environ['LOCALAPPDATA'] + "\\AGS\\New World\\Game.log"

# INSTRUCTIONS
# 1. Uncomment the names of the plugins you wish to use
# 2. Configure the relevant variables below

###############################
##      PLUGIN SETTINGS      ##
###############################
# It is recommended you leave these two as default, no testing has been performed with different values
NW_FILE_CHECK_FREQUENCY = 60           # How frequently the script checks your queue position. Default: 60
NW_ALERT_AT_QUEUE_POSITION = 25        # Send a notification when you are at this position in queue (or less). It is recommended this be 25 or greater. 

PLUGINS_ENABLED = {                    # Remove the hash (#) before a line to enable it
    #"NotifyByPushover",
    #"NotifyBySMS",
    #"NotifyByDiscord"
}

# Want to test your notifications? Enable it above and then set "TEST_MODE" to True. A notification will be triggered as soon as the script starts
TEST_MODE = True

###############################
## PLUGIN SPECIFIC VARIABLES ##
###############################
# Plugin: NotifyByPushover
PUSHOVER_TOKEN = "<VALUEHERE>"
PUSHOVER_USER = "<VALUEHERE>"
PUSHOVER_DEVICE = "<VALUEHERE>"
PUSHOVER_HIGHPRIORITY = True

# Plugin: NotifyBySMS (sinch.com)  (Note: Paid service)
# Note: The SMS provider is currently going through a rebranding and, as a result, the APIs below could stop working. 
# If any issues are encountered, please raise an issue on Github
SMS_PLAN_ID = ""
SMS_TOKEN = ""
SMS_SOURCE = "New World"     # Must be a valid MSISDN, short code or alphanumeric originator (see https://www.sinch.com/docs/sms/http-rest.html#request)
SMS_TARGET = ""     # Destination phone number, including country code (eg. +15555551234 or +61411000000)

# Plugin: NotifyByDiscord
# In a Discord server you own/manage, navigate to Server Settings -> Integrations -> Webooks -> New Webhook. Click "Copy Webhook URL" and paste it below
DISCORD_WEBHOOKURL = "https://discord.com/api/webhooks/xxxxxxxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DISCORD_TTS = False     # Use Discord "Text to speech" to speak the announcement


###############################
## INTERNAL VARIABLES ##
###############################
# Don't change these unless you're having issues

NW_LOGFILE_CHECK_LENGTH = 100             # Number of lines to monitor in the logfile
NW_SEARCH_REGEX = ".*Waiting in login queue.*Position \((.*)\)$"
NW_SEARCH_REGEX_INDEX = 1