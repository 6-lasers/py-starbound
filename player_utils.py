#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import optparse
import os
import os.path
import signal
import struct
import pprint

import starbound
import starbound.sbvj01
import starbound.versioning

pp = pprint.PrettyPrinter(indent=2)

try:
    # Don't break on pipe signal.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except:
    # Probably a Windows machine.
    pass


# Override range with xrange when running Python 2.x.
try:
    range = xrange
except:
    pass


def main():
    p = optparse.OptionParser('Usage: %prog [options] <input file>')
    p.add_option('-p', '--print', dest='print',
                 action='store_true', default=False,
                 help='print player data')
    p.add_option('-v', '--version', dest='version',
                 help='upgrade player file to version')
    options, arguments = p.parse_args()
    # Get the path from arguments.
    if len(arguments) != 1:
        p.error('incorrect number of arguments')
    try:
        # Open the file
        fh = open(arguments[0], 'rb')
        file_size = os.fstat(fh.fileno()).st_size
        player = starbound.sbvj01.SBVJ01(fh)
        fh.close()
    except Exception as e:
        p.error('could not open file ({})'.format(e))
    
    # Just pretty print the player data
    if options.print:
        pp.pprint(player.deserialize())
    
    if options.version:
        if int(options.version) == 25:
            starbound.versioning.upgrade_player_12_25(player)

if __name__ == '__main__':
    main()
