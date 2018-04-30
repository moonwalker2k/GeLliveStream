#!/usr/bin/python3
#-*- coding:utf-8 -*-
import subprocess
import sys
import os
import argparse
from DouYu import packet_handler


def start():
    stdout=sys.stdout
    stdin=sys.stdin
    stderr=sys.stderr
    parser = argparse.ArgumentParser(prog='proxy_server',
                                     description='start mitmdump with packet_handler.py')
    script = packet_handler.__file__

    parser.add_argument('-p', '--p',dest='port', default='8080',
                        action='store', type=str, help='使用指定的端口')
    args = parser.parse_args()
    subprocess.call(['mitmdump', '-p', args.port, '-s', script],
                    stdout=stdout, stdin=stdin, stderr=stderr)


if __name__ == '__main__':
    start()
