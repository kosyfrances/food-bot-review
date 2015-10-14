#!/usr/bin/env python

import sys
# sys.dont_write_bytecode = True

import glob
import os
import time
import logging
import os.path
from argparse import ArgumentParser


class RtmBot(object):

    def __init__(self, token):
        self.last_ping = 0
        self.token = token
        self.bot_plugins = []
        self.slack_client = None

    def connect(self):
        """Convenience method that creates Server instance"""
        from slackclient import SlackClient

        self.slack_client = SlackClient(self.token)
        self.slack_client.rtm_connect()

    def start(self):
        self.connect()
        self.load_plugins()
        while True:
            print "Bot start function"
            for reply in self.slack_client.rtm_read():
                self.input(reply)
            self.crons()
            self.output()
            self.autoping()
            time.sleep(.5)

    def autoping(self):
        # hardcode the interval to 3 seconds
        now = int(time.time())
        if now > self.last_ping + 3:
            self.slack_client.server.ping()
            self.last_ping = now

    def input(self, data):
        if "type" in data:
            function_name = "process_" + data["type"]
            logging.debug("got {}".format(function_name))
            for plugin in self.bot_plugins:
                plugin.register_jobs()
                plugin.do(function_name, data)

    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                if channel != None and output[1] != None:
                    if limiter == True:
                        time.sleep(.1)
                        limiter = False
                    message = output[1].encode('ascii', 'ignore')
                    channel.send_message("{}".format(message))
                    limiter = True

    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()

    def load_plugins(self):
        for plugin in glob.glob(directory + '/plugins/*'):
            sys.path.insert(0, plugin)
            sys.path.insert(0, directory + '/plugins/')
        for plugin in glob.glob(directory + '/plugins/*.py') + glob.glob(
                directory + '/plugins/*/*.py'):
            logging.info(plugin)
            name = plugin.split('/')[-1][:-3]
            try:
                self.bot_plugins.append(Plugin(name))
            except:
                import traceback
                traceback_msg = traceback.format_exc()
                logging.error("error loading plugin {name} {traceback_msg}".format(name=name, traceback_msg=traceback_msg))


class Plugin(object):
    def __init__(self, name, plugin_config={}):
        self.name = name
        self.jobs = []
        self.module = __import__(name)
        self.register_jobs()
        self.outputs = []
        if name in config:
            logging.info("config found for: " + name)
            self.module.config = config[name]
        if 'setup' in dir(self.module):
            self.module.setup()

    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval("self.module." + function)))
            logging.info(self.module.crontable)
            self.module.crontable = []
        else:
            self.module.crontable = []

    def do(self, function_name, data):
        if function_name in dir(self.module):
            # this makes the plugin fail with stack trace in debug mode
            if not debug:
                try:
                    eval("self.module." + function_name)(data)
                except:
                    logging.debug("problem in module {} {}".format(function_name, data))
            else:
                eval("self.module." + function_name)(data)
        if "catch_all" in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                logging.debug("problem in catch all")

    def do_jobs(self):
        for job in self.jobs:
            job.check()

    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    logging.info("output from {}".format(self.module))
                    output.append(self.module.outputs.pop(0))
                else:
                    break
            else:
                self.module.outputs = []
        return output


class Job(object):
    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0

    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)

    def __repr__(self):
        return self.__str__()

    def check(self):
        if self.lastrun + self.interval < time.time():
            if not debug:
                try:
                    self.function()
                except:
                    logging.debug("problem")
            else:
                self.function()
            self.lastrun = time.time()
            pass


class UnknownChannel(Exception):
    pass


def main_loop():
    print "Main loop function"
    if "LOGFILE" in config:
        logging.basicConfig(filename=config["LOGFILE"], level=logging.INFO,
                            format='%(asctime)s %(message)s')
    logging.info(directory)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logging.exception('OOPS')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()


if __name__ == "__main__":
    print "Bot is started"
    from config import Config

    args = parse_args()
    directory = os.path.dirname(sys.argv[0])
    if not directory.startswith('/'):
        directory = os.path.abspath("{}/{}".format(os.getcwd(),
                                                   directory
                                                   ))
    config = Config()
    if os.path.exists('./rtmbot.conf'):
        config.load_yaml(args.config or 'rtmbot.conf')

    else:
        config.load_os_environ_vars('FB__')

    logging.basicConfig(stream=sys.stdout, filename='debug.log',
                        level=logging.DEBUG if config["DEBUG"] else logging.INFO)
    logging.info('Bot is')
    token = config["SLACK_TOKEN"]
    debug = config["DEBUG"]

    bot = RtmBot(token)
    site_plugins = []
    files_currently_downloading = []
    job_hash = {}

    if config["DAEMON"]:
        import daemon
        with daemon.DaemonContext():
            main_loop()
    else:
        main_loop()
