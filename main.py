#==================================================================#

# on importe les modules

# module principal de pygame
import pygame as py
# module python pour la musique 
from pygame import mixer
# module os qui gère pour aller regarder les fichiers
import os
# module random pour rajouter de l'aléatoire
import random
# module csv pour gérer les maps
import csv
# fichier externe qui gère les boutons en jeu comme start, restart etc...
import bouton

#==================================================================#

# Parametres principaux de notre fenetre

# on initialise mixer pour la musique/les sons en jeu 
mixer.init()
# on initialise pygame pour l'ensemble de la fenetre
py.init()
# on definit une horloge de temps pour les images en jeu
clock = py.time.Clock()
# 60 images par seconde
FPS = 60


#==================================================================#

# creer la fenetre avec les differentes caracteristiques

#largeur de la fenetre à 800
screen_width = 800
# hauteur de la fenetre ayant pour valeur 80% de la largeur de la fenetre
screen_height = int(screen_width * 0.8)
# on met en place la fenetre avec sa largeur et hauteur
screen = py.display.set_mode((screen_width, screen_height), py.RESIZABLE)
# on donne un nom à cette fenetre
py.display.set_caption("Projet jeu 25 Mai")
# on load et met en place l'icone de la fenetre
icone = py.image.load('Images/Icon/icon.png').convert_alpha()
py.display.set_icon(icone)



#==================================================================#

# variable utiles


# couleur du fond pour eviter des bugs avec les images
BG = (44,154,208)
# code couleur du rouge
rouge = (255, 0, 0)
# code couleur du blanc
blanc = (255, 255, 255)
# code couleur du vert
vert = (0, 255, 0)
# code couleur du noir
noir = (0, 0, 0)
# code couleur du fond de mort
couleur_fond = (27, 30, 44)
# variable correspondant à la gravité
gravite = 0.75
# nombre d'images dans notre dossier de textures
type_tile = 40
# niveau actuel
niveau = 0
# nombre maximal de niveau 
niveau_max = 1


# Les variables lignes et colonnes sont modifiables mais n'ont pas d'utilité si le fichier csv
# n'a pas le nombre de lignes/colonnes correspondant, cela va juste creer du vide

# lignes en jeu ayant un rapport avec les tiles/blocs
lignes = 16
# nombre de colonnes pour definir une limite à la map
colonnes = 150

# taille des blocs à 40
taille_tile = screen_height // lignes


# variable d'action du joueur

# deplacement gauche definit sur False ce qui veut dire que le personnage ne se déplace pas vers la gauche
deplacement_gauche = False
# deplacement droite definit sur False ce qui veut dire que le personnage ne se déplace pas vers la droite
deplacement_droite = False
# on definit la liste d'animation qui est disponible dans le fichier d'images correspondant au nom
# liste des monstres disponible dans le jeu
liste_monstre = ["yellow", "bear", "red", "tiny", "ooze", "slime"]
# liste de type d'animations disponibles pour le joueur
liste_anim_joueur = ["idle", "walk", "death", "jump", "throw"]
# liste de type d'animations disponibles pour les monstres 
liste_anim_monstre = ["idle", "walk", "death"]
# on definit si le joueur est en train de tire
tir = False
# on definit si le joueur est en train de tirer un projectile
projectile = False
lancer_projectile = False

# on definit la limite de scroll c'est a dire le nombre de pixel à la limite de la map où la caméra va commencer à se deplacer
distance_scroll = 200
# variable du scroll qui va deplacer tout les elements de la map
screen_scroll_x = 0
# variable du scroll qui va deplacer le background
background_scroll = 0

# on definit si la partie à commencer
debut_partie = False
# on definit si l'intro à commencer
debut_intro = False

# definir la police (ca marche pas...)
police = py.font.SysFont('Planes_ValMore.ttf', 30)


#==================================================================#

# on definit si le bruit des oiseaux et du vent est présent ou non
oiseaux = True
vent = True

# on importe la musique de fond
py.mixer.music.load('sons/musique_fond.mp3')
# on definit le volume à 0.2 de sa valeur initiale
py.mixer.music.set_volume(0.2)
# on lance la musique
py.mixer.music.play(-1, 0.0, 5000)

# on importe les sons d'oiseaux
oiseaux_son = py.mixer.Sound('sons/oiseaux.mp3')
# on definit le volume à 0.2 de sa valeur initiale
oiseaux_son.set_volume(0.2)
# on importe le bruit de vent
vent_son = py.mixer.Sound('sons/vent.mp3')
# on definit le volume à 0.5 de sa valeur initiale
vent_son.set_volume(0.5)
# on importe le bruit de l'explosion
explosion_son = py.mixer.Sound('sons/explosion.mp3')
# on definit le volume à 0.5 de sa valeur initiale
explosion_son.set_volume(0.5)
# si la variable oiseaux est sur True
if oiseaux == True:
    # on lance les bruits d'oiseaux
    oiseaux_son.play(-1, 0, 5000)
# si la variable vent est sur True
if vent == True:
    # on lance le bruit du vent
    vent_son.play(-1, 0, 5000)



# on importe les images

# images de boutons

# bouton start
start = py.image.load('Images/boutons/Lancer.png').convert_alpha()

# bouton restart
restart = py.image.load('Images/boutons/Relancer.png').convert_alpha()


# image du background
background_image = py.image.load('Images/background/background_large.png').convert_alpha()


# stocker les blocs dans une liste
# liste d'image des blocs
image_liste = []
# boucle qui va charger les images par rapport au nombre d'images qui a été spécifié dans la variable type_tile
for x in range(type_tile):
    # on charge l'image dans le dossier avec le nombre qui correspond à x
    image = py.image.load(f'Images/textures/{x}.png')
    # on change le scale en fonction de la taille des blocs
    image = py.transform.scale(image, (taille_tile, taille_tile))
    # et on ajoute l'image dans la liste
    image_liste.append(image)



# on charge toutes les images spécifiques et on change leur scale

# on charge l'image de la pierre 
pierre_image = py.image.load('Images/rock/rock1.png').convert_alpha()
# on change son scale
pierre_image = py.transform.scale(pierre_image, (int(pierre_image.get_width() * 1.5), int(pierre_image.get_height() * 1.5)))


