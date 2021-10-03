# nwwatch - Monitor the New World queue and notify when it is about to finish

## Getting Started
1. install python 3.7+

2. navigate to the directory where you unzipped / cloned this script to 

3. open a command prompt in that directory, install requirements using `pip3 install -r requirements.txt`

4. edit `config.py` to enable/disable the notification plugins you want (see PLUGIN SETTINGS and PLUGIN SPECIFIC VARIABLES sections)

5. start New World

6. run the script using `python3 .\nwwatch.py`. Events enabled within config.py will automatically trigger when the queue threshold (defined in config.py) is met

Once you've done initial setup, you can jump straight to Step 5 going forward.

Want to test your notifications? Set "TEST_MODE" to True in the config.py file. A notification will be triggered as soon as the script starts

## How

New World creates a `Game.log` each time you start the game. Queue progress is logged to this file. nwwatch monitors the status of the queue, as recorded in the logfile, and triggers notification events as a result.

## FAQ

### What notification types are supported
* Out of the box nwwatch supports the following notification types:
    * [Pushover](https://pushover.net) push notifications (e.g. iOS/Android),
    * [Discord Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
    * SMS notifications (via sinch.com)

* Additional notification types can be implemented by adding extra python code to `notifier.py`. Nwwatch will automatically instantiate and call the notify() method on all subclasses of the Notifier class defined within this file. 
```
class NotifyByMyDesiredMethod(Notifier):
     def notify(self):
       [Put your custom python code here]
```

### What languages are supported
* English only at the moment. It should be reasonably easy to adapt for other languages by updating the NW_SEARCH_REGEX parameter in config.py. 

### Is use of this script allowed by Amazon Games?
* The script does not make any modifications to New World files (it simply reads the game logfile) so you should be fine. However you run this at your own risk.

### I need more help?
* Try the [Wiki](https://github.com/Rawr0/nwwatch/wiki) for a sample config.py

## Example Screenshots
Enabling/Disabling Plugins via config.py (remember to populate the entries under 'Plugin Specific Variables' too)

![nwwatch-config2](https://user-images.githubusercontent.com/18738504/135720182-fef5d758-0f0d-49e8-8008-dae8473da81b.png)

Log Monitoring

![nwwatch](https://user-images.githubusercontent.com/18738504/135712635-e31d3d9f-2432-4cb0-9c04-3d9dae85e320.png)

Example Notification

![nwwatch-discord](https://user-images.githubusercontent.com/18738504/135712639-3ca713eb-f334-4961-896d-47dabbdae6f6.png)
