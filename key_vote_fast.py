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
	sorted = ([],[]) # tableau contenant les résultats triés (un pour chaque main)
	scores = {} # tableau associatif des scores par touche
	matchs = {} # matchs réellement effectués
	
	if len( sys.argv ) == 1 :
		resultFile = 'result'
		key_vote_lib.printStdOut( u'Pas de fichier spécifié, utilisation du fichier ' + resultFile )
	else:
		resultFile = sys.argv[1]

	# choix du clavier
	kbd = key_vote_lib.chooseKbd()
	
	if os.path.exists( resultFile ):
		matchs = pickle.load( file( resultFile ) )
	else:
		matchs = {}
	
	# affichage des matchs à charger
	#for pair in matchs.keys():
		#k1 = key_vote_lib.posToString(pair[0], kbd)
		#k2 = key_vote_lib.posToString(pair[1], kbd)
		#print '(' + k1 + ',' + k2 + ') : ' + str(matchs[pair])
	
	# prise en compte des matchs déjà joué
	for pair in matchs.keys():
		k1 = key_vote_lib.posToString(pair[0], kbd)
		k2 = key_vote_lib.posToString(pair[1], kbd)
		if (k1 in kbd[0] and k2 in kbd[0]) or (k1 in kbd[1] and k2 in kbd[1]):
			if k1 in kbd[0]:
				handID = 0
			else:
				handID = 1
			
			for c in (k1,k2):
				# si on a déjà classé la touche, on passe à celle d'après
				already = False
				for keys in results[handID]:
					if c in keys:
						already = True
						break
				if already == True:
					break
				
				if len(results[handID]) == 0:
					results[handID].append((c,))
				else: # dichotomie, voir dans les tests pour l'algorithme
					min = 0
					max = len(results[handID])-1
					
					matchfound = True
					while min <= max and matchfound == True:
						middle = (max+min)/2
						
						test = results[handID][middle][0] # on va tester par rapport à ce caractère
						
						if c == test:
							break
						
						matchfound = False
						for pair in matchs.keys():
							if matchfound == True:
								print 'BIG WARNING'
							pair0 = key_vote_lib.posToString(pair[0], kbd)
							pair1 = key_vote_lib.posToString(pair[1], kbd)
							if pair0 == c and pair1 == test:
								if matchs[pair] == 0: # key == test
									min = max+1
									results[handID][middle] += (c,)
									matchfound = True
									break
								elif matchs[pair] == 1: # key > test
									min = middle+1
									if max < min:
										results[handID].insert(middle+1, (c,))
									matchfound = True
									break
								elif matchs[pair] == 2: # key < test
									max = middle-1
									if max < min:
										results[handID].insert(middle, (c,))
									matchfound = True
									break
							elif pair0 == test and pair1 == c:
								if matchs[pair] == 0: # key == test
									min = max+1
									results[handID][middle] += (c,)
									matchfound = True
									break
								elif matchs[pair] == 2: # key > test
									min = middle+1
									if max < min:
										results[handID].insert(middle+1, (c,))
									matchfound = True
									break
								elif matchs[pair] == 1: # key < test
									max = middle-1
									if max < min:
										results[handID].insert(middle, (c,))
									matchfound = True
									break
						
						#if matchfound == False:
							#key_vote_lib.printStdOut( '"' + c + u'" : match avec "' + test + u'" non trouvé. pas d\'insertion' )
						
		else:
			key_vote_lib.printStdOut( k1 + ' et ' + k2 + ' sont sur des mains différentes!' )
	
	
	# ces touches sont sous les doigts et gagnent toujours
	win = kbd[0][11:15] + kbd[1][15:19]
	
	run = True
	
	# tests (pour chaque main)
	for handID in (0,1):
		if not run:
			break
		# création d'un array contenant tous les caractères mélangés
		untested = array('u')
		untested.fromunicode(kbd[handID])
		
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
			
			if len(results[handID]) == 0: # si le tableau de résultats est vide
				results[handID].append((c,)) # on ajoute notre caractère
			else:
				min = 0 # minimum de la dichotomie
				max = len(results[handID])-1 # maximum de la dichotomie
				# après le choix, on aura 0 <= c <= len(...)
				
				while min <= max and run:
					middle = (max+min)/2 # on choisit le milieu (dichotomie)
					
					test = results[handID][middle][0] # on va tester c par rapport à ce caractère
					
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
						key_vote_lib.printKbdLayout(kbd, (c,test) )
						key_vote_lib.printStdOut( u"1: %s  2: %s   0: égalité   Q: quitter  (%i touches restantes sur cette main)" % ( c, test, len(untested) ) )
						res = key_vote_lib.readResult( 'vote: ', ['0', '1', '2', 'Q', c, test] )
						ires = key_vote_lib.zeroOneTwo( res )
					
					if res == 'Q':
						run = False
					
					key = (key_vote_lib.stringToPos(c, kbd),key_vote_lib.stringToPos(test, kbd))
					
					if ires == 1 or res == c: # le caractère est meilleur que le milieu
						min = middle+1 # le minimum est maintenant après le milieu
						if max < min:
							results[handID].insert(middle+1, (c,)) # insertion avant le milieu
						matchs[key] = 1
					elif ires == 2 or res == test: # le caractère est moins bon que le milieu
						max = middle-1 # le maximum est avant le milieu
						if max < min:
							results[handID].insert(middle, (c,)) # insertion après le milieu
						matchs[key] = 2
					elif ires == 0: # les caractères sont aussi bons
						results[handID][middle] += (c,) # on ajoute au milieu
						max = min-1 # fin du test de ce caractère
						matchs[key] = 0
				
				pickle.dump( matchs, file( resultFile, "w" ) )
				
			untested.pop(0) # on supprime le caractère de l'array
		
		for (i,result) in enumerate(results[handID]): # pour chaque ensemble de touches
			for char in result: # pour chaque touche
				if len(results[handID])-1 > 0:
					score = i/(len(results[handID])-1.) # calcul du le score entre 0 et 1
				else:
					score = 0
				sorted[handID].append( (score, char) ) # on ajoute le score à la liste triée
				scores[char] = score # on associe le score à la touche
	
	# affichage des résultats
	
	key_vote_lib.printStdOut()
	key_vote_lib.printStdOut( u'Vos votes :' )
	
	# calcul des matchs perdus/total pour chaque touche (comme dans key_vote.py)
	
	matchs = {}
	for handID in (0,1):
		for k1 in kbd[handID]:
			for k2 in kbd[handID]:
				if k1 != k2 and k1 in scores.keys() and k2 in scores.keys():
					(lost1, total1) = matchs.get(k1, (0,0))
					(lost2, total2) = matchs.get(k2, (0,0))
					total1 = total1+1
					total2 = total2+1
					if scores[k1] > scores[k2]:
						lost2 = lost2+1
					elif scores[k1] < scores[k2]:
						lost1 = lost1+1
					matchs[k1] = (lost1,total1)
					matchs[k2] = (lost2,total2)
	
	# calcul du score pour chaque touche
	
	finalScores = {}
	for char in matchs.keys():
		(lost,total) = matchs[char]
		finalScores[char] = float( total - lost ) / total
	
	# affichage du résultat
	
	key_vote_lib.printKbdScores(kbd, finalScores)
	key_vote_lib.readResult( u'appuyez sur Entrée pour quitter' )
