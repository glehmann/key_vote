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

def readResult( s="" ):
  print s,
  res = sys.stdin.readline().strip()
  if res == "":
    return readResult( s )
  return unicode( res, sys.stdin.encoding )
  
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
  u"azerty pc":              ( u"""²&é"'(azertqsdfg<wxcvb""", u"""-è_çà)=yuiop^$hjklmù`n,;:=""" ),
  u"bépo 6.2.2.4":           ( u"""@"«»()bépoèauie,êàyh.k""", u"""_+-/*=%çvdlfzwctsnrm^'qgxj""" ),
  u"bépo 6.2.2.4 (test)":    ( u"""@"«»()bépoèauie,êàyh.k""", u"""_+-/*=%^vdljzwctsrnmç'qgxf""" ),
}

keyboardName = readResult( "\n".join( keyboards.keys() ) + "\nvotre clavier: ")
hands = keyboards[ keyboardName ]
  
leftHand,rightHand = hands

#nbOfChars = int( readResult( "N-gramme: ") )
nbOfChars = 1

nbOfVotes = 10

if os.path.exists( sys.argv[1] ):
  results = pickle.load( file( sys.argv[1] ) )
  printStdOut()
  printStdOut( "%i votes dans le fichier" % len( results ) )
  printStdOut()
else:
  results = {}

  for i in range( 11, 15 ):
    for i2 in range( i + 1, 15 ):
      results[ ( (i,), (i2,) ) ] = 0
  for i in range( 0, 11 ):
    for i2 in range( 11, 15 ):
      results[ ( (i,), (i2,) ) ] = 2
  for i in range( 15, len( leftHand ) ):
    for i2 in range( 11, 15 ):
      results[ ( (i2,), (i,) ) ] = 1
           
  for i in range( 15, 19 ):
    for i2 in range( i + 1, 19 ):
      results[ ( ( 100 + i,), ( 100 + i2,) ) ] = 0
  for i in range( 0, 15 ):
    for i2 in range( 15, 19 ):
      results[ ( ( 100 + i,), ( 100 + i2,) ) ] = 2
  for i in range( 19, len( rightHand ) ):
    for i2 in range( 15, 19 ):
      results[ ( ( 100 + i2,), ( 100 + i,) ) ] = 1
        
chars = leftHand.ljust( 100 ) + rightHand

run = True
nbOfSearch = 0
while run:
  for min, max in [ ( 0, len( leftHand ) - 1 ) ] * nbOfVotes + [ ( 100, 100 + len( rightHand ) - 1 ) ] * nbOfVotes:
    candidate1 = generateCandidate( nbOfChars, min, max )
    candidate2 = generateCandidate( nbOfChars, min, max, candidate1 )
    pair = tuple( sorted( ( candidate1, candidate2 ) ) )
  
    s1 = posToString( pair[0], chars )
    s2 = posToString( pair[1], chars )
  
    if pair not in results:
      nbOfSearch = 0
      printStdOut( u"1->  %s     2->  %s     0->  égalité     S->  sauver     Q->  sauver et quitter" % ( s1, s2 ) )
      res = readResult( "vote: " )
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
        printStdOut( u"Réponse invalide" )
      printStdOut()
    else:
      nbOfSearch += 1
      if nbOfSearch > 1000:
        printStdOut( u"Il semble difficile de trouver de nouvelles combinaisons." )
        res = readResult( u"Choix: " )
        if res == "Q":
          run = False
          break
        elif res == "C":
          printStdOut( u"Continue à chercher" )
        else:
          printStdOut( u"Réponse invalide" )
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
for r, pos in ratio:
  printStdOut( posToString( pos, chars ) + " " + str( r ) )
  