# -*- coding: utf-8 -*-
# key vote common functions

import sys

keyboards = {
  u"azerty mac":             ( u"""@&é"'(azertqsdfg<wxcvb""", u"""§è!çà)-yuiop^$hjklmù`n,;:=""" ),
  u"azerty pc":              ( u"""²&é"'(azertqsdfg<wxcvb""", u"""-è_çà)=yuiop^$hjklmù*n,;:!""" ),
  u"bépo 6.2.2.4":           ( u"""@"«»()bépoèauie,êàyh.k""", u"""_+-/*=%çvdlfzwctsnrm^’qgxj""" ),
  u"bépo 6.2.2.4 (test)":    ( u"""@"«»()bépoèauie,êàyh.k""", u"""_+-/*=%^vdljzwctsrnmç'qgxf""" ),
  u"bépo 6.2.3":             ( u"""@"«»()bépoèauie,êàyh.k""", u"""_+-/*=%çvdlfzwctsnrm^'qgxj""" ),
  u"bépo Olivier":           ( u"""@"«»()ébpoèauie,êàyh.k""", u"""_+-/*=%^vdlfzwctsrnmç'qgxj""" ),
}

keyboardTemplate = u"""
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

if sys.platform == "win32":
	# no (easy) color support
	redColor = u""
	noColor = u""
else: # terminal color for Linux & MacOSX
	redColor = u"\033[31;1m"
	noColor = u"\033[0m"

# print a string on stdout
# whith the good charset
def printStdOut( s="", endl=True ) :
	encoding = sys.stdout.encoding
	if not encoding :
		encoding = sys.getdefaultencoding()
	print s.encode( encoding, 'replace' ), # très bizarre, mais ça ne fonctionne pas sans ça sur mac
	if endl :
		print

# read the result from the choice
# return the character, retry if needed until a good reply is provided
def readResult( s="", validResults=None ):
	encoding = sys.stdout.encoding
	if not encoding :
		encoding = sys.getdefaultencoding()
	printStdOut( s, False )
	res = sys.stdin.readline().strip()
	res = unicode( res, encoding, 'replace' )
	
	if validResults and res not in validResults :
		printStdOut( u"Réponse invalide." )
		return readResult( s, validResults )
		
	return res

# take a char and return the corresponding integer
# return None if it's not an integer, or if the integer is not 0,1 or 2
def zeroOneTwo( s ):
	if not s.isdigit():
		return None
	i = int( s )
	if 0 <= i <= 2:
		return i
	return None

def printKbdLayout(keyboard, chars=None):
	d = {}
	for handID in (0,1):
		for (i,c) in enumerate( keyboard[handID] ):
			if chars!=None and c in chars: # highlight it
				d[ str(i + handID*100) ] = redColor + c.upper().rjust(2) + noColor
			else:
				d[ str(i + handID*100) ] = c.upper().rjust(2)
	printStdOut( keyboardTemplate % d )

def printKbdScores(keyboard, scores): # { key1 => score1 ; key2 => score2 ; ... }
	d = {}
	for handID in (0,1):
		for (i,c) in enumerate( keyboard[handID] ):
			if c in scores.keys():
				if scores[c] == 1: # should display '100'
					d[ str(i + handID*100) ] = '00' # we display '00'
				else:
					d[ str(i + handID*100) ] = str(int(scores[c]*100)).rjust( 2 )
			else:
				d[ str(i + handID*100) ] = '  ' # untested keys displayed as spaces
	printStdOut( keyboardTemplate % d )
	for char in scores:
		printStdOut( char + ' ' + str(scores[char]) )

def chooseKbd():
	printStdOut( "\n" )
	possibleResults = keyboards.keys()
	for (i,k) in enumerate( keyboards.keys() ):
		printStdOut( str(i) + ' : ' + k )
		possibleResults.append(str(i))
	#printStdOut( 'possible results : ' + str(possibleResults) )
	kbdindex = readResult( "votre clavier: ", possibleResults )
	if kbdindex.isdigit():
		return keyboards[keyboards.keys()[int(kbdindex)]]
	else:
		return keyboards[kbdindex]

if sys.version < '2.4' :
	def sorted(iterable, cmp=None, key=None, reverse=False) :
		i = list(iterable)
		if key :
			d = {}
			for v in iterable :
				k = key(v)
				if not d.has_key(k) :
					d[k] = []
				d[k].append(v)
			keys = d.keys()
			keys.sort(cmp)
			i = []
			for k in keys :
				i += d[k]
		else :
			i.sort(cmp)
		if reverse :
			i.reverse()
		return i

def posToString( pos, kbd ):
	ref = kbd[0].ljust( 100 ) + kbd[1]
	s = ""
	for p in pos:
		s += ref[p]
	return s

def stringToPos( s, kbd ):
	ref = kbd[0].ljust( 100 ) + kbd[1]
	pos = []
	for c in s:
		pos.append( ref.find( c ) )
	return tuple( pos )

def cancelDuel(results, kbd):
	chars = kbd[0].ljust( 100 ) + kbd[1]
	printStdOut( u'Annulation de duel' )
	
	i = 0
	possible = []
	for pair in results.keys():
		printStdOut(str(i) + ' : ' + posToString(pair[0], kbd) + ' ' + '=><'[results[pair]] + ' ' + posToString(pair[1], kbd))
		possible.append(str(i))
		i = i+1
	
	pos = int(readResult( u'choix : ', possible ))
	i = 0
	for pair in results.keys():
		if i == pos:
			del results[pair]
			printStdOut( u'Le duel est annulé. Vour pourrez revoter pour ce duel plus tard.' )
			return
		i = i+1
