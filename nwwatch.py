import sys
import time
import os
import datetime
import re

# Plugins
from os.path import dirname, basename, isfile
from notifier import Notifier

# Import Custom Classes
import config as cfg

class ConsoleLogger():
    @staticmethod
    def log(message):
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print("[" + time + "] " + message)

class Util():
    @staticmethod
    def minutesBetweenTimes(time1, time2, absolute=True):
        minutes = int((time1 - time2).total_seconds()/60)
        if(absolute):
            minutes = abs(minutes)

        return minutes


def tail(f, lines=1, _buffer=4098):
    """Tail a file and get X lines from the end"""
    # Credit to glenbot (https://stackoverflow.com/questions/136168/get-last-n-lines-of-a-file-similar-to-tail)
    
    # place holder for the lines found
    lines_found = []

    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()

        # we found enough lines, get out
        # decrement the block counter to get the
        # next X bytes
        block_counter -= 1

    return lines_found[-lines:]

if __name__ == "__main__":
    print("[Watching] " + cfg.LOGFILE)
    waitingInQueue = True
    queueStartTime = None
    queuePosition = "0"
    currentTime = None
    jumpedQueue = "0"
    elapsedTime = None
    jumpindex = 0
    totaljumped = 0
    avgJumped = 0
    remainingJumps = 0
    totalTimeElapsed = None
    timeleft = 0
    startingPosition = 0

    # If test mode
    if(cfg.TEST_MODE):
        ConsoleLogger.log("TEST MODE ENABLED - TESTING NOTIFICATIONS")
        Notifier().triggerNotificationThreaded()
        ConsoleLogger.log("Notifications sent. Quitting. If notifications are working well, update your config.py to set TEST_MODE to False")
        sys.exit()

    while waitingInQueue:
        try:
            f = open(cfg.LOGFILE, "r")
            logtail = tail(f,cfg.NW_LOGFILE_CHECK_LENGTH)
            f.close()

            # Look at the last entry first
            logtail.reverse()
            
            for line in logtail:
                searchResult = re.search(cfg.NW_SEARCH_REGEX, line)

                if(searchResult is not None):
                    # Start timing
                    if(queueStartTime is None):
                        queueStartTime = datetime.datetime.now()
                        # Save for first jump
                        prevTime = queueStartTime

                    currentTime = datetime.datetime.now()
                    totalTimeElapsed = currentTime - queueStartTime
                    
                    # Extract position
                    jumpedQueue = 0
                    elapsedTime = 0
                    prevQueuePosition = queuePosition
                    queuePosition = searchResult[cfg.NW_SEARCH_REGEX_INDEX]
                    if (startingPosition == 0):
                        startingPosition = int(queuePosition)

                    if (int(prevQueuePosition) - int(queuePosition) > 0):
                        elapsedTime = currentTime - prevTime
                        # calculate queue positions down + time gone by
                        jumpedQueue = int(prevQueuePosition) - int(queuePosition)
                        # Counter of jumps done
                        jumpindex = jumpindex + 1
                        # Calculate remaining jumps
                        totaljumped = totaljumped + jumpedQueue
                        avgJumped = totaljumped / jumpindex
                        remainingJumps = int(queuePosition) / int(avgJumped)
                        # calulate avg time between jumps
                        avgJumpTime = (totalTimeElapsed.total_seconds()) / jumpindex
                        # calculate approximate time left
                        # convert avgJumpTime to minutes and then to int
                        timeleft = (int(avgJumpTime) * int(remainingJumps)) // 60
                        # Save time for next jump
                        prevTime = currentTime
                        # output only if jumped position
                        ConsoleLogger.log("Position in queue: " + queuePosition + " | Time left: ~ " + str(timeleft) + " min")

                    if(int(queuePosition) <= cfg.NW_ALERT_AT_QUEUE_POSITION):
                        Notifier().triggerNotificationThreaded()
                        waitingInQueue = False
                    
                    break
            
            if waitingInQueue:        
                time.sleep(cfg.NW_FILE_CHECK_FREQUENCY)

        except OSError as e:
            ConsoleLogger.log("[ERROR] I/O error {0}: {1}".format(e.errno, e.strerror))
            sys.exit()   

    print("Queue is almost ready. Enjoy New World!")
    print("Time in queue: " + str(Util.minutesBetweenTimes(datetime.datetime.now(), queueStartTime)) + " minutes")
