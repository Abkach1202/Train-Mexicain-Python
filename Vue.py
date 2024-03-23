import tkinter

class VueTrain :
    '''Classe permettant de faire l'affichage du jeu de Train maxicain'''
    def __init__(self,jeu,joueurs) : 
        '''VueTrain,JeuMexicain,list(Joueur) -> VueTrain
        Permet de creer la fenetre et tous les autres composants de l'affichage'''
        # Fenetre et son titre
        self.__fen = tkinter.Tk()
        self.__fen.title("Jeu du Train Mexicain")

        # Le modele du jeu et les joueurs
        self.__jeu = jeu
        self.__joueurs = joueurs

        # Création des images
        self.__images = list()
        for i in range(13) :
            self.__images.append(list())
            for j in range(13) :
                img = tkinter.PhotoImage(file=f"Images/petit-{i}-{j}.gif")
                self.__images[i].append(img)
        # Image du domino vide
        img = tkinter.PhotoImage(file=f"Images/petit--1--1.gif")
        self.__images.append([img])
        
        # Frame pour la premiere ligne
        frame1 = tkinter.Frame(self.__fen)
        frame1.pack()
        # Frame pour les trains
        frame2 = tkinter.Frame(self.__fen)
        frame2.pack()
        # Frame pour la reserve
        self.__frame3 = tkinter.Frame(self.__fen)
        self.__frame3.pack()
        # Frame pour le bouton Go
        frame4 = tkinter.Frame(self.__fen)
        frame4.pack()

        # Labels domino depart
        label0 = tkinter.Label(frame1,text="Jeu des dominos mexicains - Domino de départ : ")
        label0.pack(side="left")

        # Bouton pour choisir dans quel trains mettre
        self.__btns_choix = []
        for i in range(5) :
            if i == 0 :
                btn = tkinter.Button(frame2,text="Train Mexicain",relief="flat")
                self.__btns_choix.append(btn)
                btn.grid(row=i,column=0)
            else :
                btn = tkinter.Button(frame2,text=f"Joueur {i}",relief="flat")
                self.__btns_choix.append(btn)
                btn.grid(row=i,column=0)

        # Le reste des labels
        self.__label6 = tkinter.Label(self.__frame3)
        self.__label6.grid(row=0,column=0,columnspan=5)
        self.__label7 = tkinter.Label(frame4)
        self.__label7.grid(row=0,column=0)

        # Bouton Départ
        self.__btn_depart = tkinter.Button(frame1,relief="flat",image=self.__images[-1][-1])
        self.__btn_depart.pack(side="right")

        # Bouton train
        self.__btns_train = []
        for i in range(5) :
            self.__btns_train.append(list())
            for j in range(5) :
                btn = tkinter.Button(frame2,relief="flat")
                self.__btns_train[i].append(btn)
                btn.grid(row=i,column=j+1)
        
        # Boutons reserve que l'on va créer ulterieurement
        self.__btns_reserve = []
        for i in range(3) :
            for j in range(5) :
                btn = tkinter.Button(self.__frame3,relief="flat")
                self.__btns_reserve.append(btn)
                btn.grid(row=i+1,column=j)

        # Bouton Go
        self.__btn_go = tkinter.Button(frame4,text="Go !")
        self.__btn_go.grid(row=0,column=1)
        
        # Bouton Piocher pour piocher
        self.__btn_piocher = tkinter.Button(frame4,text="Piocher",state="disabled")
        self.__btn_piocher.grid(row=0,column=2)

    
    def affiche_btn_depart(self) :
        '''VueTrain -> None
        Affiche le bouton depart'''
        # Prend les coordonnées de l'image
        coord = self.__jeu.domino_depart().coord_image()
        
        # Affiche l'image sur le bouton
        self.__btn_depart.config(image=self.__images[coord[0]][coord[1]])


    def les_boutons(self) :
        '''VueTrain -> list(Button)
        Renvoie les boutons afin que le controleur les utilise'''
        return (self.__btn_go,self.__btn_piocher,self.__btns_reserve,self.__btns_choix)
    

    def fen(self) :
        '''VueTrain -> Tk
        Retourne la fenetre'''
        return self.__fen

    
    def valide_domino(self,ind,num_joueur,train) :
        '''VueTrain,int,int,int -> None
        Permet de valider si le domino est posable sur le train, si non il dit qu'il faut le permuter et retourne False'''
        # Prends le domino
        domino = self.__joueurs[num_joueur].nieme_domino(ind+1)
        # Regarde si on pose sur le train mexicain
        if train == 0 and not self.__joueurs[num_joueur].est_posable_train_mexicain(domino) :
            self.__btns_reserve[ind].config(relief="raised")
            self.__label7.config(text="Permuter le domino d'abord !!")
            return False
        # Si non c'est le train du joueur
        if train != 0 and not self.__joueurs[train-1].est_posable_train(domino) :
            self.__btns_reserve[ind].config(relief="raised")
            self.__label7.config(text="Permuter le domino d'abord !!")
            return False
        return True
        

    def met_a_jour_affichage(self,num_joueur) :
        '''VueTrain,int -> None
        Met à jour l'affichage en affichant les differents boutons avec leurs valeurs de domino'''
        # Met à jour les boutons des trains
        self.met_a_jour_train_mexicain()
        self.met_a_jour_trains(1)
        self.met_a_jour_trains(2)
        self.met_a_jour_trains(3)
        self.met_a_jour_trains(4)

        # Met à jour les boutons de la reserve
        self.met_a_jour_reserve(num_joueur)

        # Met à jour le label7 et le label6
        if self.__jeu.pioche_est_vide() :
            self.__label7.config(text=f"Pioche vide !!!\t\tJoueur {num_joueur+1}")
        else :
            self.__label7.config(text=f"Pioche non vide\t\tJoueur {num_joueur+1}")


    def met_a_jour_train_mexicain(self) :
        '''VueTrain,ind -> None
        Met à jour l'affichage du train mexicain'''
        # Met à jour les boutons du train en recuperant les images des 5 dernier dominos 
        liste_str = self.__jeu.img_dominos()
        # Il met les images sur les boutons correspondant
        for i in range(5) :
            coord = liste_str[i]
            self.__btns_train[0][i].config(image=self.__images[coord[0]][coord[1]])


    def met_a_jour_trains(self,ind) :
        '''VueTrain,ind -> None
        Met à jour l'affichage du train de joueur à la position ind'''
        # Met à jour les boutons du train en recuperant les images des 5 dernier dominos 
        liste_str = self.__joueurs[ind-1].img_dominos()
        # Il met les images sur les boutons correspondant
        for i in range(5) :
            coord = liste_str[i]
            self.__btns_train[ind][i].config(image=self.__images[coord[0]][coord[1]])


    def met_a_jour_reserve(self,num_joueur) :
        '''VueTrain -> None
        Met à jour l'affichage de la reserve du joueur'''
        # Met à jour le nom de la reserve
        self.__label6.config(text=f"Reserve du Joueur {num_joueur+1}")
        # Prend le nombre de domino dans la reserve et le nombre de bouton
        len_res = self.__joueurs[num_joueur].nbre_domino_reserve()
        len_btn = len(self.__btns_reserve)

        # Gère le debordement
        if len_res > len_btn :
            for i in range(len_res-len_btn) :
                btn = tkinter.Button(self.__frame3,relief="flat")
                btn.grid(row=((len_btn+i)//5)+1,column=(len_btn+i)%5)
                self.__btns_reserve.append(btn)    
        
        # Parcours les boutons pour leur mettre le texte correspondant
        for i in range(len(self.__btns_reserve)) :
            
            # Si il reste des domino à afficher
            if i < len_res :
                # Il prend le domino à la ième position
                ieme_domino = self.__joueurs[num_joueur].nieme_domino(i+1)
                # Prend les coordonnées de l'image
                coord = ieme_domino.coord_image()
                # met l'image sur le bouton lui correspondant
                self.__btns_reserve[i].config(image=self.__images[coord[0]][coord[1]])
            
            # Si non il met l'image du vide met du blanc
            else :
                coord = (-1,-1)
                self.__btns_reserve[i].config(image=self.__images[coord[0]][coord[1]])
    
    
    def jeu_fini(self,gagnant) :
        '''VueTrain,int -> None
        Permet de gerer la fin du jeu en declarant le gagnant, en desactivant les boutons de la reserve et en transformant
        le bouton GO à Recommencer'''

        # Change le label7 pour declarer le gagnant ou pour dire si le jeu est en boucle
        if gagnant != -1 :
            self.__label7.config(text=f"Joueur {gagnant+1} a gagné !!!\t\tBravo, Bravo")
            # Met à jour le train du gagnant et le train mexicain
            self.met_a_jour_train_mexicain()
            self.met_a_jour_trains(gagnant+1)
            self.met_a_jour_reserve(gagnant)
        else :
            self.__label7.config(text="Match nul !\tJeu en boucle")

        # Desactive les boutons de la reserve
        for btn in self.__btns_reserve :
            btn.config(state="disabled")

        # Bouton Go deviens Recommencer pour pouvoir recommencer
        self.__btn_go.config(text="Recommencer ?")
    

    def recommencer(self) :
        '''VueTrain -> None
        Permet de recommencer le jeu en remettant les bouton de la reserve'''
        # Remet les boutons à la normal et detruit les surplus de boutons        
        for i in range(len(self.__btns_reserve)) :
            if i >= 15 :
                self.__btns_reserve[i].destroy()
            else :
                self.__btns_reserve[i].config(state="normal")
        
        # Supprime les boutons detruits
        while len(self.__btns_reserve) > 15 :
            del(self.__btns_reserve[15])

        # Remet le bouton depart à vide
        self.__btn_depart.config(image=self.__images[-1][-1])


