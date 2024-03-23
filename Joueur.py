from pilefile import Pile
from domino import Domino
from random import randint

class Joueur :
    '''Classe permettant de modeliser un joueur du jeu Mexicain'''
    def __init__(self,jeu) :
        '''Joueur,JeuMexicain -> Joueur
        Permet d'initialiser une instance de la classe joueur avec ses composants'''
        # Attribut train, reserve, JeuMexicain et open
        self.__train = Pile()
        self.__reserve = list()
        self.__jeu = jeu
        self.__open = False
    

    def est_open(self) :
        '''Joueur -> bool
        Teste si le joueur est open ou pas'''
        return self.__open


    def train_a_demarre(self) :
        '''Joueur -> boolean
        Teste si le train a demarre ou pas'''
        return not self.__train.est_vide()


    def dernier_domino(self) :
        '''Joueur -> Domino
        Retourne le dernier domino du train du joueur'''
        return self.__train.sommet()


    def est_posable_train(self,domino) :
        '''Joueur -> Domino
        Retourne si domino est posable sur le train'''
        # Si le train n'a pas demarré, il compare avec le dominoDepart
        if not self.train_a_demarre() :
            return domino.peutEtrePlaceApres(self.__jeu.domino_depart())
        # Si non il compare avec le dernier domino du train
        return domino.peutEtrePlaceApres(self.dernier_domino())
    

    def possible_train(self,domino) :
        '''Joueur -> Domino
        Retourne si domino ou son inverse est posable ou inversement posable sur le train'''
        # Si le train n'a pas demarré, il compare avec le dominoDepart
        if not self.train_a_demarre() :
            return domino.possible_apres(self.__jeu.domino_depart())
        # Si non il compare avec le dernier domino du train
        return domino.possible_apres(self.dernier_domino())


    def est_posable_train_mexicain(self,domino) :
        '''Joueur -> Domino
        Retourne si domino est posable sur le train mexicain'''
        # Si le train n'a pas demarré, il compare avec le dominoDepart
        if not self.__jeu.train_a_demarre() :
            return domino.peutEtrePlaceApres(self.__jeu.domino_depart())
        # Si non il compare avec le dernier domino du train
        return domino.peutEtrePlaceApres(self.__jeu.dernier_domino())
    
    
    def possible_train_mexicain(self,domino) :
        '''Joueur -> Domino
        Retourne si domino est posable ou inversement posable sur le train mexicain'''
        # Si le train n'a pas demarré, il compare avec le dominoDepart
        if not self.__jeu.train_a_demarre() :
            return domino.possible_apres(self.__jeu.domino_depart())
        # Si non il compare avec le dernier domino du train
        return domino.possible_apres(self.__jeu.dernier_domino())
    
    
    def possible_train_joueurs(self,domino,joueurs) :
        '''Joueurs -> Domino
        Teste si le domino est posable sur un des trains des joueurs ouverts'''
        for joueur in joueurs.values() :
            if joueur.possible_train(domino) :
                return True
        return False

    def nbre_domino_reserve(self) :
        '''Joueur -> int
        Retourne le nombre de domino dans la reserve'''
        return len(self.__reserve)


    def nieme_domino(self,n) :
        '''Joueur,int -> Domino
        Retourne le nième domino de sa reserve'''
        assert 0 < n <= len(self.__reserve)
        return self.__reserve[n-1]


    def plus_grand_domino_double(self) :
        '''Joueur -> Domino
        Retourne l'indice du plus grand domino double du joueur'''
        ind_maxi = -1
        # On parcours pour rechercher le plus grand et le retourne
        for ind in range(len(self.__reserve)) :
            if ind_maxi == -1 and self.__reserve[ind].estDouble():
                ind_maxi = ind
            elif self.__reserve[ind].estDouble() and self.__reserve[ind].valeur() > self.__reserve[ind_maxi].valeur() : 
                ind_maxi = ind
        return ind_maxi


    def PDST(self) :
        '''Joueur -> int
        Retourne l'indice du premier domino de sa reserve posable ou inversement posable sur son train'''
        # On parcours pour chercher le premier
        for ind in range(len(self.__reserve)) :
            if self.possible_train(self.__reserve[ind]) :
                self.__open = False
                return ind
        # Si non il retourne -1
        return -1


    def PDSTM(self) :
        '''Joueur -> int
        Retourne l'indice du premier domino de sa reserve posable ou inversement posable sur le train mexicain'''
        # On parcours pour chercher le premier
        for ind in range(len(self.__reserve)) :
            if self.possible_train_mexicain(self.__reserve[ind]) :
                self.__open = False
                return ind
        # Si non il retourne -1
        return -1
    

    def PDSTJ(self,joueurs) :
        '''Joueurs -> tuple(Joueur,int)
        Retourne le joueur ouvert et l'indice du premier domino de la reserve posable ou inversement posable sur un des trains des joueurs ouverts'''
        # On parcours pour chercher le premier
        for ind in range(len(self.__reserve)) :
            for joueur in joueurs.values() :
                if joueur.possible_train(self.__reserve[ind]) :
                    self.__open = False
                    return joueur,ind
        # Si il trouve pas il retourne None et -1
        return None,-1
                

    def pose_domino_train(self,domino) :
        '''Joueur,Domino -> None
        Pose le domino sur le train sachant qu'il est correct'''
        self.__train.empiler(domino)


    def pose_domino_train_mexicain(self,domino) :
        '''Joueur,Domino -> None
        Pose le domino sur le train mexicain sachant qu'il est correct'''
        self.__jeu.pose_domino(domino)


    def pioche(self) :
        '''Joueur -> None
        Permet au joueur de piocher dans la pioche du jeu'''
        if not self.__jeu.pioche_est_vide() :
            self.__reserve.append(self.__jeu.pioche())
        # Le joueur ne peut pas devenir ouvert si le domino depart n'est pas choisi
        if self.__jeu.est_choisi_depart() :
            self.__open = True


    def str_dominos(self) :
        '''JeuMexicain -> list(str)
        Retourne une liste des strings des cinq premier dominos de la pile'''
        cpt = 0
        p1 = Pile()
        # Il met les elements du train dans une file en les comptants
        while not self.__train.est_vide() and cpt < 5 :
            p1.empiler(self.__train.depiler())
            cpt += 1
        # Il les remets dans le train en prenant leurs str
        liste_str = ["\t","\t","\t","\t","\t"]
        cpt = 0
        while not p1.est_vide() :
            domino = p1.depiler()
            liste_str[cpt] = domino.__str__()
            self.__train.empiler(domino)
            cpt += 1
        return liste_str
    

    def img_dominos(self) :
        '''JeuMexicain -> list(tuple(int))
        Retourne une liste des coordonnées des images des cinq premier dominos de la pile'''
        cpt = 0
        p1 = Pile()
        # Il met les elements du train dans une file en les comptants
        while not self.__train.est_vide() and cpt < 5 :
            p1.empiler(self.__train.depiler())
            cpt += 1
        # Il les remets dans le train en prenant leurs coordonnées de images
        liste_img = [(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1)]
        cpt = 0
        while not p1.est_vide() :
            domino = p1.depiler()
            liste_img[cpt] = domino.coord_image()
            self.__train.empiler(domino)
            cpt += 1
        return liste_img
    

    def supprimer_domino(self,ind) :
        '''Joueur,int -> None 
        Supprime le domino à l'indice i dans la reserve'''
        assert 0 <= ind < len(self.__reserve)
        del(self.__reserve[ind]) 

    
    def donner_domino_depart(self) :
        '''Controleur -> None
        Regarde le plus grand domino double dans la reserve, si il ne trouve pas, il pioche'''
        # Il prend l'indice du domino double pour le choisir comme dominoDepart
        ind_domino = self.plus_grand_domino_double()
        # Si c'est vide, il pioche
        if ind_domino == -1 :
            self.pioche()
        # Si non, il supprime le domino et le choisis comme dominoDepart
        else :
            self.__jeu.choisi_domino_depart(self.__reserve[ind_domino])
            self.supprimer_domino(ind_domino)

    
    def dominos_posables(self,joueurs) :
        '''Joueur,dico(int: Joueur) -> list(int)
        Renvoie les indice des dominos posables inversement posable, soit sur le train, sur le train mexicain ou sur un des joueurs ouverts'''
        btns = list()
        # Parcours les dominos pour ajouter les indices
        for ind in range(len(self.__reserve)) :
            if self.possible_train(self.__reserve[ind]) or self.possible_train_mexicain(self.__reserve[ind]) or self.possible_train_joueurs(self.__reserve[ind],joueurs) :
                btns.append(ind)
                self.__open = False
        # il les retourne
        return btns

    
    def jouer(self,joueurs) :
        '''Joueur -> Boolean
        Permet aux joueurs artificiels de jouer et teste si le joueur a pioché ou pas'''
        # Regarde si il y'a un domino posable sur le train
        ind = self.PDST()
        if ind == -1 :
            # Si il ne trouve pas, il cherche pour le train mexicain
            ind = self.PDSTM()
            if ind == -1 :
                # Si il ne trouve pas, il cherche sur le train des joueurs ouverts
                joueur,ind = self.PDSTJ(joueurs)
                if ind == -1 :
                    # Si il trouve pas il pioche
                    self.pioche()
                    return True
                domino = self.__reserve[ind]
                # Si le domino trouvé est posable sur le train du joueur
                if joueur.est_posable_train(domino) :
                    joueur.pose_domino_train(domino)
                # Si non c'est l'inverse qui est posable
                else :
                    self.permuter(ind)
                    joueur.pose_domino_train(self.__reserve[ind])
                self.supprimer_domino(ind)
                # Si le domino est double, il joue encore
                if domino.estDouble() :
                    self.jouer(joueurs)
                return False
            domino = self.__reserve[ind]
            # Si le domino trouvé est posable sur le train
            if self.est_posable_train_mexicain(domino) :
                self.pose_domino_train_mexicain(domino)
            # Si non c'est l'inverse qui est posable
            else :
                self.permuter(ind)
                self.pose_domino_train_mexicain(self.__reserve[ind])
            self.supprimer_domino(ind)
            # Si le domino est double, il joue encore
            if domino.estDouble() :
                self.jouer(joueurs)
            return False
        domino = self.__reserve[ind]
        # Si le domino trouvé est posable sur le train
        if self.est_posable_train(domino) :
            self.pose_domino_train(domino)
        # Si non c'est l'inverse qui est posable
        else :
            self.permuter(ind)
            self.pose_domino_train(self.__reserve[ind])
        self.supprimer_domino(ind)
        # Si le domino est double, il joue encore
        if domino.estDouble() :
            self.jouer(joueurs)
        return False


    def a_gagne(self) :
        '''Joueur -> Boolean
        Teste si le joueur a gagné ou pas c'est a dire si sa reserve est vide'''
        return len(self.__reserve) == 0

    
    def recommencer(self) :
        '''Joueur -> None
        Remet tous les dominos de son train et de sa reserve dans la pioche'''
        # Remet les dominos du train dans la pioche
        while not self.__train.est_vide() :
            self.__jeu.empile_pioche(self.__train.depiler())
        
        # Remet les dominos de la reserve dans la pioche et la vide 
        for domino in self.__reserve :
            self.__jeu.empile_pioche(domino)
        self.__reserve.clear()
    

    def permuter(self,ind) :
        '''Joueur,int -> None
        Permet de permuter le domino à l'indice ind de la reserve du joueur'''
        if ind < len(self.__reserve) :
            self.__reserve[ind].permuter()
