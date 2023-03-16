from random import randint, shuffle, choice

import pprint
pp = pprint.PrettyPrinter(indent=2)

class MazeCustom:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height, width, empty = False):
        """
        Constructeur d'un labyrinthe de height cellules de haut 
        et de width cellules de large 
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range (width)}

        if empty:
            for i in range(height):
                for j in range(width):
                    if i > 0:
                        self.neighbors[(i,j)].add((i-1,j))
                    if i < height-1:
                        self.neighbors[(i,j)].add((i+1,j))
                    if j > 0:
                        self.neighbors[(i,j)].add((i,j-1))
                    if j < width-1:
                        self.neighbors[(i,j)].add((i,j+1))


    def info(self):
        """
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        # What is the english version of this description?
        txt = f"{self.height} x {self.width}\n"
        txt += str(self.neighbors)
        return txt

    def __str__(self):
        """
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt
    
    def add_wall(self, c1, c2):
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2) # on le retire
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire

    def remove_wall(self, c1, c2):
        # Conditions bien-sûr réutilisées depuis l'énoncé pour quelque chose de propre et de lisible 
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de la suppression d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Suppression du mur
        if c2 not in self.neighbors[c1]: # Si c2 n'est pas dans les voisines de c1
            self.neighbors[c1].add(c2)   # on l'ajoute
        if c1 not in self.neighbors[c2]: # Si c1 n'est pas dans les voisines de c2
            self.neighbors[c2].add(c1)   # on l'ajoute

    def get_walls(self):
        """
        Retourne la liste des murs du labyrinthe
        arguments : 
            self
        retour : 
            list
        """
        walls = []
        for i in range(self.height):
            for j in range(self.width):
                vois=[]
                if j!=self.width-1:
                    vois.append((i,j+1))
                if i!=self.height-1:
                    vois.append((i+1,j))
                for k in vois:
                    if k not in self.neighbors[i,j]:
                        walls.append(((i,j),k))
        return walls
    
    def fill(self):
        """
        Permet de remplir le labyrinthe
        arguments : 
            self
        retour :
            None
        """
        self.neighbors = {(i,j): set() for i in range(self.height) for j in range (self.width)}

    def empty(self):
        """
        Vide le labyrinthe en retirant tous les murs du labyrinthe
        arguments : 
            self
        retour : 
            list
        """
        for i in range(self.height):
            for j in range(self.width):
                if i > 0:
                    self.neighbors[(i,j)].add((i-1,j))
                if i < self.height-1:
                    self.neighbors[(i,j)].add((i+1,j))
                if j > 0:
                    self.neighbors[(i,j)].add((i,j-1))
                if j < self.width-1:
                    self.neighbors[(i,j)].add((i,j+1))
    
    def get_contiguous_cells(self, c):
        """
        Retourne la liste des cellules contigues à la cellule c
        arguments : 
            self, c
        retour : 
            list
        """
        vois=[] #liste des voisins
        if c[0]!=0: #si on est pas sur la première ligne
            vois.append((c[0]-1,c[1])) #on ajoute le voisin du dessus
        if c[1]!=0: #si on est pas sur la première colonne
            vois.append((c[0],c[1]-1)) #on ajoute le voisin de gauche
        if c[1]!=self.width-1: #si on est pas sur la dernière colonne
            vois.append((c[0],c[1]+1)) #on ajoute le voisin de droite
        if c[0]!=self.height-1: #si on est pas sur la dernière ligne
            vois.append((c[0]+1,c[1])) #on ajoute le voisin du dessous
        return vois
    
    """
    def get_reachable_cells(self, c):
        visite=[c]
        pile=[]
        for i in self.neighbors[c]:
            pile.append(i)
        while len(pile)!=0:
            visite.append(pile[0])
            for i in self.neighbors[pile[0]]:
                if i not in pile and i not in visite:
                    pile.append(i)
            pile.pop(0)
        visite.pop(0)
        return visite
    """
    def get_reachable_cells(self, c):
        """
        Permet de retourner les cellules atteigables (càd sans mur)
        arguments : 
            self, c
        retour : 
            list
        """
        atteignables=[]
        for i in self.neighbors[c]:
            atteignables.append(i)
        return atteignables
    
    @classmethod
    def gen_btree(cls, h, w):
        """
        Permet de génére un labyrinthe aléatoire avec l'algorithme de relation binaire qui est le suivant:
        - Initialisation : un labyrinthe plein (contenant tous les murs possibles)
        - Pour chaque cellule du labyinthe:
            - Supprimer aléatoirement le mur EST ou le mur SUD (s'il n'en possède qu'un, supprimer ce mur ; s'il n'en possède aucun des deux, ne rien faire)
        arguments : 
            cls, h, w
        retour : 
            Maze
        """
        laby=MazeCustom(h, w, empty = False)
        for i in range(laby.height):
            for j in range(laby.width):
                c=(i,j)
                if i==(laby.height-1) and j!=(laby.width-1):
                    laby.remove_wall(c,(c[0],c[1]+1))
                elif j==(laby.width-1) and i!=(laby.height-1):
                    laby.remove_wall(c,(c[0]+1,c[1]))
                elif i!=(laby.height-1) and j!=(laby.width-1):
                    aleatoire=randint(1,2)
                    if aleatoire==1:
                        laby.remove_wall(c,(c[0],c[1]+1))
                    else :
                        laby.remove_wall(c,(c[0]+1,c[1]))
        return laby


    @classmethod
    def gen_sidewinder(cls, h, w):
        """
        Fonction de génération d'un labyrinthe aléatoire selon l'algorithme de Sidewinder qui est le suivant:
        - On procède maintenant ligne par ligne, d'OUEST en EST, en choisissant aléatoirement de casser le mur EST d'une cellule.
        - Pour chaque séquence de celulles voisines (connectées) créées sur la ligne, on casse un mur SUD ou hasard d'une des cellules.
        arguments : 
            cls, h, w
        retour : 
            Maze
        """
        laby=MazeCustom(h, w, empty = False) # On crée un labyrinthe vide
        for i in range(laby.height): # Pour chaque ligne
            run=[] # On crée une liste vide pour stocker les sommets de la ligne
            for j in range(laby.width): # Pour chaque sommet de la ligne
                c=(i,j) # On récupère les coordonnées du sommet
                run.append(c) # On ajoute le sommet à la liste des sommets de la ligne
                if i==laby.height-1 and j!=laby.height-1: # Si on est sur la dernière ligne
                    laby.remove_wall(c,(c[0],c[1]+1)) # On supprime le mur de droite
                else: # Sinon
                    if j==(laby.width-1): # Si on est sur la dernière colonne
                        aleatoire=randint(0,len(run)-1) # On choisit un sommet au hasard dans la liste des sommets de la ligne
                        if i!=laby.height-1: # Si on n'est pas sur la dernière ligne
                            laby.remove_wall(run[aleatoire],(run[aleatoire][0]+1,run[aleatoire][1])) # On supprime le mur du bas du sommet choisi
                            run=[] # On vide la liste des sommets de la ligne
                    elif randint(1,2)==1: # Sinon, on choisit un sommet au hasard dans la liste des sommets de la ligne
                        aleatoire=randint(0,len(run)-1)  # On choisit un sommet au hasard dans la liste des sommets de la ligne
                        if i!=laby.height-1: # Si on n'est pas sur la dernière ligne
                            laby.remove_wall(run[aleatoire],(run[aleatoire][0]+1,run[aleatoire][1])) # On supprime le mur du bas du sommet choisi
                        run=[] # On vide la liste des sommets de la ligne
                    else :
                        laby.remove_wall(c,(c[0],c[1]+1)) # On supprime le mur de droite
        return laby
    
    @classmethod
    def gen_fusion(cls, h, w):
        """
        L’algorithme de fusion de chemins consiste à fusionner des chemins en évitant de créer des cycles. 
        Utilisation d'un système de labellisation.
        arguments : 
            cls, h, w
        retour : 
            Maze
        """
        laby=MazeCustom(h, w, empty = False)
        # On crée un tableau de taille h*w qui contient les numéros des composantes ouvertes
        labels = {(i,j): (i,j) for i in range(laby.height) for j in range(laby.width)} # On crée le dictionnaire des labels
        walls = laby.get_walls() # On récupère la liste des murs
        shuffle(walls) # On mélange la liste des murs
        for (c1,c2) in walls: # Pour chaque mur
            if labels[c1] != labels[c2]: # Si les deux cellules ne sont pas dans la même composante ouverte
                laby.remove_wall(c1,c2) # On enlève le mur
                label2 = labels[c2] # On récupère les labels des deux cellules
                for c in labels: # Pour chaque cellule
                    if labels[c] == label2: # Si la cellule est dans la composante ouverte de la cellule 2
                        labels[c] = labels[c1] # On fusionne les deux composantes ouvertes
        return laby
    
    @classmethod
    def gen_exploration(cls, h, w):
        """
        L’algorithme d’exploration consiste à explorer aléatoirement le labyrinthe, à la manière d'un parcours en profondeur, en cassant les murs au fur et à mesure.
        arguments : 
            cls, h, w
        retour : 
            Maze
        """
        laby=MazeCustom(h, w, empty = False)
        # On crée un tableau de taille h*w qui contient les numéros des composantes ouvertes
        pile = [] # On crée la pile
        visited = [] # On crée la liste des cellules visitées
        c = (randint(0,h-1),randint(0,w-1)) # On choisit une cellule au hasard
        visited.append(c) # On ajoute la cellule à la liste des cellules visitées
        pile.append(c) # On ajoute la cellule à la pile

        while len(pile) != 0: # Tant que la pile n’est pas vide
            c = pile[0] # On prend la cellule en haut de la pile
            pile.pop(0) # On prend la cellule en haut de la pile et on l’enlève
            listeTemp = [] # On crée une liste temporaire
            for i in laby.get_contiguous_cells(c):
                if i not in visited:
                    listeTemp.append(i) # On ajoute les cellules contigües qui n’ont pas encore été visitées à la liste temporaire
            if len(listeTemp) != 0: # Si la liste temporaire n’est pas vide
                pile.insert(0,c) # On remet la cellule en haut de la pile
                c2 = choice(listeTemp) # On choisit au hasard une cellule de la liste temporaire
                laby.remove_wall(c, c2) # On enlève le mur entre la cellule qui vient d’être dépilée et la cellule qui vient d’être choisie
                visited.append(c2) # On ajoute la cellule qui vient d’être choisie à la liste des cellules visitées
                pile.insert(0,c2) # On ajoute la cellule qui vient d’être choisie à la pile
        return laby

    @classmethod
    def gen_wilson(cls, h, w):
        """
        Choisir une cellule au hasard sur la grille et la marquer
        Tant qu’il reste des cellules non marquées :
        Choisir une cellule de départ au hasard, parmi les cellules non marquées
        Effectuer une marche aléatoire jusqu’à ce qu’une cellule marquée soit atteinte (en cas de boucle, si la tête du snake se mord la queue, « couper » la boucle formée [autrement dit, supprimer toutes étapes depuis le précédent passage])
        Marquer chaque cellule du chemin, et casser tous les murs rencontrés, jusqu’à la cellule marquée.

        arguments : 
            cls, h, w
        retour : 
            Maze
        """
        laby = MazeCustom(h, w, empty = False)
        marquees = [] # Liste des cellules marquées
        c = (randint(0,h-1), randint(0,w-1)) # On choisit une cellule au hasard
        marquees.append(c) # On ajoute la cellule choisit au hasard à la liste des cellules marquées
        while len(marquees) != h*w: # Tant qu’il reste des cellules non marquées
            while c in marquees: # Tant que la cellule choisit au hasard est marquée
                c = (randint(0,h-1), randint(0,w-1)) # On choisit une cellule au hasard
            chemin = [] # On crée une liste vide qui contiendra le chemin
            chemin.append(c) # On ajoute la cellule choisit au hasard à la liste du chemin
            while c not in marquees: # Tant que la cellule choisit au hasard n’est pas marquée
                c = choice(laby.get_contiguous_cells(c)) # On choisit au hasard une cellule contigüe
                if c in chemin: # Si la cellule choisit au hasard est déjà dans le chemin
                    #chemin = chemin[:chemin.index(c)+1] # On coupe le chemin à la cellule choisit au hasard
                    while chemin[len(chemin)-1]!=c:
                        chemin.pop()
                else:
                    chemin.append(c)
            for i in range(len(chemin)-1): # Pour chaque cellule du chemin
                laby.remove_wall(chemin[i], chemin[i+1]) # On enlève le mur entre la cellule et la cellule suivante
            chemin.pop()
            marquees += chemin # On ajoute le chemin à la liste des cellules marquées
        return laby
    
    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour :
            String
        """
        if content is None:
            content = {(i,j):' ' for i in range(self.height) for j in range(self.width)}
        else:
            content = content | {(i, j): ' ' for i in range(
                self.height) for j in range(self.width) if (i,j) not in content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += " "+content[(0,j)]+" ┃" if (0,j+1) not in self.neighbors[(0,j)] else " "+content[(0,j)]+"  "
        txt += " "+content[(0,self.width-1)]+" ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " "+content[(i+1,j)]+" ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else " "+content[(i+1,j)]+"  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt
    
    def solve_dfs(self, start, stop):
        """"
        L’algorithme le plus évident pour résoudre un problème de labyrinthe, 
        consiste à adapter le parcours « en profondeur d’abord » de l’arborescence associée au labyrinthe
        arguments : 
            self, start, stop
        retour : 
            liste
        """
        pile = [start] # On crée une liste nommée pile et on  y met start 
        visited = [] # On créé une liste des cellules marquées
        predecesseur = {start: start} # On crée un dictionnaire qui contient le prédécesseur de départ

        fini=False
        while not fini:
            c = pile.pop(0) # On enlève la première cellule
            if c == stop: # Si la cellule est stop
                fini=True # On arrête la boucle
            else: # Sinon
                visited.append(c) # On ajoute la cellule
                for i in self.get_reachable_cells(c): # Pour chaque cellule contigüe
                    if i not in visited: # Si la cellule n’est pas marquée
                        pile.insert(0,i) # On l’ajoute au début de la liste
                        predecesseur[i]=c
        chemin = [stop] # On crée une liste qui contient stop
        c = stop # On met stop dans c
        while c != start: # Tant que c n’est pas start
            c = predecesseur[c] # On met le prédécesseur de c dans c
            chemin.insert(0,c) # On ajoute c au début de la liste chemin
        return chemin
    
    def solve_bfs(self, start, stop):
        """"
        Nous le résolvons maintenant en largeur, c'est à dire que l'on crée maintenant une file qui implique d'ajouter la celulle
        à la fin de la liste et non au début comme avant.
        arguments : 
            self, start, stop
        retour : 
            liste
        """
        pile = [start] # On crée une liste nommée pile et on  y met start 
        visited = [] # On créé une liste des cellules marquées
        predecesseur = {start: start} # On crée un dictionnaire qui contient le prédécesseur de départ

        fini=False
        while not fini:
            c = pile.pop(0) # On enlève la première cellule
            if c == stop: # Si la cellule est stop
                fini=True # On arrête la boucle
            else: # Sinon
                visited.append(c) # On ajoute la cellule
                for i in self.get_reachable_cells(c): # Pour chaque cellule contigüe
                    if i not in visited: # Si la cellule n’est pas marquée
                        pile.append(i) # On l’ajoute à la fin de la liste
                        predecesseur[i]=c
        chemin = [stop] # On crée une liste qui contient stop
        c = stop # On met stop dans c
        while c != start: # Tant que c n’est pas start
            c = predecesseur[c] # On met le prédécesseur de c dans c
            chemin.insert(0,c) # On ajoute c au début de la liste chemin
        return chemin
  
    def solve_rhr(self, start, stop):
        """
        L’algorithme, bien connu, dit « de la main droite » peut-être vu comme une recherche « en profondeur d’abord » mais sans vision globale du labyrinthe. 
        C’est la situation dans laquelle serait un individu qu’on abandonnerait dans un labyrinthe et qui devrait trouver la sortie.
        arguments :
            self, start, stop
        retour :
            liste du chemin
        """
        c = start #On initilialise la case où l'on se trouve à la case de départ
        suivante = choice(self.get_reachable_cells(c))#On choisit une direction où aller
        chemin = [start] #Initialisation du chemin avec la case de départ et celle où on a choisi d'aller
        ancienne = c #On enregistre la case où l'on était
        c = suivante #On se déplace à la case souhaitée
        suivante=(c[0]+c[0]-ancienne[0],c[1]+c[1]-ancienne[1])#On calcule la case en ligne droite
        while c != stop:
            #On vérifie si la case où l'on est n'est pas déjà dans la liste(donc si l'on a pas fait demi-tour)
            if c in chemin and ancienne in chemin:
                chemin.remove(ancienne)
            else :
                chemin.append(c)
            vertHor=-abs(suivante[0]-c[0])+abs(suivante[1]-c[1])#Variable qui détecte si la trajectoire entre c et suivante est horizontale ou verticale (1:horizontale, -1: verticale)
            #S'il y a une intersection à droite on la prend
            if (c[0]-vertHor*(c[1]-suivante[1]),c[1]-vertHor*(c[0]-suivante[0])) in self.get_reachable_cells(c) and ancienne!=(c[0]-vertHor*(c[1]-suivante[1]),c[1]-vertHor*(c[0]-suivante[0])):
                ancienne=c
                c=(c[0]-vertHor*(c[1]-suivante[1]),c[1]-vertHor*(c[0]-suivante[0]))
            #Sinon s'il n'y a pas de mur tout droit on y va
            elif suivante in self.get_reachable_cells(c):
                ancienne = c #On enregistre la case où l'on était
                c = suivante #On se déplace à la case souhaitée
            #Sinon si on peut tourner à gauche on le fait
            elif (c[0]+vertHor*(c[1]-suivante[1]),c[1]+vertHor*(c[0]-suivante[0])) in self.get_reachable_cells(c) and ancienne!=(c[0]+vertHor*(c[1]-suivante[1]),c[1]+vertHor*(c[0]-suivante[0])):
                ancienne=c#On enregistre la case où l'on était
                c=(c[0]+vertHor*(c[1]-suivante[1]),c[1]+vertHor*(c[0]-suivante[0]))#On se déplace à la case de gauche
            #Sinon on fait demi-tour
            else :
                temp=ancienne#On retient l'ancienne case
                ancienne=c#On définit l'ancienne case à la case actuelle
                c=temp#On retourne à la case précédente
            suivante=(c[0]+c[0]-ancienne[0],c[1]+c[1]-ancienne[1])#On calcule la case en ligne droite
            #Si la case suivante n'est pas dans le labyrinthe:
            if suivante not in self.get_contiguous_cells(c):
                vertHor=-abs(suivante[0]-c[0])+abs(suivante[1]-c[1])
                if (c[0]-vertHor*(c[1]-suivante[1]),c[1]-vertHor*(c[0]-suivante[0])) in self.get_reachable_cells(c):#On tourne à droite si possible
                    suivante=(c[0]-vertHor*(c[1]-suivante[1]),c[1]-vertHor*(c[0]-suivante[0]))
                elif (c[0]+vertHor*(c[1]-suivante[1]),c[1]+vertHor*(c[0]-suivante[0])) in self.get_reachable_cells(c):#Sinon tourne à gauche si l'on peut
                    suivante=(c[0]+vertHor*(c[1]-suivante[1]),c[1]+vertHor*(c[0]-suivante[0]))
                else  : #Sinon on fait demi-tour
                    suivante=ancienne
        chemin.append(stop)
        return chemin

    def distance_geo(self,c1,c2):
        return len(self.solve_dfs(c1,c2))-1
        
    def distance_man(self,c1,c2):
        return abs(c1[0]-c2[0])+abs(c1[1]-c2[1])

# width = 10
# height = 20
# maze = Maze.gen_exploration(width, height)

def new_str_method(self):
    """
    Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
    Retour:
            chaîne (str) : chaîne de caractères représentant le labyrinthe
    """
    txt = ""
    # Première ligne
    txt += "#"
    for j in range(self.width-1):
        txt += "##"
    txt += "##\n"
    txt += "#"
    for j in range(self.width-1):
        if (0,j+1) not in self.neighbors[(0,j)]:
            txt += " #"
        else:
            txt += "  " ## 2 chars or 3 chars?
    txt += " #\n"
    # Lignes normales
    for i in range(self.height-1):
        txt += "#"
        for j in range(self.width-1):
            if (i+1,j) not in self.neighbors[(i,j)]:
                txt += "##" 
            else:
                txt += " #"
        if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)]:
            txt += "##\n"
        else:
            txt += " #\n"
        txt += "#"
        for j in range(self.width):
            if (i+1,j+1) not in self.neighbors[(i+1,j)]:
                txt += " #"
            else:
                txt += "  "
        txt += "\n"
    # Bas du tableau
    txt += "#"
    for i in range(self.width-1):
        txt += "##"
    txt += "##\n"

    return txt
# data = new_str_method(maze)
# datagrid = data.splitlines()

# 0 = empty 1 = wall
# grid = [[0]*len(datagrid) for _ in range(len(datagrid[0]))]

def convert_to_grid(datagrid:str, grid):
    for y, line in enumerate(datagrid):
        print(y, datagrid[y])
        for x, char in enumerate(datagrid[y]):
            iswall = 1 if char == "#" else 0
            print(x, y, char)
            grid[x][y] = iswall

    return grid
# grid = convert_to_grid(data, grid)
# pp.pprint(grid)

def generate_map(width, height):
    maze = MazeCustom.gen_exploration(width, height)
    datagrid = new_str_method(maze).splitlines()
    grid = [[0]*len(datagrid) for _ in range(len(datagrid[0]))]
    grid = convert_to_grid(datagrid, grid)
    return grid, maze.neighbors