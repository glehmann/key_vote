#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, pickle, key_vote_lib

hands = key_vote_lib.chooseKbd()

scores = {}
nbOfVotes = 0

for fName in sys.argv[2:] :
  f = file( fName )
  results = pickle.load( f )
  
  if isinstance( results, tuple ):
    results = key_vote_lib.computeMachs( results )
  
  key_vote_lib.countLost( results, scores )
  nbOfVotes += len( results )
  
  f.close()
  
ratio = key_vote_lib.computeScores( scores )

# load the results to compare to the mean
singleResults = pickle.load( file( sys.argv[1] ) )
if isinstance( singleResults, tuple ):
  singleResults = key_vote_lib.computeMachs( singleResults )
singleScores = key_vote_lib.countLost( singleResults )
singleRatio = key_vote_lib.computeScores( singleScores )

# now, for the all the scores, compute the diff to the mean
singleDiff = {}
total = 0
for k, v in singleRatio.iteritems() :
  diff = abs( v - ratio[k] )
  singleDiff[k] = diff
  total += diff

key_vote_lib.printScores( singleDiff, hands )
key_vote_lib.printStdOut()
key_vote_lib.printStdOut( u"Différence totale: " + str( total ) )
key_vote_lib.printKbdScores( singleDiff )
