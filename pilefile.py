class Pile :
    '''Definition d'une pile - structure de données LIFO (Last In First Out)
    '''

    def __init__(self) : 
        '''Pile -> Pile
        construit une pile vide
        '''
        # basée sur une pile
        self.__les_elts = list()
        
    
    def empiler(self,elt) :
        '''(modif) Pile, Objet -> Rien
        ajoute un élément au sommet de la pile.
        '''
        self.__les_elts.append(elt)
            
    def est_vide(self) : 
        '''Pile -> Boolean
        teste si la pile est vide. '''
        return len(self.__les_elts) == 0
  
    def sommet(self) : 
        '''Pile -> Objet
        retourne l'élément au sommet de la pile.
        '''
        assert not self.est_vide()
        return self.__les_elts[-1] 
        
    def depiler(self) : 
        '''(modif) Pile -> Objet
        enlève l'élément au sommet de la pile.
        ''' 
        assert not self.est_vide()
        elt = self.__les_elts[-1] 
        del(self.__les_elts[-1])
        return elt

# fin de la classe Pile

class File : 
  "Modélise une structure de données FIFO (First In First Out)"

  def __init__(self) :
    '''File -> File
    construite une file vide.'''
    # basée sur une liste
    self.__les_elts = list()

  def est_vide(self) : 
    '''File -> Boolean
    teste si la file est vide.
    '''
    return len(self.__les_elts) == 0

  def ajouter(self, elt) :
    '''(modif) File, Objet -> Rien
    ajoute une élément à la file.
    '''
    self.__les_elts.append(elt)

  def enlever(self) :
    '''(modif) File -> Objet
    enlève le premier élément de la file.
    '''
    assert not self.est_vide()
    elt = self.__les_elts[0]
    del(self.__les_elts[0])
    return elt

  def sommet(self) :
    '''File -> Objet
    retourne le premier élément de la file.
    '''
    assert not self.est_vide()
    return self.__les_elts[0]

  def __str__(self) :
      '''File -> str
      uniquement poour tricher à la bataille (ou ailleurs)
      '''
      txt = 'FIFO ('+str(len(self.__les_elts))+' elts) : '
      for elt in self.__les_elts :
          txt += str(elt)+' - '
      return txt


# fin de la classe File    

