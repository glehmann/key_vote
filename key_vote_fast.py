#!/usr/bin/python
# -*- coding: utf-8 -*-

# Définition d'une carte d'accessibilité par duel de touches
# Copyright (C) 2007 Damien Thébault <damien.thebault@laposte.net>

# Merci à Gaëtan Lehmann pour l'idée originale et pour quelques bouts de code
# Merci à Daniel Delay pour l'idée de la dichotomie
# Merci à Julien Pauty qui a lui aussi travaillé sur le programme

#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#

from array import array
import random, sys, pickle, os
import key_vote_lib

if __name__ == '__main__':
  results = ([],[]) # tableau contenant les résultats (un pour chaque main)
  matchs = {} # matchs réellement effectués
  
  if len( sys.argv ) < 2 :
    sortedResultFile = 'result-sorted'
    key_vote_lib.printStdOut( u'Pas de fichier spécifié, utilisation du fichier ' + sortedResultFile )
  else:
    sortedResultFile = sys.argv[1]

  if len( sys.argv ) < 3 :
    resultFile = 'result'
    key_vote_lib.printStdOut( u'Pas de fichier spécifié, utilisation du fichier ' + resultFile )
  else:
    resultFile = sys.argv[2]

  # choix du clavier
  kbd = key_vote_lib.chooseKbd()
  
  if os.path.exists( sortedResultFile ):
    results = pickle.load( file( sortedResultFile ) )
  else:
    results = ([],[])
  
  if os.path.exists( resultFile ):
    matchs = pickle.load( file( resultFile ) )
  else:
    matchs = {}
  
  # ces touches sont sous les doigts et gagnent toujours
  win = [ key_vote_lib.stringToPos( c, kbd ) for c in kbd[0][11:15] + kbd[1][15:19] ]
  
  run = True
  
  nbOfChars = 1
  
  # tests (pour chaque main)
  for handID in (0,1):
    if not run:
      break
    # création d'un array contenant tous les caractères mélangés
    untested = []
    for c in kbd[handID]:
    	# à faire : gérer plusieurs charactères
      untested.append( key_vote_lib.stringToPos( c, kbd ) )
    
    # on enlève ce qu'on a déjà testé (sauvegardé)
    for keys in results[handID]:
      for key in keys:
        if key in untested:
          untested.remove(key)
        else:
          print '"' + key + u'" n\'est pas là!!!'
          print untested
          print results[handID]
    
    random.shuffle(untested)
    
    # tant qu'on a pas testé tous les caractères
    while len(untested) > 0 and run:
      c = untested[0] # on récupère le premier caractère correspondant
      C = key_vote_lib.posToString( c, kbd )
      
      if len(results[handID]) == 0: # si le tableau de résultats est vide
        results[handID].append((c,)) # on ajoute notre caractère
      else:
        min = 0 # minimum de la dichotomie
        max = len(results[handID])-1 # maximum de la dichotomie
        # après le choix, on aura 0 <= c <= len(...)
        
        while min <= max and run:
          middle = (max+min)/2 # on choisit le milieu (dichotomie)
          
          test = results[handID][middle][0] # on va tester c par rapport à ce caractère
          TEST = key_vote_lib.posToString( test, kbd )
          
          pair = ( c, test )
          
          if c in win and test in win: # touches gagnantes au même niveau
            res = None
            ires = 0
          elif c in win: # touches gagnantes gagnent contre toutes les autres touches
            res = None
            ires = 1
          elif test in win: # touches gagnantes gagnent contre les autres touches
            res = None
            ires = 2
          else:
            key_vote_lib.printKbdLayout(kbd, (C,TEST) )
            key_vote_lib.printStdOut( u"1: %s  2: %s   0: égalité   Q: quitter  (%i touches restantes sur cette main)" % ( C, TEST, len(untested) ) )
            res = key_vote_lib.readResult( 'vote: ', ['0', '1', '2', 'Q', C, TEST] )
            ires = key_vote_lib.zeroOneTwo( res )
          
          if res == 'Q':
            run = False
          
          if ires == 1 or res == C: # le caractère est meilleur que le milieu
            min = middle+1 # le minimum est maintenant après le milieu
            if max < min:
              results[handID].insert(middle+1, (c,)) # insertion avant le milieu
            matchs[pair] = 1
          elif ires == 2 or res == TEST: # le caractère est moins bon que le milieu
            max = middle-1 # le maximum est avant le milieu
            if max < min:
              results[handID].insert(middle, (c,)) # insertion après le milieu
            matchs[pair] = 2
          elif ires == 0: # les caractères sont aussi bons
            results[handID][middle] += (c,) # on ajoute au milieu
            max = min-1 # fin du test de ce caractère
            matchs[pair] = 0
        
        pickle.dump( matchs, file( resultFile, "w" ) )
        pickle.dump( results, file( sortedResultFile, "w" ) )
        
      untested.pop(0) # on supprime le caractère de l'array
    

  # génère les duels comme dans la version de base
  base_results = key_vote_lib.computeMachs( results )

  # affichage des résultats
  key_vote_lib.printStdOut()
  key_vote_lib.printStdOut( u'Vos votes :' )
  
  # calcul des matchs perdus/total pour chaque touche
  scores = key_vote_lib.computeScores( key_vote_lib.countLost( base_results ) )
  
  # affichage du résultat
  key_vote_lib.printKbdScores( scores )
  key_vote_lib.readResult( u'appuyez sur Entrée pour quitter' )
