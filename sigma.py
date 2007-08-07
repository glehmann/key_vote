#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, pickle, key_vote_lib, math

hands = key_vote_lib.chooseKbd()

scores = {}
ratios = []

for fName in sys.argv[1:] :
  f = file( fName )
  results = pickle.load( f )
  
  if isinstance( results, tuple ):
    results = key_vote_lib.computeMachs( results )
  
  key_vote_lib.countLost( results, scores )
  
  # for the individual ratios
  ratios.append( key_vote_lib.computeScores( key_vote_lib.countLost( results ) ) )
  
  f.close()
  
ratio = key_vote_lib.computeScores( scores )

sigma = {}
total = 0
for k in ratio.keys() :
  sum2 = 0
  for r in ratios :
    sum2 += math.pow( r[k] - ratio[k], 2 )
  s = math.sqrt( sum2 / len(ratios) )
  sigma[k] = s
  total += s

key_vote_lib.printScores( sigma, hands )
key_vote_lib.printStdOut()
key_vote_lib.printStdOut( u"Différence totale: " + str( total ) )
key_vote_lib.printKbdScores( sigma )
