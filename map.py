#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, pickle

keyboardTemplate = """
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────╔════════╗
│    │    │    │    │    │    │    │    │    │    │    │    │    ║        ║
│ %(0)s │ %(1)s │ %(2)s │ %(3)s │ %(4)s │ %(5)s │ %(100)s │ %(101)s │ %(102)s │ %(103)s │ %(104)s │ %(105)s │ %(106)s ║ <--    ║
╔═══════╗─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─┴──┬─╚══╦═════╣
║  |<-  ║    │    │    │    │    │    │    │    │    │    │    │    ║   | ║
║  ->|  ║ %(6)s │ %(7)s │ %(8)s │ %(9)s │ %(10)s │ %(107)s │ %(108)s │ %(109)s │ %(110)s │ %(111)s │ %(112)s │ %(113)s ║ <-' ║
╠═══════╩╗───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───┴┬───╚╗    ║
║        ║    │    │    │    │    │    │    │    │    │    │    │    ║    ║
║  CAPS  ║ %(11)s │ %(12)s │ %(13)s │ %(14)s │ %(15)s │ %(114)s │ %(115)s │ %(116)s │ %(117)s │ %(118)s │ %(119)s │ %(120)s ║    ║
╠══════╦═╝──┬─┴──┬─┴──┬─┴─══─┴──┬─┴──┬─┴─══─┴──┬─┴──┬─┴──┬─┴──╔══════╩════╣
║   ^  ║    │    │    │    │    │    │    │    │    │    │    ║     ^     ║
║   |  ║ %(16)s │ %(17)s │ %(18)s │ %(19)s │ %(20)s │ %(21)s │ %(121)s │ %(122)s │ %(123)s │ %(124)s │ %(125)s ║     |     ║
╠══════╩╦══════╦═════╦═══════════════════════╦═══════╦══════╦═╩════╦══════╣
║       ║      ║     ║                       ║       ║      ║      ║      ║
║ Ctrl  ║ WinG ║ Alt ║  SPACE                ║ AltGr ║ WinD ║ WinM ║ Ctrl ║
╚═══════╩══════╩═════╩═══════════════════════╩═══════╩══════╩══════╩══════╝
"""
  
scores = {}
nbOfVotes = 0

for fName in sys.argv[1:] :
  f = file( fName )
  results = pickle.load( f )

  for ( pos1, pos2 ), v in results.iteritems():
  #  printStdOut( posToString( pos1, chars ) + " " + "=><"[v] + " " + posToString( pos2, chars ) )
  
    lost, total = scores.get( pos1, ( 0, 0 ) )
    total += 1
    if v == 2:
      lost += 1
    scores[ pos1 ] = ( lost, total )
  
    lost, total = scores.get( pos2, ( 0, 0 ) )
    total += 1
    if v == 1:
      lost += 1
    scores[ pos2 ] = ( lost, total )
    
    nbOfVotes += 1
    
  f.close()
  
print nbOfVotes, "votes."

ratio = []
for pos, ( lost, total ) in scores.iteritems():
  ratio.append( ( float( total - lost ) / total, pos ) )
  
ratio.sort()
d = {}
for i in range( 0, 126 ) :
  d[ str( i ) ] = "  "
for r, pos in ratio:
  if r == 1 :
    d[ str( pos[0] ) ] = "00"
  else :
    d[ str( pos[0] ) ] = str( int( r * 100 ) ).rjust( 2 )
  
print keyboardTemplate % d

