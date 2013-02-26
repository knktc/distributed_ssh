#!/usr/bin/env python
# -*- coding: utf-8 -*-
# distributed_ssh.py
# created on 2013-02-24
# read the README file for more info

"""
@author:knktc
@contact:me@knktc.com
"""

import os
import sys
import getopt
import paramiko

arguments = {"hosts_list": "",
             "command": "",
             }


def help_content():
    """
    help content
    """
    print """
This script is
Usage: distributed_ssh.py -h hosts_list -c command

"""


def option_parser(arguments):
    """
    an option parser
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:c:", ["help"])
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(1)

    if opts == []:
        help_content()
        sys.exit(0)

    for option, value in opts:
        if option == "-h":
            arguments["hosts_list"] = value
        elif option == "-c":
            arguments["command"] = value
        elif option == "--help":
            help_content()
            sys.exit(0)

    return arguments


def host_info_parser(host_info):
    """
    parse host info
    """
    hostname = ""
    port = 22
    username = ""
    password = ""
    flag = True
    if len(host_info) == 0:
        flag = False
    elif host_info[0] == '#':
        flag = False
    else:
        splited_info = host_info.split()
        if len(splited_info) != 3:
            flag = False
        else:
            username = splited_info[1]
            password = splited_info[2]
            if splited_info[0].find(":") != -1:
                hostname, port = splited_info[0].split(":")
            else:
                hostname = splited_info[0]
            flag = True
    if flag:
        return True, hostname, port, username, password
    else:
        return False, hostname, port, username, password

class remote_host(object):
    def __init__(self, hostname, username, password, port=22, timeout=60):
        """
        create ssh connection object with connection info
        """
        self.ssh_conn = None
        self.ssh_conn = paramiko.SSHClient()
        self.ssh_conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh_conn.connect(hostname=hostname, port=port, username=username, password=password, timeout=timeout)
        except Exception, err:
            self.ssh_conn = None

    def run_ssh(self, cmd):
        """
        run ssh in remote server
        """
        i, o, e = self.ssh_conn.exec_command(cmd)
        print o.read(), e.read()

    def close(self):
        """
        close connection
        """
        self.ssh_conn.close()
        self.ssh_conn = None

if __name__ == '__main__':
    conf_dict = option_parser(arguments)
    hosts_list_file = os.path.abspath(conf_dict['hosts_list'])
    command = conf_dict['command']
    print "command: %s" % command
    print ""
    if not os.path.isfile(hosts_list_file):
        print "no such hosts list file!"
        sys.exit(1)
    else:
        hosts_list = open(hosts_list_file, 'rb').readlines()
        if len(hosts_list) == 0:
            print "the hosts list file is empty!"
            sys.exit(1)
        else:
            for single_host in hosts_list:
                hosts_info = host_info_parser(single_host)
                if hosts_info[0]:
                    hostname = hosts_info[1]
                    port = int(hosts_info[2])
                    username = hosts_info[3]
                    password = hosts_info[4]
                    print "%s@%s:%s" % (username, hostname, port)
                    host = remote_host(hostname=hostname, port=port, username=username, password=password)
                    host.run_ssh(command)
                else:
                    continue




