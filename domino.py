
class Domino :
    '''Classe permettant de creer des objets simulant les pièces d'un jeu de domino'''
    def __init__(self,face_a = 0,face_b = 0) :
        '''Domino,int,int -> Domino
        Permet de créer une pièce de domino à partir du face_a et face_b'''
        self.__A = face_a
        self.__B = face_b
        
    def valeur(self) :
        '''Domino -> int
        Renvoie la somme des deux face du domino'''
        return self.__A + self.__B
    
    def __str__(self) :
        '''Domino -> str
        Retourne une chaine de caractère avec les points présents sur les deux faces'''
        msg = "["
        if self.__A < 10 : msg += "0"     # Pour completer avec un 0
        msg += str(self.__A) + " | "
        if self.__B < 10 : msg += "0"
        msg += str(self.__B)
        msg += "]"
        return msg
    
    def coord_image(self) :
        '''Domino -> tuple(int)
        Retourne les coordonnées de l'image correspondant au domino ie les numero des faces'''
        return (self.__A,self.__B)
    
    def possible_apres(self,do) :
        '''Domino,Domino -> bool
        Vérifie si la face B du domino courant a le meme valeur que la face A ou que la face B du domino do'''
        return self.__B == do.__B or self.__A == do.__B
    
    def estDouble(self) :
        '''Domino -> boolean
        Teste si un domino est un double ou pas'''
        return self.__A == self.__B
    
    def peutEtrePlaceApres(self,domino) :
        '''Domino -> boolean
        Teste si on peut placer le domino self à coter de domino'''
        return self.__A == domino.__B
    
    def permuter(self) :
        '''Domino -> None
        renverse le domino c'est à dire que sa face A devient sa face B et vice-versa'''
        self.__A,self.__B = self.__B,self.__A
    
    def est_vide(self) :
        '''Domino -> boolean
        teste si ce domino est vide ou pas ie face A = -1 et face B = -1'''
        return self.__A == -1 and self.__B == -1
    
    