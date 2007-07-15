#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys, pickle, os
import key_vote_lib

if sys.version < '2.4' :
  from key_vote_lib import sorted

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

if __name__ == '__main__':
  
  if len( sys.argv ) == 1 :
    resultFile = 'result'
    key_vote_lib.printStdOut( u'Pas de fichier spécifié, utilisation du fichier ' + resultFile )
  else:
    resultFile = sys.argv[1]
  
  hands = key_vote_lib.chooseKbd()
  leftHand,rightHand = hands
  
  nbOfChars = 1
  
  nbOfVotes = 10
  
  if os.path.exists( resultFile ):
    results = pickle.load( file( resultFile ) )
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
      
      s1 = key_vote_lib.posToString( pair[0], hands )
      s2 = key_vote_lib.posToString( pair[1], hands )
      
      if pair not in results:
        nbOfSearch = 0
        if candidate1 in homePos and candidate2 not in homePos :
          results[ pair ] = 1
          key_vote_lib.printStdOut( 'Vote automatique: ' + key_vote_lib.posToString( candidate1, hands ) + ' > ' + key_vote_lib.posToString( candidate2, hands ) )
        elif candidate2 in homePos and candidate1 not in homePos :
          results[ pair ] = 2
          key_vote_lib.printStdOut( 'Vote automatique: ' + key_vote_lib.posToString( candidate1, hands ) + ' < ' + key_vote_lib.posToString( candidate2, hands ) )
        elif candidate2 in homePos and candidate1 in homePos :
          results[ pair ] = 0
          key_vote_lib.printStdOut( 'Vote automatique: ' + key_vote_lib.posToString( candidate1, hands ) + ' = ' + key_vote_lib.posToString( candidate2, hands ) )
        else: # not automatic vote
          key_vote_lib.printKbdLayout(hands, (s1,s2) )
          
          key_vote_lib.printStdOut( u"%(s1)s ou 1->  %(s1)s     %(s2)s ou 2->  %(s2)s     0->  égalité     Q->  quitter     A->  annuler un duel" % {"s1": s1, "s2": s2 } )
          key_vote_lib.printStdOut( u"       %i duels réalisés / 556 possibles" % len( results ) )
          res = key_vote_lib.readResult( 'vote: ', ['Q', '0', '1', '2', s1, s2, 'A'] )
          ires = key_vote_lib.zeroOneTwo( res )
          
          if res == 'Q': # Q
            run = False
            break
          elif ires!=None: # 0, 1, 2
            results[ pair ] = ires
          elif res==s1:
            results[ pair ] = 1
          elif res==s2:
            results[ pair ] = 2
          elif res == 'A':
            key_vote_lib.cancelDuel(results, hands)
          else:
            key_vote_lib.printStdOut( u'Erreur dans le programme !' )
          
          pickle.dump( results, file( resultFile, "w" ) )
          key_vote_lib.printStdOut()
      else:
        nbOfSearch += 1
        if nbOfSearch > 10000:
          
          key_vote_lib.printStdOut( u"Il semble difficile de trouver de nouvelles combinaisons." )
          key_vote_lib.printStdOut( u"C -> continuer à chercher   Q -> sauver et quitter     A->  annuler un duel" )
          key_vote_lib.printStdOut( u"       %i duels réalisés" % len( results ) )
          res = readResult( u'Choix: ', ['C', 'Q', 'A'] )
          
          if res == "Q":
            run = False
            break
          elif res == "C":
            nbOfSearch = 0
            key_vote_lib.printStdOut( u'Continue à chercher' )
          elif res == "A":
            key_vote_lib.cancelDuel(results, hands)
          else:
            key_vote_lib.printStdOut( u'Erreur dans le programme !' )
          
          key_vote_lib.printStdOut()
  
  pickle.dump( results, file( resultFile, "w" ) )
  
  # affichage des résultats
  
  key_vote_lib.printStdOut()
  # key_vote_lib.printStdOut( u'Vos votes :' )
  
  # calcul des matchs perdus/total pour chaque touche
  scores = key_vote_lib.computeScores( key_vote_lib.countLost( results ) )
  
  # affichage du résultat
  key_vote_lib.printScores( scores, hands )
  key_vote_lib.printKbdScores( scores )
  key_vote_lib.readResult( u'appuyez sur Entrée pour quitter' )
