#!/usr/bin/python

import os
import logging
from subprocess import call, check_output
import psutil

SER2NET_CONTROLPORT = 2000
SER2NET_CONFIG = "/etc/ser2net.conf"

class Ser2Net(object):
    def __init__(self, config=SER2NET_CONFIG):
        self.__config = config

        # stop running indiserver, if any
        self.stop()

    def __run(self):
        cmd = 'ser2net -p %d -c %s' % \
            (SER2NET_CONTROLPORT, self.__config)
        logging.info(cmd)
        call(cmd, shell=True)

    def start(self):
        if self.is_running():
            self.stop()

        self.__run()

    def stop(self):
        cmd = ['pkill', '-9', 'ser2net']
        logging.info(' '.join(cmd))
        ret = call(cmd)
        if ret == 0:
            logging.info('ser2con terminated successfully')
        else:
            logging.warn('terminating ser2con failed code ' + str(ret))

    def is_running(self):
        for proc in psutil.process_iter():
            if proc.name() == 'ser2net':
                return True
        return False