# on charge l'image du projectile
pierre_projectile_image = py.image.load('Images/rock/0.png').convert_alpha()
# on change son scale
pierre_projectile_image = py.transform.scale(pierre_projectile_image, (int(pierre_projectile_image.get_width() * 0.9), int(pierre_projectile_image.get_height() * 0.9)))


# on charge l'image de la boite qui donne des points de vie 
boite_vie = py.image.load('Images/boxes/Box6.png').convert_alpha()
# on change son scale
boite_vie = py.transform.scale(boite_vie, (int(boite_vie.get_width() * 1.5), int(boite_vie.get_height() * 1.5)))


# on charge l'image de la boite qui donne des munitions (pierres)
boite_muni = py.image.load('Images/boxes/Box2.png').convert_alpha()
# on change son scale
boite_muni = py.transform.scale(boite_muni, (int(boite_muni.get_width() * 1.5), int(boite_muni.get_height() * 1.5)))


# on charge l'image de la boite qui donne des projectiles
boite_projectile = py.image.load('Images/boxes/Barrel1.png').convert_alpha()
# on change son scale
boite_projectile = py.transform.scale(boite_projectile, (int(boite_projectile.get_width() * 1.5), int(boite_projectile.get_height() * 1.5)))

# on importe l'image du coeur
coeur_image = py.image.load('Images/barre_vie/coeur.png').convert_alpha()
coeur_image = py.transform.scale(coeur_image, (int(coeur_image.get_width() * 0.07), int(coeur_image.get_height() * 0.07)))


# on met dans un dictionnaire à quoi correspond chaque boite 
boite_objet = {'Vie': boite_vie, 'Munition': boite_muni, 'Projectile': boite_projectile}




#==================================================================#

# fonction qui génère du texte qui prend en argument le texte, la police (fonctionne pas...), la couleur du texte, sa position en x et sa position en y 
def texte(texte, police, texte_couleur, x, y, scale):
    # le texte est en fait une image 
    image = police.render(texte, True, texte_couleur)
    image = py.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))

    # image que l'on va blit pour l'afficher
    screen.blit(image, (x, y))


# fonction qui va gerer le background
def background():
    # on fill/remplit l'ecran d'une couleur pour eviter certains bugs avec les sprites
    screen.fill(BG)
    # on recupere la largeur de sky dans la variable width
    width = background_image.get_width()
    # dans une boucle de 5
    for i in range(5):
        # on fait en sorte que le background se repete, vu que le jeu a un scrool si on ne fait pas de boucle
        # à une certaine distance le background va disparaitre et laisser place à la couleur de fond
        screen.blit(background_image, ((i * width) - background_scroll * 0.5, 0))
        


# fonction qui gère la reinitialisation du niveau
def reinitialiser_niveau():
    # on vide tout les groupes
    groupe_monstre.empty()
    groupe_pierre.empty()
    groupe_projectile.empty()
    groupe_explosion.empty()
    groupe_boite.empty()
    groupe_decoration.empty()
    groupe_piques.empty()
    groupe_sorties.empty()


    # Quand on va vouloir reinitialiser le niveau on va creer une liste qui va gerer les données du monde
    # Cette liste va etre remplie de blocs vide (-1 = bloc vide)

    # creer une liste de blocs vide
    #liste vide qui représente les données du monde
    donnee = []
    # boucle dans la range de ligne
    for ligne in range(lignes):
        # l est egal à - 1
        l = [-1] * colonnes
        # on l'append
        donnee.append(l)

    return donnee






#==================================================================#

