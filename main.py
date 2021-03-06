#! /usr/bin/env python

import sys
import logging
from logging import debug, info
import argparse
import lxc
import handlers

command_handlers = {
    'grant-storage': handlers.GrantStorageHandler()
}

class CommandLineHandler(object):
    def run(self, args):
        ns = self.initialize(args)
        handler = command_handlers[ns.command]
        handler.run(ns.rest_args)
        
    def initialize(self, args):
        parser = argparse.ArgumentParser()

        parser.add_argument('command', choices=['grant-storage'])

        parser.add_argument(
            '--log-level', metavar="LEVEL", type=str, help="Log level",
            default='INFO'
        )
        parser.add_argument('rest_args', metavar="ARGS", nargs='*')            
        ns = parser.parse_args(args)

        logging.basicConfig(
            level=getattr(logging, ns.log_level),            
            format="%(asctime)s - %(levelname)8s - %(name)s - %(message)s"
        )

        return ns

if __name__ == "__main__":
    obj = CommandLineHandler()
    obj.run(sys.argv[1:])
