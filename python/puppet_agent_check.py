#! /usr/bin/env python

import sys
import os
import datetime
import re
import getopt
"""
    NRPE plugin to check if Puppet agent works properly.
    last_run_summary.yaml verification
"""

summary = '/opt/puppetlabs/puppet/cache/state/last_run_summary.yaml'


def ok(message):
    print 'OK: %s' % message
    sys.exit(0)


def warning(message):
    print 'WARNING: %s' % message
    sys.exit(1)


def critical(message):
    print 'CRITICAL: %s' % message
    sys.exit(2)


def unknown(message):
    print 'UNKNOWN: %s' % message
    sys.exit(3)


def time_conversion(secs):
    """Returns a readable time description"""

    days = secs // 86400
    hours = (secs % 86400) // 3600
    minutes = (secs % 3600) // 60
    seconds = secs % 60
    message = '%d seconds ago' % seconds
    if minutes:
        message = '%d minutes and %s' % (minutes, message)
    if hours:
        message = '%d hours, %s' % (hours, message)
    if days:
        message = '%d days, %s' % (days, message)
    return message

def argument_parser():
    warn_sec = 100
    crit_sec = 200
    try:
        opts, args = getopt.getopt(sys.argv[1:], "w:c:h", ['warn=', 'crit=', 'help'])
    except getopt.GetoptError, err:
        usage()

    for opt, arg in opts:
        if opt == "-w":
            warn_sec = arg
        elif opt == "-c":
            crit_sec = arg
        else:
            usage()
    return warn_sec, crit_sec

def usage():
    """ returns nagios status UNKNOWN with 
        a one line usage description
        usage() calls nagios_return()
    """
    unknown('UNKNOWN', 
            "usage: {0} -w warninig".format(sys.argv[0]))

def get_summary_file(summary):
    summary_list = []
    try:
        with open(summary, 'r') as summary_file:
            for line in summary_file.read().splitlines():
                summary_list.append(line)
        summary_file.close()
    except Exception, exc:
        return (critical('Puppet has never run, no %s found. Error: %s' % (summary,exc)))
    try:    
        for line in summary_list:
            if re.search('failed:', line):
                failed = line
            elif re.search('failure', line):
                failure = line
            elif re.search('last_run', line):
                last_run = re.split(': ', line)

        if re.search('[1-9]', failure) and re.search('[1-9]', failed):
            critical('Puppet %s event(s) failure(s) and Puppet %s resource(s) failed.' % (re.split(': ', failure)[1],re.split(': ', failed)[1]))
        elif re.search('[1-9]', failure):
            critical('Puppet %s event(s) failure(s).' % re.split(': ', failure)[1])
        elif re.search('[1-9]', failed):
            critical('Puppet %s resource(s) failed.' % re.split(': ', failed)[1])
        return (failed, failure, last_run)
    except Exception, exc:
        return (critical('Puppet last_run format error: %s' % exc))


def get_total_seconds(td): return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6

def main():
    warn_seconds, crit_seconds = argument_parser()
    # Check last_run time on summary file
    now = datetime.datetime.now()
    failed, failure, last_run = get_summary_file(summary)
    last_run_time = datetime.datetime.fromtimestamp(int(last_run[1]))
    diff_time = now - last_run_time
    diff_sec = get_total_seconds(diff_time)
    last_run = 'Puppet last run was %s' % time_conversion(int(diff_sec))

    if last_run_time > now:
        warning('Time syncing issue!')
    elif diff_sec > crit_seconds:
        critical(last_run)
    elif diff_sec > warn_seconds:
        warning(last_run)
    else:
        ok(last_run)

main()