# Class pour chaques entitées (definit en sprite de pygame)
class Entite(py.sprite.Sprite):
    # on creer la fonction init qui prend en parametres le nom de l'image, sa position en x et y, l'echelle donc le scale, la vitesse
    # le nombre de munition, le nombre de projectile et la liste d'animation lui correspondant
    def __init__(self, nom, x, y, scale, vitesse, munition, projectile, liste_anim):
        py.sprite.Sprite.__init__(self)
        # definir la liste d'animation
        self.liste_anim = liste_anim
        # variable du joueur vivant sur True
        self.vivant = True
        # le nom du perso par exemple player
        self.nom = nom
        # la vitesse du player qui doit etre set lors de sa creation
        self.vitesse = vitesse
        # definit le nombre de munitions
        self.munition = munition
        # definit le nombre de munition au debut de la partie
        self._munition_debut = munition
        # compte a rebours du tir/lancer de pierre
        self.tirer_temps = 0
        self.projectile = projectile
        # definir la vie
        self.point_de_vie = 100 # peut etre mis en parametre si on veut que les differentes entitées aient des pdv differents
        # le nombre de point de vie maximum
        self.pdv_max = self.point_de_vie
        # direction qui va servir à aller vers la gauche ou la droite selon le deplacement
        self.direction = 1
        # velocité correspondant au saut
        self.velocite_y = 0
        # on definit si le personnage est en l'air
        self.en_l_air = True
        # on definit si le personnage saute
        self.saut = False
        # on definit si le personnage est retourné
        self.retourne = False
        # on definit la liste d'animations
        self.liste_animation = []
        # on definit le nombre d'image et le changement
        self.liste_images = 0
        self.action = 0
        # on met a jour le temps
        self.maj_temps = py.time.get_ticks()
        # creer des variables spécifiques a l'ia
        # compte à rebours du deplacement
        self.deplacement_car = 0
        # on creer un rectangle qui va definir la vision de l'ia
        self.vision = py.Rect(0, 0, 150, 20)

        # on definit si l'ia est à l'arret
        self.arret = False
        # compte à rebours de l'arret
        self.arret_car = 0

        
        if self.nom == 'tiny':
            scale = 1.7
        else:
            pass

        # on enregistre tout les types d'images du joueur
        types_animations = self.liste_anim
        # on regarde chaque animation dans types_animation qui correspond à la liste d'animation
        for animation in types_animations:
            # on reinitialise la liste temporaire d'images
            liste_temporaire = []
            # on compte le nombre d'images dans le fichier grace au module os
            num_of_frames = len(os.listdir(f"Images/{self.nom}/{animation}/"))
            # on creer la boucle qui va charger nos images d'animation
            for i in range(num_of_frames):
                # on charge l'image
                image = py.image.load(f"Images/{self.nom}/{animation}/{i}.png").convert_alpha()
                # on la change selon le scale definit
                image = py.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
            # et on l'append
                liste_temporaire.append(image)
            self.liste_animation.append(liste_temporaire)

        # l'image est egale à l'image de self.action (par exemple en index 0 on est sur l'animation d'idle
        # donc quand l'entitée ne fait rien) et self.liste_images qui va correspondre à l'image actuelle de l'action et c'est grace
        # a ça qu'on va pouvoir creer des animations c'est a dire en changeant l'image actuelle
        self.image = self.liste_animation[self.action][self.liste_images]
        # on recupere le rect de l'image
        self.rect = self.image.get_rect()
        # on definit le rect center par rapport aux valeurs x et y qui ont été données en créant l'instance de la class
        self.rect.center = (x, y)
        # on recupère la largeur et la hauteur de l'image
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    # fonction update qui va regroupe tout les fonctions/actions qui devront etre réalisées en continu
    def update(self):
        self.update_animation()
        self.verif_vivant()

        # temps de mise a jour
        # si self.tirer_temps est superieur à 0
        if self.tirer_temps > 0:
            # on lui retire 1
            self.tirer_temps -= 1


    # fonction qui gère les deplacement/collisions etc.. qui prend en parametre le deplacement gauche et droite
    def deplacement(self, deplacement_gauche, deplacement_droite):
        # variable screen_scroll_x à 0
        screen_scroll_x = 0
        # varible de dx et dy à 0
        dx = 0
        dy = 0



        # si la variable deplacement gauche est sur True
        if deplacement_gauche:
            # la varible dx est egale à - self.vitesse
            dx = -self.vitesse
            # on se retourne
            self.retourne = True
            # et la direction est negative donc inversée
            self.direction = -1
        # si la variable de deplacament droite est dur True
        if deplacement_droite:
            # la variable dx est egale à self.vitesse
            dx = self.vitesse
            # on ne se retourne pas
            self.retourne = False
            # la direction ne change pas
            self.direction = 1

        # saut
        # si la touche de saut est sur True et que l'entitée n'est pas en l'air
        if self.saut == True and self.en_l_air == False:
            # on saute de -11
            self.velocite_y = -11
            # l'entitée ne saute plus donc on passe self.saut en False
            self.saut = False
            # et l'entitée est en l'air donc self.en_l_air est sur True tant qu'elle est en l'air
            self.en_l_air = True


        # appliquer une gravité
        # on ajoute à self.velocite_y la valeur de la gravite
        self.velocite_y += gravite
        # si self.velocite_y est superieur à 10
        if self.velocite_y > 10:
            # self.velocite_y est egal à 10
            self.velocite_y = 10
        # et dy est egal à self.velocite_y
        dy += self.velocite_y


        # verifier les colisions
        for tile in monde.obstacle_liste:
            # verifier les collisions en x
            # si l'entité touche un bloc en coordonnée x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                # dx passe à 0 donc le joueur s'arrete
                dx = 0
                # si l'ia a touché un mur  on la fait retourner en arriere
                if self.nom == 'monstre':
                    self.direction *= -1
                    self.arret_car = 0
            # si l'entité touche un bloc en coordonnée y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # si la velocite en y est inferieure à 0
                if self.velocite_y < 0:
                    # elle est egale à 0
                    self.velocite_y = 0
                    # dy est egal à la coordonnée en y du tile sur son bottom - self.rect.top (pour les collisions entre la tete de l'entité
                    # avec le bas du bloc)
                    dy = tile[1].bottom - self.rect.top
                # si la velocité en y est superieure ou égale à 0
                elif self.velocite_y >= 0:
                    # elle est égale à 0
                    self.velocite_y = 0
                    # l'entitée n'est pas en l'air
                    self.en_l_air = False
                    # dy est égal à la coordonnée en y du tile sur son top - self.rect.bottom (pour les collisions entre les pieds de l'entité
                    # avec le haut du bloc)
                    dy = tile[1].top - self.rect.bottom


        # si le nom est egal à player (sert à spécifier des conditions)
        if self.nom == 'player':
            # si le joueur tente de depasser le monde par la gauche ou la droite
            if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
                # dx est egal à 0 et donc le joueur ne peut pas aller plus loin
                dx = 0




        # verifier les collisions avec les piques
        # si il y a une collision entre une entitée et un pique
        if py.sprite.spritecollide(self, groupe_piques, False):
            # on retire 1 point de vie (impossible de sortir des piques mais je ne voulais pas faire une
            # mort intantannée avec un -= 100)
            self.point_de_vie -= 1

        # verifier les collisions avec la sortie
        # le niveau n'est pas complété
        niveau_complete = False
        # si il y a un collision avec une sortie
        if py.sprite.spritecollide(self, groupe_sorties, False):
            # le niveau est complété
            niveau_complete = True



        # verifier si une entitée tombe de la map
        # si le rect en bottom est superieur à la hauteur de la fenetre
        if self.rect.bottom > screen_height:
            # les points de vie passent à 0 et le joueur meurt
            self.point_de_vie = 0


        # mettre a  jour la position du rect
        self.rect.x += dx
        self.rect.y += dy

        # mettre a jour le scroll en fonction de la position du joueur
        # encore une spécialisation au joueur
        if self.nom == 'player':
            # si le rect du joueur est supérieur à la distance indiquée qui correspond à la valeur max avant de deplacer la "camera"
            # grace a distance_scroll qui est definit à 200 et que le scroll du background est inferieur à la taille du monde
            # (les colonnes donc 150 (150 pas obligé car la valeur peut changer)) * la taille d'un bloc donc 150 * 40 = 6000 - screen_width
            # donc - 800 donc 6000 - 800 = 5200 ce qui correspond à la limite du monde ou si le self.rect en left est inferieur à
            # distance_scroll et que background_scroll est superieur à la valeur absolue de dx
            if (self.rect.right > screen_width - distance_scroll and background_scroll < (monde.taille_niveau * taille_tile) - screen_width) or (self.rect.left < distance_scroll and background_scroll > abs(dx)):
                # on enleve la valeur de dx au self.rect en x
                self.rect.x -= dx
                # et le screen_scroll_x est égal à -dx
                screen_scroll_x = -dx
        
        # on return screen_scroll_x et niveau_complete
        return screen_scroll_x, niveau_complete    

    # fonction pour que le joueur tire un projectile
    def tirer(self):
        # si self.tirer_temps est egal à 0 et que l'entitée a encore des munitions
        if self.tirer_temps == 0 and self.munition > 0:
            # self.tirer_temps est egal à 25
            self.tirer_temps = 25
            # on creer une instance de pierre 
            pierre = Pierre(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            # on la rajoute dans le groupe des pierres
            groupe_pierre.add(pierre)
            # et on retire une munition
            self.munition -= 1


    # fonction qui gère l'ia qui ne concerne que les monstres
    def ia(self):
        # si l'entitée est encore en vie et que le joueur l'est aussi
        if self.vivant and joueur.vivant:
            # si le monstre n'est pas en arret et que le nombre qui est un random entre 1 et 200 est egal à 1
            if self.arret == False and random.randint(1, 2000) == 1:
                # le monstre est à l'arret
                self.arret = True
                # on joue l'animation de idle
                self.update_action(0)
                # on remet le compte à rebours de l'arret à 50
                self.arret_car = 50
            #regarder si l'ia est proche du joueur
            if self.vision.colliderect(joueur.rect):
                # arreter de courir et rester face au joueur
                # on joue l'animation de idle
                self.update_action(0)
                # on tire des pierre
                self.tirer()
            # sinon
            else:
                # si le monstre n'est pas à l'arret
                if self.arret == False:
                    # si sa direction est egale à 1
                    if self.direction == 1:
                        # le monstre se deplace vers la droite
                        ia_deplacement_droite = True
                    # sinon
                    else:
                        # le monstre ne se deplace pas vers la droite
                        ia_deplacement_droite = False
                    # le deplacement gauche du monstre est egal à l'inverse du deplacement droit
                    ia_deplacement_gauche = not ia_deplacement_droite
                    # on appelle la fonction deplacement pour le monstre
                    self.deplacement(ia_deplacement_gauche, ia_deplacement_droite)
                    # on active l'action de deplacement
                    self.update_action(1)
                    # on rajoute 1 au compte à rebours de deplacement
                    self.deplacement_car += 1
                    # mettre a jour la vision avec les mouvements du monstre
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)                   
                    # si le compte à rebours de deplacement est superieur a la taille d'un bloc
                    if self.deplacement_car > taille_tile:
                        # on change la direction
                        self.direction *= -1
                        # on inverse self.deplacement_car
                        self.deplacement_car *= -1
                # sinon
                else:
                    # on retire 1 au compte à rebours d'arret
                    self.arret_car -= 1
                    # si le compte à rebours d'arret est inferieur ou égal à 0
                    if self.arret_car <= 0:
                        # le monstre n'est plus à l'arret
                        self.arret = False


        # scroll
        self.rect.x += screen_scroll_x

    # fonction qui met à jour l'animation
    def update_animation(self):
        # mettre à jour l'animation
        car_animation = 100 # car = compte à rebours
        # Mettre à jour l'animation par rapport à l'image actuelle
        self.image = self.liste_animation[self.action][self.liste_images]
        # check si assez de temps est passé pour passer à l'image suivante
        if py.time.get_ticks() - self.maj_temps > car_animation:
            self.maj_temps = py.time.get_ticks()
            self.liste_images += 1
            # Si il n'y a plus d'images on retourne à la 1ere
        if self.liste_images >= len(self.liste_animation[self.action]):
            if self.action == 2:
                self.liste_images = len(self.liste_animation[self.action]) - 1
            else:
                self.liste_images = 0

    # fonction qui met à jour l'action
    def update_action(self, nouvelle_action):
        # verifier si la nouvelle action est differente de la precedente
        if nouvelle_action != self.action:
            # l'action est egale à la nouvelle action
            self.action = nouvelle_action
            # mettre à jour les parametres d'animation
            self.liste_images = 0
            self.maj_temps = py.time.get_ticks()


    # fonction qui vérifie si l'entitée est encore en vie
    def verif_vivant(self):
        # si les points de vie sont inferieur ou egal à 0
        if self.point_de_vie <= 0:
            # les points de vie sont égal à 0
            self.point_de_vie = 0
            # la vitesse est egale à 0
            self.vitesse = 0
            # l'entitée n'est plus vivante
            self.vivant = False
            # on lance l'animation de mort
            self.update_action(2)


    def dessiner(self):
        screen.blit(py.transform.flip(self.image, self.retourne, False),self.rect)
        py.draw.rect(screen, rouge, self.rect, 1)

