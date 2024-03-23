from pilefile import Pile
from random import randint
from domino import Domino

class JeuMexicain :
    '''Classe permettant de modeliser le jeu du train mexicain'''
    def __init__(self) :
        '''JeuMexicain -> JeuMexicain
        Permet de creer une instance de la classe JeuMexicain et d'initialiser ses composants'''
        # Attribut du domino de depart, du train et de la pioche
        self.__dominoDepart = Domino(-1,-1)
        self.__trainMexicain = Pile()
        self.__pioche = Pile()
        
        # Création des dominos
        dominos = []
        for i in range(13) :
            for j in range(13) :
                dominos.append(Domino(i,j))
        
        # Melange des dominos 
        for i in range(1000) :
            a,b = randint(0,168),randint(0,168)
            dominos[a],dominos[b] = dominos[b],dominos[a]

        # Empile les pioches
        for domino in dominos :
            self.__pioche.empiler(domino)
    

    def est_choisi_depart(self) :
        '''JeuMexicain -> boolean
        Teste si le domino de depart a été choisi'''
        return not self.__dominoDepart.est_vide()
    

    def dernier_domino(self) :
        '''JeuMexicain -> Domino
        Retourne le dernier domino, si le train est vide il retourne erreur'''
        assert not self.__trainMexicain.est_vide()
        return self.__trainMexicain.sommet()
    

    def pose_domino(self,domino) :
        '''JeuMexicain,Domino -> None
        Elle ajoute domino dans le train sachant que le domino est correct'''
        self.__trainMexicain.empiler(domino)
    

    def pioche(self) :
        '''JeuMexicain -> Domino
        Elle prend le sommet de la pile des dominos et retourne le domino'''
        return self.__pioche.depiler()
    

    def pioche_est_vide(self) :
        '''JeuMexicain -> boolean
        Teste si la pile des dominos est vide ou pas'''
        return self.__pioche.est_vide()
    

    def train_a_demarre(self) :
        '''JeuMexicain -> boolean
        Teste si il le train n'est pas vide (si il a demarre)'''
        return not self.__trainMexicain.est_vide()
    

    def domino_depart(self) :
        '''JeuMexicaon -> Domino
        Retourne le domino de depart du train mexicain'''
        return self.__dominoDepart
    

    def choisi_domino_depart(self,domino) :
        '''JeuMexicain,Domino -> None
        Ajoute le domino depart au jeu'''
        self.__dominoDepart = domino
    

    def str_dominos(self) :
        '''JeuMexicain -> list(str)
        Retourne une liste des strings des cinq premier dominos de la pile'''
        cpt = 0
        p1 = Pile()
        # Il met les elements du train dans une file en les comptants
        while not self.__trainMexicain.est_vide() and cpt < 5 :
            p1.empiler(self.__trainMexicain.depiler())
            cpt += 1
        # Il les remets dans le train en prenant leurs str
        liste_str = ["\t","\t","\t","\t","\t"]
        cpt = 0
        while not p1.est_vide() :
            domino = p1.depiler()
            liste_str[cpt] = domino.__str__()
            self.__trainMexicain.empiler(domino)
            cpt += 1
        return liste_str


    def img_dominos(self) :
        '''JeuMexicain -> list(tuple(int))
        Retourne une liste des coordonnées des images des cinq premier dominos de la pile'''
        cpt = 0
        p1 = Pile()
        # Il met les elements du train dans une file en les comptants
        while not self.__trainMexicain.est_vide() and cpt < 5 :
            p1.empiler(self.__trainMexicain.depiler())
            cpt += 1
        # Il les remets dans le train en prenant leurs coordonnées de images
        liste_img = [(-1,-1),(-1,-1),(-1,-1),(-1,-1),(-1,-1)]
        cpt = 0
        while not p1.est_vide() :
            domino = p1.depiler()
            liste_img[cpt] = domino.coord_image()
            self.__trainMexicain.empiler(domino)
            cpt += 1
        return liste_img


    def empile_pioche(self,domino) :
        '''JeuMexicain,Domino -> None
        Permet d'empiler un domino dans la pioche'''
        self.__pioche.empiler(domino)


    def recommencer(self) :
        '''JeuMexicain -> None
        Remet tous les dominos du train dans la pioche'''
        while not self.__trainMexicain.est_vide() :
            self.empile_pioche(self.__trainMexicain.depiler())
        self.empile_pioche(self.__dominoDepart)
        self.__dominoDepart = Domino(-1,-1)