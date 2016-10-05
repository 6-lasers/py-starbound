#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import optparse
import os
import os.path
import signal
import struct
import json
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
    p.add_option('--to_json', dest='to_json',
                 action='store_true', default=False,
                 help='dump player file as JSON')
    p.add_option('--from_json', dest='from_json',
                 action='store_true', default=False,
                 help='load JSON into player file')
    p.add_option('-o', '--output_file', dest='output_file',
                 help='output file')
    options, arguments = p.parse_args()
    # Get the path from arguments.
    if len(arguments) != 1:
        p.error('incorrect number of arguments')
    
    if options.from_json:
        # Input file is a JSON file
        try:
            # Open the file
            fh = open(arguments[0], 'r')
            player_json = json.load(fh)
            fh.close()
            player = starbound.sbvj01.SBVJ01(player_json=player_json)
        except Exception as e:
            p.error('could not open file ({})'.format(e))
    else:
        # Input file is a .player file
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
        output_player = True
        
    
    output_player = False
    output_json = False
    
    if options.to_json:
        if options.output_file:
            player_json = {
                'name' : player.name,
                'version' : player.version,
                'data' : player.data
            }
            
            output_json = True
    
    if options.from_json:
        output_player = True
    
    if output_player or output_json:
        if options.output_file:
            # Just to be safe, don't overwrite an existing file
            if os.path.isfile(options.output_file):
                print("ERROR: file {} already exists!".format(options.output_file))
            else:
                if output_player:
                    ofh = open(options.output_file, "wb")
                    player.serialize(ofh)
                    ofh.close()
                if output_json:
                    ofh = open(options.output_file, "w")
                    json.dump(player_json, ofh, indent=2, separators=(',', ': '))
                    ofh.close()
                    
    else:
        print("WARNING: 'version' option selected but with no output file.")
    

if __name__ == '__main__':
    main()