#==================================================================#

# on creer la class de notre monde
class Monde():
    # la class n'as pas besoins d'aguments
    def __init__(self):
        # on definit la liste des obstacles (blocs avec collision)
        self.obstacle_liste = []

    # fonction qui va créer le monde qui prends en argument les données du monde
    def process_donnees(self, donnee):
        # la taille du niveau est egale à la len de donnee sur l'axe x donc ici 150
        self.taille_niveau = len(donnee[0])
        # boucle qui va prendre dans donnée la valeur de y (le nombre de ligne donc de 0 à 15 et ligne qui va etre chaque liste de ligne dans donnee)
        for y, ligne in enumerate(donnee):
        # boucle qui va prendre dans donnée la valeur de x (le nombre de ligne donc de 0 à 149 et tile qui va etre chaque bloc)
            for x, tile in enumerate(ligne):
                # si tile est supérieur ou égal à 0
                if tile >= 0:
                    # image est egal à la liste des textures qui ont ete importées
                    image = image_liste[tile]
                    # on prend leur rect
                    image_rect = image.get_rect()
                    # le rect x est egal à x * la taille d'un bloc
                    image_rect.x = x * taille_tile
                    # le rect y est egal à y * la taille d'un bloc
                    image_rect.y = y * taille_tile
                    # donnée du bloc qui est egal à l'image et à son rect
                    donnee_tile = (image, image_rect)
                    # si le bloc est compris entre 0 et 10
                    if tile >= 0 and tile <= 10:
                        # on l'ajoute a la liste des obstacles
                        self.obstacle_liste.append(donnee_tile)
                    # si le bloc est egal à 11
                    elif tile == 11:
                        # on creer une instance de Boites pour une boite de vie
                        boite = Boites('Vie', x * taille_tile, y * taille_tile, 0.8)
                        groupe_boite.add(boite)
                    # si le bloc est egal à 12
                    elif tile == 12:
                        # on creer une instance de Boites pour une boite de vie
                        boite = Boites('Munition', x * taille_tile, y * taille_tile, 0.8)
                        groupe_boite.add(boite)
                    # si le bloc est egal à 13
                    elif tile == 13:
                        # on creer une instance de Boites pour une boite de vie
                        boite = Boites('Projectile', x * taille_tile, y * taille_tile, 0.8)
                        groupe_boite.add(boite)
                    # si le bloc est egal à 14
                    elif tile == 14:
                        # on creer une instance de Boites pour une boite de vie
                        piques = Piques(image, x * taille_tile, y * taille_tile)
                        groupe_piques.add(piques)
                    # si le bloc est egal à 15
                    elif tile == 15:
                        # on creer le joueur et sa barre de vie
                        joueur = Entite("player",x * taille_tile, y * taille_tile, 2.1, 5, 20, 5, liste_anim_joueur)
                        barre_vie = Barre_vie()
                    # si le bloc est egal à 16
                    elif tile == 16:
                        # on creer un monstre
                        monstre = Entite(random.choice(liste_monstre), x * taille_tile, x * taille_tile, 2, 2, 20, 0, liste_anim_monstre)
                        groupe_monstre.add(monstre)
                    # si le bloc est compris entre 17 et 18
                    elif tile >= 17 and tile <= 18:
                        # on creer une instance de Decoration pour les decorations
                        decoration = Decoration(image, x * taille_tile, y * taille_tile, 1)
                        groupe_decoration.add(decoration)
                    elif tile >= 20 and tile <= 28:
                        # on creer une instance de Decoration pour les decorations
                        decoration = Decoration(image, x * taille_tile, y * taille_tile, 2)
                        groupe_decoration.add(decoration)
                    elif tile >= 29 and tile <= 30:
                        # on creer une instance de Decoration pour les decorations
                        decoration = Decoration(image, x * taille_tile, y * taille_tile, 1.4)
                        groupe_decoration.add(decoration)
                    elif tile >= 31 and tile <= 38:
                        # on creer une instance de Decoration pour les decorations
                        decoration = Decoration(image, x * taille_tile, y * taille_tile, 3.5)
                        groupe_decoration.add(decoration)
                    elif tile == 39:
                        sortie = Sortie(image, x * taille_tile, y * taille_tile)
                        groupe_sorties.add(sortie)
        # on return joueur et barre vie
        return joueur, barre_vie

    # fonction qui blit chaque image
    def creer(self):
        # pour chaque bloc dans la liste des obstacles
        for tile in self.obstacle_liste:
            # on applique le scroll en x
            tile[1][0] += screen_scroll_x
            # on blit chaque image avec son rect
            screen.blit(tile[0], tile[1])


