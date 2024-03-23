import Joueur
import JeuMexicain
import Vue
from random import randint

class Contoleur :
    '''Classe permettant de jouer au jeu Mexicain'''
    def __init__(self,n=2) :
        '''Controleur,int -> Controleur
        Permet de jouer au jeu'''
        # Crée le jeu et les joueurs
        self.__jeu = JeuMexicain.JeuMexicain()
        self.__joueurs = list()
        for i in range(4) :
            self.__joueurs.append(Joueur.Joueur(self.__jeu))
        
        # Attribut boucle qui dit si le jeu est en boucle ou pas 
        self.__boucle = True
        # Attribut nombre de joueur humains
        if n > 4 : self.__nbre_humain = 4
        elif n <= 0 : self.__nbre_humain = 1
        else : self.__nbre_humain = n
        
        # Attribut tour qui permet de gerer le tour
        self.__tour = 0
        # Attribut pour les joueurs open (dico)
        self.__opened = dict()

        # Crée la vue
        self.__vue = Vue.VueTrain(self.__jeu,self.__joueurs)
        
        # Sauvegarde les boutons
        les_boutons = self.__vue.les_boutons()
        self.__btn_go = les_boutons[0]
        self.__btn_piocher = les_boutons[1]
        self.__btns_reserve = les_boutons[2]
        self.__btns_choix = les_boutons[3]
        
        # Partage les dominos
        self.partage_domino()

        # Choisi le domino de depart
        self.choisi_domino_depart()

        # Met aux boutons la commandes liée au joueur qui va jouer
        self.met_commande_a_jour(self.__tour)

        # met à jour les joueurs open
        self.met_a_jour_open()
        
        # Met à jour l'affichage du joueur humain qui va jouer
        self.__vue.met_a_jour_affichage(self.__tour)

        self.__vue.fen().mainloop()    


    def partage_domino(self) :
        '''Controleur -> None
        Partage les dominos aux joueurs'''
        # Chaque joueur pioche 10 fois
        for i in range(10) :
            for j in range(4) :
                self.__joueurs[j].pioche()
    

    def choisi_domino_depart(self) :
        '''Controleur -> None
        Appelle la fonction du modele à chaque tour de joueur qui choisi 
        un domino au hasard dans la reserve'''
        # Permet de voir le joueur qui choisi le domino de depart
        self.__tour = randint(0,3)
        # Tant que il n'a pas trouvé le domino depart
        while not self.__jeu.est_choisi_depart() :
            self.__joueurs[self.__tour].donner_domino_depart()
            # Passe au joueur suivant
            self.__tour = (self.__tour+1) % 4
        # Le premier joueur est choisi parmi les joueurs humains
        self.__tour = self.__tour % self.__nbre_humain
    

    def met_commande_a_jour(self,num_joueur) :
        '''Controleur,int -> None
        Met les commandes des differents boutons à jour'''
        # Bouton Go et Piocher
        self.__btn_go.config(command=self.controle_GO(num_joueur))
        self.__btn_piocher.config(command=self.controle_pioche(num_joueur))
        
        # Commande double clic
        for ind in range(len(self.__btns_reserve)) :
            self.__btns_reserve[ind].bind("<Double-Button-1>",self.double_clic(ind,num_joueur))
    

    def met_a_jour_open(self) :
        '''Controleur -> None
        Met à jour les joueurs ouverts'''
        # Les joueurs open à jour
        self.__opened.clear()
        for i in range(len(self.__joueurs)) :
            if self.__joueurs[i].est_open() :
                self.__opened[i] = self.__joueurs[i] 
    

    def controle_GO(self,num_joueur) :
        '''Controleur,int -> fonction'''
        def ctrlGo() :
            '''None -> None
            Affiche le domino depart, rend visible les dominos posables 
            et leurs met leurs commandes'''
            # Affiche le domino depart
            self.__vue.affiche_btn_depart()
            
            # Prend les indices des dominos posables sur les trains
            ind_btns = self.__joueurs[num_joueur].dominos_posables(self.__opened)

            # Si il n'y a pas de domino posable, il demande au joueur de piocher
            if len(ind_btns) == 0 :
                self.__btn_piocher.config(state="normal")
                self.__btn_go.config(state="disable")
            # Si non, pour chaque indice 
            for ind in ind_btns :

                # Il rend visible le bouton et lui met sa commande
                self.__btns_reserve[ind].config(relief="raised",command=self.controle_reserve(ind,num_joueur))
                # Met aussi le bouton GO à disable pour obliger le joueur à cliquer le domino
                self.__btn_go.config(state="disable")
        
        return ctrlGo


    def controle_reserve(self,ind,num_joueur) :
        '''Controleur,int,int -> fonction'''
        def ctrlReserve() :
            '''None -> None
            Enleve les commandes des boutons de la reserve, il rend visible les boutons
            de choix de train et leur met leur commandes'''
            # Le jeu n'est plus en boucle
            self.__boucle = False
            
            # Enleve la commande de tous les boutons choix
            for btn in self.__btns_choix :
                # Il les rend invisibles
                btn.config(relief="flat",command=self.rien)
            
            # Prend les indices des dominos posables pour rendre invisible sauf celui de ind
            ind_btns = self.__joueurs[num_joueur].dominos_posables(self.__opened)
            for i in ind_btns :
                if i != ind :
                    self.__btns_reserve[i].config(relief="flat")
                else :
                    self.__btns_reserve[i].config(relief="raised")
                
            # Prends le domino
            domino = self.__joueurs[num_joueur].nieme_domino(ind+1)
            # Il regarde si il est posable sur le train mexicain
            if self.__joueurs[num_joueur].possible_train_mexicain(domino) :
                self.__btns_choix[0].config(relief="raised",command=self.controle_train(ind,num_joueur,0))
            # Ou sur le train du joueur
            if self.__joueurs[num_joueur].possible_train(domino):
                self.__btns_choix[num_joueur+1].config(relief="raised",command=self.controle_train(ind,num_joueur,num_joueur+1))
            # Ou sur le train des joueurs ouverts
            for num,joueur in self.__opened.items() :
                if joueur.possible_train(domino) :
                    self.__btns_choix[num+1].config(relief="raised",command=self.controle_train(ind,num_joueur,num+1))

        return ctrlReserve
    
    def rien(self) :
        return
    

    def controle_train(self,ind,num_joueur,train) :
        '''Controle,int,int,bool -> fct'''
        def ctrlTrain() :
            '''None -> None
            Permet de poser le domino sur le train correspondant en verifiant si il est posable'''
            # Il verifie si le domino est valide c'est à dire si ce n'est pas son inverse qu'on veut
            if self.__vue.valide_domino(ind,num_joueur,train) :
                # Prend les indices des dominos posables pour enlever les commandes
                ind_btns = self.__joueurs[num_joueur].dominos_posables(self.__opened)
                for i in ind_btns :
                    # Il les rend invisibles
                    self.__btns_reserve[i].config(relief="flat",command=self.rien)

                # Prends le domino
                domino = self.__joueurs[num_joueur].nieme_domino(ind+1)
                # Il regarde si il est posable sur le train mexicain
                if train == 0 :
                    self.__joueurs[num_joueur].pose_domino_train_mexicain(domino)
                # Si non il pose sur le train du joueur correspondant
                else :
                    self.__joueurs[train-1].pose_domino_train(domino)

                # Enleve la commande de tous les boutons choix
                for btn in self.__btns_choix :
                    # Il les rend invisibles
                    btn.config(relief="flat",command=self.rien)
                
                # Bouton go à normal
                self.__btn_go.config(state="normal")
                
                # Supprime le domino
                self.__joueurs[num_joueur].supprimer_domino(ind)

                # Verifie si le joueur a gagné
                if self.__joueurs[num_joueur].a_gagne() : self.jeu_fini(num_joueur)
                
                # Si non
                else :
                    # On vérifie si il a mis un domino double (si oui il joue encore, sinon le prochain joueur joue)
                    if not domino.estDouble() :
                        # il met à jour les joueurs open
                        self.met_a_jour_open()
                        # Si c'est au tour des joueurs artificiels de jouer
                        if self.__tour == self.__nbre_humain -1 :
                            # Elle les fait jouer
                            for i in range(self.__nbre_humain,4) :
                                self.__joueurs[i].jouer(self.__opened)
                                # Si le joueur a gagné le jeu s'arrete
                                if self.__joueurs[i].a_gagne() :
                                    self.jeu_fini(i)
                                    return
                                self.met_a_jour_open()
                            self.__boucle = True
                        # Met le tour à jour
                        self.__tour = (self.__tour+1) % self.__nbre_humain
                    # met à jour l'affichage
                    self.__vue.met_a_jour_affichage(self.__tour)
                    # Met aux boutons la commandes liée au joueur qui va jouer
                    self.met_commande_a_jour(self.__tour)
        
        return ctrlTrain
    

    def controle_pioche(self,num_joueur) :
        '''Controleur,Joueur -> fonction'''
        def ctrlPioche() :
            '''None -> None
            Permet au joueur de piocher dans la pioche'''
            # Pour verifier si le jeu est en boucle
            self.__boucle = self.__boucle and True

            # Pioche
            self.__joueurs[num_joueur].pioche()

            # Remet les boutons à leurs formes
            self.__btn_go.config(state="normal")
            self.__btn_piocher.config(state="disabled")

            # met à jour les joueurs open
            self.met_a_jour_open()

            # Si c'est au tour des joueurs artificiels de jouer
            if self.__tour == self.__nbre_humain -1 :
                # Elle les fait jouer
                for i in range(self.__nbre_humain,4) :
                    # En verifiant si le joueur a pioché ou pas
                    self.__boucle = self.__boucle and self.__joueurs[i].jouer(self.__opened)
                    # Si le joueur a gagné le jeu s'arrete
                    if self.__joueurs[i].a_gagne() :
                        self.jeu_fini(i)
                        return
                    self.met_a_jour_open()
                # Il verifie si le jeu n'est pas en boucle, Si oui il arrete le jeu
                if self.__boucle and self.__jeu.pioche_est_vide() :
                    self.jeu_fini(-1)
                    return
                self.__boucle = True
            # Met le tour à jour
            self.__tour = (self.__tour+1) % self.__nbre_humain
            # met à jour l'affichage
            self.__vue.met_a_jour_affichage(self.__tour)
            # Met aux boutons la commandes liée au joueur qui va jouer
            self.met_commande_a_jour(self.__tour)
        
        return ctrlPioche
    

    def double_clic(self,ind,num_joueur) :
        '''VueTrain,int -> fct'''
        def ctrlDC(event) :
            '''None -> None
            Gère le double clic'''
            # Permute le domino à l'indice ind
            self.__joueurs[num_joueur].permuter(ind)
            self.__vue.met_a_jour_reserve(num_joueur)
        
        return ctrlDC


    def jeu_fini(self,gagnant) :
        '''Controleur,int -> None
        Permet de declarer le joueur gagnant et de cloturer le jeu'''
        # Dit à la vue de desactiver que le jeu est fini
        self.__vue.jeu_fini(gagnant)

        # Remet la commande du bouton Go à recommencer
        self.__btn_go.config(command=self.recommencer)


    def recommencer(self) :
        '''Controleur -> None
        Permet de recommencer le jeu en demandant aux joueurs de remettre les dominos dans la pioche'''
        # Les joueurs remettent leurs domino dans la pioche
        self.__jeu.recommencer()
        self.__joueurs[0].recommencer()
        self.__joueurs[1].recommencer()
        self.__joueurs[2].recommencer()
        self.__joueurs[3].recommencer()

        # La vue aussi recommence
        self.__vue.recommencer()

        # Partage les dominos
        self.partage_domino()

        # Choisi le domino de depart
        self.choisi_domino_depart()

        # met à jour les joueurs open
        self.met_a_jour_open()

        # Remet le bouton Go comme avant
        self.__btn_go.config(text="Go !",command=self.controle_GO(self.__tour))
        
        # Met à jour l'affichage
        self.__vue.met_a_jour_affichage(self.__tour)
        self.__boucle = True



if __name__ == '__main__' :
    Jeu = Contoleur(2)
