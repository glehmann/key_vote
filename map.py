#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, pickle, key_vote_lib

scores = {}
nbOfVotes = 0

for fName in sys.argv[1:] :
  f = file( fName )
  results = pickle.load( f )
  
  if isinstance( results, tuple ):
    results = key_vote_lib.computeMachs( results )
  
  key_vote_lib.countLost( results, scores )
  nbOfVotes += len( results )
  
  f.close()
  
print nbOfVotes, "votes."
ratio = key_vote_lib.computeScores( scores )
key_vote_lib.printKbdScores( ratio )