# class qui concerne les decorations
class Decoration(py.sprite.Sprite):
    # on demande l'image, la position en x et en y
    def __init__(self, image, x, y, scale):
        py.sprite.Sprite.__init__(self)
        # on definit l'image
        self.image = image
        self.image = py.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        # on recupere le rect
        self.rect = self.image.get_rect()
        # on definit le rect.midtop
        self.rect.midtop = (x + taille_tile // 2, y + (taille_tile - self.image.get_height()))

    # fonction update pour le scroll
    def update(self):
        self.rect.x += screen_scroll_x


# class pour les pique
class Piques(py.sprite.Sprite):
    # on demande l'image, la position en x et en y
    def __init__(self, image, x, y):
        py.sprite.Sprite.__init__(self)
        # on definit l'image
        self.image = image
        # on recupere le rect
        self.rect = self.image.get_rect()
        # on definit le rect midtop
        self.rect.midtop = (x + taille_tile // 2, y + (taille_tile - self.image.get_height()))

    # fonction update pour le scroll
    def update(self):
        self.rect.x += screen_scroll_x

# class pour la sortie
class Sortie(py.sprite.Sprite):
    # on demande l'image, la position en x et en y
    def __init__(self, image, x, y):
        py.sprite.Sprite.__init__(self)
        # on definit l'image
        self.image = image
        # on recupere le rect
        self.rect = self.image.get_rect()
        # on definit le rect midtop
        self.rect.midtop = (x + taille_tile // 2, y + (taille_tile - self.image.get_height()))

    # fonction update pour le scroll
    def update(self):
        self.rect.x += screen_scroll_x

# class pour les boites
class Boites(py.sprite.Sprite):
    # on demande le type de boite
    def __init__(self, objet, x, y, scale):
        py.sprite.Sprite.__init__(self)
        # on definit la boite
        self.objet = objet
        # l'image de la boite est egale à celle du dictionnaire
        self.image = boite_objet[self.objet]
        self.image = py.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
        # on recupere le rect
        self.rect = self.image.get_rect()
        # on definit le rect.midtop
        self.rect.midtop = (x + taille_tile // 2, y + (taille_tile - self.image.get_height()))

    # fonction update
    def update(self):
        # scroll
        self.rect.x += screen_scroll_x
        # verifier si le joueur a recuperer la boite
        if py.sprite.collide_rect(self, joueur):
            # verifier le type de boite
            # si c'est une boite de vie
            if self.objet == 'Vie':
                # on rajoute 25 pdv
                joueur.point_de_vie += 25
                # si je nombre de pdv est au dessus du nombre de max
                if joueur.point_de_vie > joueur.pdv_max:
                    # on le redescend au nombre max
                    joueur.point_de_vie = joueur.pdv_max
            # si c'est une boite de munition
            elif self.objet == 'Munition':
                # on donne 10 pierres 
                joueur.munition += 10
            # si c'est une boite de projectiles
            elif self.objet == 'Projectile':
                # on donne 3 projectiles
                joueur.projectile += 3
            # et on supprime la boite
            self.kill()


# class de la barre de vie du joueur
class Barre_vie():
    # on demande la position en x et y, la vie et la vie max
    def __init__(self):
        self.nombre_coeur = 4


    # fonction qui creer la barre
    def update(self, vie):
    
        if joueur.point_de_vie <= 75:
            self.nombre_coeur = 3
        if joueur.point_de_vie <= 50:
            self.nombre_coeur = 2
        if joueur.point_de_vie <= 25:
            self.nombre_coeur = 1
        if joueur.point_de_vie <= 0:
            self.nombre_coeur = 0


# class pour la pierre (lancée avec la souris)
class Pierre(py.sprite.Sprite):
    # on demande les coordonnées en x et en y ainsi que la direction (qui sera definie sur celle de l'entitée pour
    # pouvoir changer de direction selon celle de l'entitée)
    def __init__(self, x, y, direction):
        py.sprite.Sprite.__init__(self)
        # on definit la vitesse
        self.vitesse = 10
        # on definit l'image
        self.image = pierre_image
        # on recupere son rect
        self.rect = self.image.get_rect()
        # on definit son rect.center
        self.rect.center = (x, y)
        # on definit sa direction
        self.direction = direction


    # fonction update qui va gerer les deplacements et collisions
    def update(self):
        # deplacer la pierre
        # on ajoute au rect en x de la pierre la direction et la vitesse pour definir de quel coté va aller la pierre
        # et on ajoute le screen scroll pour que la pierre se deplace selon la camera
        self.rect.x += (self.direction * self.vitesse) + screen_scroll_x
        # la distance est agle au rect en x de la pierre
        distance = self.rect.x

        # verifier si la pierre sort de l'ecran
        # si la pierre a un coordonné inferieur à 0 ou superieur à la largeur de la fenetre
        if self.rect.right < 0 or self.rect.left > screen_width:
            # on detruit la pierre
            self.kill()


        # verifier les collisions avec le monde
        # dans la liste des blocs dans la liste des obstacles du monde
        for tile in monde.obstacle_liste:
            # si les coordonnées d'un bloc rentre en collision avec la pierre
            if tile[1].colliderect(self.rect):
                # on kill la pierre
                self.kill()

        # verifier les collisions avec une autre entitée
        # si il y a collision entre le groupe de pierre et le joueur
        if py.sprite.spritecollide(joueur, groupe_pierre, False):
            # et si le joueur est encore en vie
            if joueur.vivant:
                # on enlève 5 pdv au joueur
                joueur.point_de_vie -= 25
                # et on detruit la pierre
                self.kill()
        # pour chaque monstre dans la liste de monstre
        for monstre in groupe_monstre:
            # si il ya collision entre le groupe de pierre et un monstre
            if py.sprite.spritecollide(monstre, groupe_pierre, False):
                # et si le monstre est vivant
                if monstre.vivant:
                    # on lui enleve 25 pdv
                    monstre.point_de_vie -= 25
                    # et on detruit la pierre
                    self.kill()
        

# class du projectile (se lance avec a)
class Projectile(py.sprite.Sprite):
    # on demande les coordonnées en x et en y ainsi que la direction (qui sera definie sur celle de l'entitée pour
    # pouvoir changer de direction selon celle de l'entitée)
    def __init__(self, x, y, direction):
        py.sprite.Sprite.__init__(self)
        # on definit le compte à rebours avant l'explosion
        self.car = 100
        # on definit sa velocité en y
        self.velocite_y = -11
        # on defininit sa vitesse
        self.vitesse = 7
        # on definit son image
        self.image = pierre_projectile_image
        # on recupere le rect de l'image
        self.rect = self.image.get_rect()
        # on definit son rect.center
        self.rect.center = (x, y)
        # on recupere sa largeur et sa hauteur
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # on definit sa direction
        self.direction = direction
        

    # fonction update qui va gerer les deplacement, la physique du projectile, les collisons
    # et tout se qui va se passer pour gerer l'explosion
    def update(self):
        # scroll
        self.rect.x += screen_scroll_x
        # on applique une gravité au projectile
        self.velocite_y += gravite
        # dx est egal a la direction * la vitesse pour definir le sens
        dx = self.direction * self.vitesse
        # dy est egal à la velocité en y 
        dy = self.velocite_y


        # verifier les collisions avec le monde
        # pour chaque bloc dans la liste d'obstacle dans le monde
        for tile in monde.obstacle_liste:
            # verifier la collision avec les murs
            # si il y a un collision en x avec un mur
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    # on change de sens (en gros le projectile rebondit)
                    self.direction *= -1
                    dx = self.direction * self.vitesse
            # si il y a une collision en y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # la vitesse passe à 0                
                self.vitesse = 0
                # si la velocité est inferieure à 0
                if self.velocite_y < 0:
                    # elle est egale à 0
                    self.velocite_y = 0
                    # et donc le projectile reste sur le bloc
                    dy = tile[1].bottom - self.rect.top + 25
                # si la velocité est superieure à 0
                elif self.velocite_y >= 0:
                    # elle est egale à 0
                    self.velocite_y = 0
                    # et donc le projectile reste sur le bloc
                    dy = tile[1].top - self.rect.bottom + 25



        # mettre a jour la position du projectile
        self.rect.x += dx
        self.rect.y += dy

        # le compte à rebours baisse de 1
        self.car -= 1
        # si le compte à rebours est inferieur ou égal à 0
        if self.car <= 0:
            # on supprime le projectile
            self.kill()
            # on joue le son de l'explosion
            explosion_son.play()
            # on creer une instance de Explosion
            explosion = Explosion(self.rect.x + 30, self.rect.y + 25, 1.2)
            groupe_explosion.add(explosion)
            # infliger des degats a toutes les entitées à proximité
            # si le joueur se trouve à proximité de l'explosion (2 blocs)
            if abs(self.rect.centerx - joueur.rect.centerx) < taille_tile * 2 and abs(self.rect.centery - joueur.rect.centery) < taille_tile * 2:
                # on lui retire 50 pdv
                joueur.point_de_vie -= 50
            # pour chaque monstre dans le groupe de monstre
            for monstre in groupe_monstre:
                # si le joueur se trouve à proximité de l'explosion (2 blocs)
                if abs(self.rect.centerx - monstre.rect.centerx) < taille_tile * 2 and abs(self.rect.centery - monstre.rect.centery) < taille_tile * 2:
                    # on lui retire 50 pdv
                    monstre.point_de_vie -= 50


# class qui va gerer l'explosion du projectile
class Explosion(py.sprite.Sprite):
    # on demande les coordonnées en x et y ainsi que le scale
    def __init__(self, x, y, scale):
        py.sprite.Sprite.__init__(self)
        # on regroupe dans une liste l'ensemble des images qui sont dans le fichier explosion
        self.images = []
        # dans une boucle de 8 (nombre d'images)
        for i in range(8):
            # on load chaque image 
            img = py.image.load(f'Images/explosion/{i}.png').convert_alpha()
            # on change son scale en fontion de celui qu'on a definit
            img = py.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            # et on l'append
            self.images.append(img)
        # on definit l'index de l'image actuelle
        self.image_index = 0
        # on definit l'image actuelle
        self.image = self.images[self.image_index]
        # on recupere son rect
        self.rect = self.image.get_rect()
        # on definit son rect.center
        self.rect.center = (x, y)
        # on definit le compte à rebours de l'animation
        self.counter = 0

    def update(self):
        # scroll
        self.rect.x += screen_scroll_x
        # on definit la vitesse d'explosion qui correspond à la limite du compte à rebours
        vitesse_explosion = 4
        # mettre a jour l'animation d'explosion
        self.counter += 1

        # si le compte à rebours est supérieur à la limite
        if self.counter >= vitesse_explosion:
            # le compteur passe à 0
            self.counter = 0
            # on passe à l'image suivante
            self.image_index += 1
            # si l'animation est finie on la supprime
            if self.image_index >= len(self.images):
                self.kill()
            # sinon
            else:
                # l'image est egale à l'image actuelle
                self.image = self.images[self.image_index]








# class qui va gerer les effets à l'ecran
class EffetScreen():
    # on demande la direction, la couleur et la vitesse
    def __init__(self, direction, couleur, vitesse):
        # on definit la direction
        self.direction = direction
        # on definit la couleur
        self.couleur = couleur
        # on definit la vitesse
        self.vitesse = vitesse
        # on definit la distance de deplacement
        self.distance = 0


    # fonction qui va creer l'animation
    def creer(self):
        # variable qui definit si l'ecran est complété sur False
        ecran_complete = False
        # on rajoute a la distance la vitesse
        self.distance += self.vitesse

        # si la direction est egale à 1
        if self.direction == 1:
            # on creer avec des rectangles un effet d'ouverture avec 4 carrés qui disparaissent chacuns de leur coté
            py.draw.rect(screen, self.couleur, (0 - self.distance, 0, screen_width // 2, screen_height))
            py.draw.rect(screen, self.couleur, (screen_width // 2 + self.distance, 0, screen_width, screen_height))
            py.draw.rect(screen, self.couleur, (0, 0 - self.distance, screen_width, screen_height // 2))
            py.draw.rect(screen, self.couleur, (0, screen_height //2 + self.distance, screen_width, screen_height))

        # si la direction est egale à 2
        if self.direction == 2:
            # on creer un rectangle qui va aller vers le bas
            py.draw.rect(screen, self.couleur, (0, 0, screen_width, 0 + self.distance))
        # si la distance est superieure à la largeur de l'ecran
        if self.distance >= screen_width:
            # ecran est complété
            ecran_complete = True

        # on return ecran_complete
        return ecran_complete


# on creer une instance de EffetScreen pour l'effet de l'ecran du debut de partie
ecran_debut = EffetScreen(1, noir, 4)
# on creer une instance de EffetScreen pour l'effet de l'ecran de mort
ecran_mort = EffetScreen(2, couleur_fond, 4)



# creer les boutons
# on creer 3 boutons
# un bouton pour start la partie
start_bouton = bouton.Button(screen_width // 2 - 435, screen_height // 2 - 250, start, 2)
# un pour recommencer lorsque le joueur est mort
restart_bouton = bouton.Button(screen_width // 2 - 435, screen_height // 2 - 250, restart, 2)



# creer un groupe d'image
groupe_monstre = py.sprite.Group()
groupe_pierre = py.sprite.Group()
groupe_projectile = py.sprite.Group()
groupe_explosion = py.sprite.Group()
groupe_boite = py.sprite.Group()
groupe_decoration = py.sprite.Group()
groupe_sorties = py.sprite.Group()
groupe_piques = py.sprite.Group()
groupe_objets_animes = py.sprite.Group()



#==================================================================#


# dans la liste de vide on va ajouter des -1 partout en fontion des lignes et colonnes
# de la map definits precedement

donnee_monde = []
for ligne in range(lignes):
    l = [-1] * colonnes
    donnee_monde.append(l)


# charger les données et creer le monde
# on va ouvrir le fichier du niveau en tant que csvfile
with open(f'donnees_niveau{niveau}.csv', newline='') as csvfile:
    # on read csvfile en definissant le delimiter
    reader = csv.reader(csvfile, delimiter=',')
    # pour x qui correspond à de 0 à 15 dans la ligne
    for x, ligne in enumerate(reader):
        # pour y qui correspond à de 0 à 149 pour chaque bloc
        for y, tile in enumerate(ligne):
            # les coordonnées en x et y sont egales à int de tile
            donnee_monde[x][y] = int(tile)

# on creer une instance de Monde
monde = Monde()
# le joueur et la barre de vie dans la fonction process_donnees
joueur, barre_vie = monde.process_donnees(donnee_monde)


# boucle du jeu
# variable True pour lancer la boucle et le jeu
running = True
# boucle while du jeu
while running:

    # horloge d'image limitée à FPS 
    clock.tick(FPS)

    # si le debut de partie est sur False
    if debut_partie == False:
        # on creer le menu
        screen.blit(background_image, (0, 0))
        
        # si on appuie sur le bouton start
        if start_bouton.draw(screen):
            # on commence la partie
            debut_partie = True
            # on commence l'intro
            debut_intro = True
        # si on appuie sur le bouton exit
        

    # sinon
    else:

        # on creer le background
        background()
        # on creer le monde
        monde.creer()
        # on creer la barre de vie du joueur 
        barre_vie.update(joueur.point_de_vie)
        # on creer un texte avec ecrit munition
        texte(f'Munition : {joueur.munition}', police, blanc, 10, 50, 1)
        # on creer un texte avec ecrit Projectile
        texte(f'Projectile : {joueur.projectile}', police, blanc, 10, 75, 1)
        for i in range(barre_vie.nombre_coeur):
            screen.blit(coeur_image, (10 + (i * 40), 10))


        
        

        # mettre a jour et dessiner les groupes
        groupe_pierre.update()
        groupe_projectile.update()
        groupe_explosion.update()
        groupe_boite.update()
        groupe_decoration.update()
        groupe_piques.update()
        groupe_sorties.update()
        groupe_pierre.draw(screen)
        groupe_projectile.draw(screen)
        groupe_explosion.draw(screen)
        groupe_boite.draw(screen)
        groupe_decoration.draw(screen)
        groupe_piques.draw(screen)
        groupe_sorties.draw(screen)



        # on creer le joueur
        joueur.dessiner()
        # on update le joueur
        joueur.update()


        # pour chaque monstre dans le groupe de monstre
        for monstre in groupe_monstre:            
            # on dessine le monstre
            monstre.dessiner()
            # on update le monstre
            monstre.update()
            # on applique l'ia
            monstre.ia()


        # si le debut d'intro est sur True et donc a commencé
        if debut_intro == True:
            # si l'anim est lancée
            if ecran_debut.creer():
                # le debut d'intro passe sur False
                debut_intro = False
                # la distance passe à 0
                ecran_debut.distance = 0



        # mettre à jour les action du joueur
        # si le joueur est vivant
        if joueur.vivant:
            # si la variable de tir passe sur True
            if tir:
                # on tire une pierre
                joueur.tirer()
            # si projectile et lancer_projectile sont sur False et que le joueur a encore des projectile
            if projectile and lancer_projectile == False and joueur.projectile > 0:
                # on creer une instance de projectile et on l'ajoute au groupe
                projectile = Projectile(joueur.rect.centerx + (0.5 * joueur.rect.size[0] * joueur.direction),joueur.rect.top + 15, joueur.direction)
                groupe_projectile.add(projectile)
                # reduire le nombre de projectiles
                joueur.projectile -= 1
                # lancer_projectile passe sur True
                lancer_projectile = True
            # si le joueur est en l'air
            if joueur.en_l_air:
                # on lance l'animation de saut
                joueur.update_action(3)# 3 pour sauter
            # si le joueur effectue un deplacement vers la gauche ou la droite
            elif deplacement_gauche or deplacement_droite:
                # on lance l'animation de marche
                joueur.update_action(1)# 1 pour marcher
            # sinon
            else:
                # on lance l'animation d'idle
                joueur.update_action(0)# 0 pour idle
            


            # le screen scroll en x et le niveau compété est egal au deplacament gauche et droite du joueur
            screen_scroll_x, niveau_complete = joueur.deplacement(deplacement_gauche, deplacement_droite)
            # on retire au background scroll le screen scroll en x
            background_scroll -= screen_scroll_x
            #si le joueur a completer le niveau
            if niveau_complete:
                # on lance l'intro
                debut_intro = True
                # on passe au niveau suivant
                niveau += 1
                # le scroll du background passe à 0
                background_scroll = 0
                # on reinitialise tout
                donnee_monde = reinitialiser_niveau()
                # si le niveau est inferieur au niveau max
                if niveau <= niveau_max:
                    # charger les données et creer le monde
                    with open(f'donnees_niveau{niveau}.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, ligne in enumerate(reader):
                            for y, tile in enumerate(ligne):
                                donnee_monde[x][y] = int(tile)

        else:
            # le srceen scroll passe à 0
            screen_scroll_x = 0
            # si l'ecran de mort est creer
            if ecran_mort.creer():
                # si on clique sur le bouton restart
                if restart_bouton.draw(screen):
                    # la distance de l'ecran de mort passe à 0
                    ecran_mort.distance = 0
                    # on relance l'intro
                    debut_intro = True 
                    # le scroll du background passe à 0
                    background_scroll = 0
                    # on reinitialise le niveau
                    donnee_monde = reinitialiser_niveau()
                    # charger les données et creer le monde
                    with open(f'donnees_niveau{niveau}.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, ligne in enumerate(reader):
                            for y, tile in enumerate(ligne):
                                donnee_monde[x][y] = int(tile)
                    monde = Monde()
                    joueur, barre_vie = monde.process_donnees(donnee_monde)



    # mise à jour du contenu
    py.display.flip()


    # event pour fermer la page
    for event in py.event.get():
        # si cet event est egal a py.QUIT
        if event.type == py.QUIT:
            # le variable running passe en False
            running = False
            

    # appuyer sur le clavier
        if event.type == py.KEYDOWN:
            # si la touche est egale à Q
            if event.key == py.K_q:
                # le deplacement gauche passe sur True
                deplacement_gauche = True
            # si la touche est egale à D
            if event.key == py.K_d:
                # le deplacement droite passe sur True
                deplacement_droite = True
            # si la touche est egale à A
            if event.key == py.K_a:
                # projectile est egal à True
                projectile = True
            # si la touche est egale à SPACE
            if event.key == py.K_SPACE and joueur.vivant:
                # le joueur saute
                joueur.saut = True
            if event.key == py.K_ESCAPE:
                running = False

            # relacher le bouton
        if event.type == py.KEYUP:
            # si la touche est egale à D
            if event.key == py.K_q:
                # le deplacement gauche passe sur False
                deplacement_gauche = False
            # si la touche est egale à D
            if event.key == py.K_d:
                # le deplacement droite passe sur False
                deplacement_droite = False
            # si la touche est egale à D
            if event.key == py.K_a:
                # lancer projectile et projectile passent sur False
                projectile = False
                lancer_projectile = False

        # si on appuie sur la souris
        if event.type == py.MOUSEBUTTONDOWN:
            # tir passe sur True
            tir = True

        # si on lache la souris
        if event.type == py.MOUSEBUTTONUP:
            # tir passe sur False
            tir = False


        if event.type == py.VIDEORESIZE:
            screen = py.display.set_mode((event.w, event.h), py.RESIZABLE)
py.quit()

#==================================================================#