
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename , askdirectory

import pandas as pd
from pandastable import Table, TableModel

from cleandata import *
from trainmodel import train
class job:
    def __init__(self,root):

        self.root = root


        self.x=1100
        self.y=750
        self.root.geometry('%sx%s'%(self.x,self.y))

        self.frame1=Frame(self.root,height=100,width=1100,bg='green')
        self.frame1.grid(row=0,column=0)
        self.frame1.grid_propagate(0)
        self.frame1.grid_rowconfigure(0,weight=1)

        
        self.frame2 = Frame(self.root, height=50, width=1100, bg='white')
        self.frame2.grid(row=1, column=0)
        self.frame2.grid_propagate(0)

        self.frame3 = Frame(self.root, height=600, width=1100, bg='gray')
        self.frame3.grid(row=2, column=0)
        self.frame3.grid_propagate(0)

        self.btraitement=Button(self.frame1,text='traitement',command=self.bclean)
        self.btraitement.grid(row=0, column=0,sticky=S)

        self.bentrainement = Button(self.frame1, text='entrainement',command=self.btrain)
        self.bentrainement.grid(row=0, column=1,sticky=S)

        self.bsimulation = Button(self.frame1, text='simulation',command=self.bsumilat)
        self.bsimulation.grid(row=0, column=2,sticky=S)

        self.bclassification = Button(self.frame1, text='classification',command=self.bclassi)
        self.bclassification.grid(row=0, column=3,sticky=S)
        self.list_dossier=[]



    # pour un mise a jour de frame 2 pour afficher les nouvelle boutton et effacer les ancians
    def update_frame2(self):
        self.frame2 = Frame(self.root, height=50, width=1100, bg='white')
        self.frame2.grid(row=1, column=0)
        self.frame2.grid_propagate(0)
        self.frame2.grid_rowconfigure(0, weight=1)
    def update_frame3(self):
        self.frame3 = Frame(self.root, height=600, width=1100, bg='gray')
        self.frame3.grid(row=2, column=0)
        self.frame3.grid_propagate(0)

    # afficher les boutton de partie de triatement les données qui déja scrapy
    def  bclean( self):
        self.update_frame2()
        self.btraitement.configure(bg="green")

        self.bimport_dossier1 = Button(self.frame2, text='import des données nigative',command=self.set_nigative)
        self.bimport_dossier1.grid(row=0, column=0, sticky=S)

        self.bimport_dossier2 = Button(self.frame2, text='import des données positive', command=self.set_positive)
        self.bimport_dossier2.grid(row=0, column=1, sticky=S)

        self.btraiter_dossier = Button(self.frame2, text='traiter et importer les données',command=self.set_clean)
        self.btraiter_dossier.grid(row=0, column=2, sticky=S)
    # pour afficher les boutton de partie de train
    def  btrain( self):
        self.update_frame2()

        self.bentrainement.configure(bg="green")
        self.bimport_data1 = Button(self.frame2, text="import data d'entrainement",command=self.set_data_train)
        self.bimport_data1.grid(row=0, column=0, sticky=S)

        self.bentrainer2= Button(self.frame2, text='entrainer',command=self.train1)
        self.bentrainer2.grid(row=0, column=1, sticky=S)

        self.btester = Button(self.frame2, text='tester',command=self.test)
        self.btester.grid(row=0, column=2, sticky=S)
    # pour afficher les boutton de partie de classification
    def  bclassi( self):
        self.update_frame2()


        self.bimport_data2 = Button(self.frame2, text="import data d'entrainement")
        self.bimport_data2.grid(row=0, column=0, sticky=S)

        self.bexport_data= Button(self.frame2, text='exporter')
        self.bexport_data.grid(row=0, column=1, sticky=S)


    # pou importer le dossier ou bien le winrar pour traiter a chaque commentaire

    def set_nigative(self):
        self.FILETYPES = [("all files", "*.*")]
        self.dir1 = askdirectory()
        self.chemin_nigative= self.dir1 + "/*"
        if self.dir1:
            self.bimport_dossier1.configure(bg='green')
    def set_positive(self):
        self.FILETYPES = [("all files", "*.*")]
        self.dir2= askdirectory()
        self.chemin_positive = self.dir2 + "/*"
        if self.dir2:
            self.bimport_dossier2.configure(bg='green')
    def set_clean(self):
        self.FILETYPES = [("all files", "*.*")]
        self.dir3=askdirectory()
        self.chemin_clean=self.dir3+"/*"
        #date_now = time.strftime('%d%m%Y')
        if self.dir1 and self.dir2 and self.dir3:
            # dans cette fonction il fais import la fonction de traitement que se triuve dans le fichier cleandata.py
            self.btraiter_dossier.configure(bg="green")
            mergeAllTweet([self.chemin_nigative,self.chemin_positive,self.chemin_clean])



    def set_data_train(self):
        self.FILETYPES = [("all files", "*.*")]
        self.dir4= askopenfilename()
        self.chemin_data_train = self.dir4
        if self.dir4:
            self.bimport_data1.configure(bg='green')
            data = pd.read_csv(self.chemin_data_train, encoding="ISO-8859-1", sep=',', names=["text", "result"])
            print(data)
            self.affiche_data(data)


    def train1(self):

        self.go=train()

        self.go.train_model(self.chemin_data_train)
        self.bentrainer2.configure(bg='green')



    def test(self):

        lresult = Label(self.frame3, text="",font=('arial',18))
        self.go.tester(lresult)
        self.btester.configure(bg="green")




    def bsumilat(self):
        self.update_frame2()
        self.update_frame3()
        self.bsimulate_import = Button(self.frame2, text="sumilation avec le model actual ",command=self.sumilat)
        self.bsimulate_import.grid(row=0, column=0, sticky=S)



        self.bsimulate_import = Button(self.frame2, text="import un model enregistré ")
        self.bsimulate_import.grid(row=0, column=1, sticky=S)


    def sumilat(self):
        self.i=0
        self.esimulate_actual = Entry(self.frame3,width=40)

        self.esimulate_actual.grid(row=0, column=0, sticky=S)

        def goo():
            self.i+=1

            self.go.simulation(str(self.esimulate_actual.get()), self.frame3,self.i)


        self.bsimulate_import = Button(self.frame3, text="publier",command=goo)
        self.bsimulate_import.grid(row=1, column=0, sticky=S)


    def affiche_data(self,data):

        f = Frame(self.frame3)
        f.grid(row=0, column=0)

        pt = Table(f, dataframe=data, height=600, width=1030)
        pt.show()




if __name__ == '__main__':
     root=Tk()
     job(root)
     root.mainloop()