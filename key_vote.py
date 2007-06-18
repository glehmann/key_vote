#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys, pickle, os


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

def printStdOut( s="" ) :
  print s.encode( sys.stdout.encoding ) # très bizarre, mais ça ne fonctionne pas sans ça sur mac

def generateCandidate( candidateSize, min, max, wrong=[] ):
  candidate = []
  for i in range( candidateSize ):
    n = random.randint( min, max )
    while n in candidate:
      n = random.randint( min, max )
    candidate.append( n )
  if candidate == list( wrong ):
    return generateCandidate( candidateSize, min, max, wrong )
  return tuple( candidate )

def readResult( s="", validResults=None ):
  print s,
  res = sys.stdin.readline().strip()
  res = unicode( res, sys.stdin.encoding )
  
  if validResults and res not in validResults :
    printStdOut( u"Réponse invalide." )
    return readResult( s, validResults )
    
  return res
  
def zeroOneTwo( s ):
  if not s.isdigit():
    return None
  i = int( s )
  if 0 <= i <= 2:
    return i
  return None
  
def posToString( pos, ref ):
  s = ""
  for p in pos:
    s += ref[p]
  return s
  
if len( sys.argv ) == 1 :
  printStdOut( "il faut spécifier le nom de fichier où seront stockés les résultats." )
  sys.exit(1)

  
keyboards = {
  u"azerty mac":             ( u"""@&é"'(azertqsdfg<wxcvb""", u"""§è!çà)-yuiop^$hjklmù`n,;:=""" ),
  u"azerty pc":              ( u"""²&é"'(azertqsdfg<wxcvb""", u"""-è_çà)=yuiop^$hjklmù*n,;:!""" ),
  u"bépo 6.2.2.4":           ( u"""@"«»()bépoèauie,êàyh.k""", u"""_+-/*=%çvdlfzwctsnrm^'qgxj""" ),
  u"bépo 6.2.2.4 (test)":    ( u"""@"«»()bépoèauie,êàyh.k""", u"""_+-/*=%^vdljzwctsrnmç'qgxf""" ),
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
  

printStdOut( "\n".join( keyboards.keys() ) )
keyboardName = readResult( "votre clavier: ", keyboards.keys() )
hands = keyboards[ keyboardName ]
  
leftHand,rightHand = hands

d = {}
for i, c in enumerate( leftHand ) :
  d[ str(i) ] = c.upper().rjust(2)
rd = {}
for i, c in enumerate( rightHand ) :
  d[ str( i + 100 ) ] = c.upper().rjust(2)
printStdOut( keyboardTemplate % d )


#nbOfChars = int( readResult( "N-gramme: ") )
nbOfChars = 1

nbOfVotes = 10

if os.path.exists( sys.argv[1] ):
  results = pickle.load( file( sys.argv[1] ) )
else:
  results = {}
        
chars = leftHand.ljust( 100 ) + rightHand
rightHomePos = [(11,), (12,), (13,), (14,)]
leftHomePos = [(115,), (116,), (117,), (118,)]
homePos = rightHomePos + leftHomePos

run = True
nbOfSearch = 0
while run:
  for min, max in [ ( 0, len( leftHand ) - 1 ) ] * nbOfVotes + [ ( 100, 100 + len( rightHand ) - 1 ) ] * nbOfVotes:
    candidate1 = generateCandidate( nbOfChars, min, max )
    candidate2 = generateCandidate( nbOfChars, min, max, candidate1 )
    pair = tuple( sorted( ( candidate1, candidate2 ) ) )
    candidate1, candidate2 = pair
  
    s1 = posToString( pair[0], chars )
    s2 = posToString( pair[1], chars )
  
    if pair not in results:
      nbOfSearch = 0
      if candidate1 in homePos and candidate2 not in homePos :
        results[ pair ] = 1
        printStdOut( "Vote automatique: " + posToString( candidate1, chars ) + " > " + posToString( candidate2, chars ) )
      elif candidate2 in homePos and candidate1 not in homePos :
        results[ pair ] = 2
        printStdOut( "Vote automatique: " + posToString( candidate1, chars ) + " < " + posToString( candidate2, chars ) )
      elif candidate2 in homePos and candidate1 in homePos :
        results[ pair ] = 0
        printStdOut( "Vote automatique: " + posToString( candidate1, chars ) + " = " + posToString( candidate2, chars ) )
      else :
        printStdOut( u"1->  %s     2->  %s     0->  égalité     S->  sauver     Q->  sauver et quitter" % ( s1, s2 ) )
        printStdOut( u"       %i duels réalisés / 556 possibles" % len( results ) )
        res = readResult( "vote: ", ["Q", "S", "0", "1", "2", s1, s2] )
        ires = zeroOneTwo( res )
        if res == "Q":
          run = False
          break
        elif res == "S":
          pickle.dump( results, file( sys.argv[1], "w" ) )
        elif res == s1:
          results[ pair ] = 1
        elif res == s2:
          results[ pair ] = 2
        elif ires != None :
          results[ pair ] = ires
        else:
          printStdOut( u"Erreur dans le programme !" )
        printStdOut()
    else:
      nbOfSearch += 1
      if nbOfSearch > 1000:
        printStdOut( u"Il semble difficile de trouver de nouvelles combinaisons." )
        printStdOut( u"C -> continuer à chercher   Q -> sauver et quitter" )
        printStdOut( u"       %i duels réalisés" % len( results ) )
        res = readResult( u"Choix: ", ["C", "Q"] )
        if res == "Q":
          run = False
          break
        elif res == "C":
          printStdOut( u"Continue à chercher" )
        else:
          printStdOut( u"Erreur dans le programme !" )
        printStdOut()
        
      
    
pickle.dump( results, file( sys.argv[1], "w" ) )

scores = {}
printStdOut( u"Vos votes :" )
for ( pos1, pos2 ), v in results.iteritems():
  printStdOut( posToString( pos1, chars ) + " " + "=><"[v] + " " + posToString( pos2, chars ) )
  
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
  
printStdOut()

ratio = []
for pos, ( lost, total ) in scores.iteritems():
  ratio.append( ( float( total - lost ) / total, pos ) )
  
ratio.sort()
d = {}
for i in range( 0, 126 ) :
  d[ str( i ) ] = "  "
for r, pos in ratio:
  if len( pos ) == 1 :
    if r == 1 :
      d[ str( pos[0] ) ] = "00"
    else :
      d[ str( pos[0] ) ] = str( int( r * 100 ) ).rjust( 2 )
  printStdOut( posToString( pos, chars ) + " " + str( r ) )
  
printStdOut( keyboardTemplate % d )

