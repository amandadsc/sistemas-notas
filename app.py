"""
Criado em 13 de Junho de 2021

@author: Amanda Dias / amandadsc
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import tkinter.messagebox as msb
import sqlite3

root = Tk()
root.title("Bem vindo(a) ao nosso programa de gerenciamento de notas")
width = 1200
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.iconbitmap("img/grade.ico")
root.config(bg="#0B0A07")


materia = StringVar()
professor = StringVar()
dia = StringVar()
horario = StringVar()
campus = StringVar()
av1 = StringVar()
av2 = StringVar()
av3 = StringVar()
avd = StringVar()
avds = StringVar()
media = StringVar()
id = None
updateWindow = None
newWindow = None


def calculaMedia(av1, av2, av3, avd, avds):
    try:
        if (av3 <= av2) and (av3 <= av1) and (avds <= avd):
            nf = (av1 + av2 + avd) / 3
        elif (av3 <= av1) and (av3 > av2) and (avds <= avd):
            nf = (av1 + av3 + avd) / 3
        elif (av3 <= av2) and (av3 > av1) and (avds <= avd):
            nf = (av2 + av3 + avd) / 3
        elif (av3 <= av1) and (av3 <= av2) and (avds > avd):
            nf = (av1 + av2 + avds) / 3 
        elif (av3 <= av1) and (av3 > av2) and (avds > avd):
            nf = (av1 + av3 + avds) / 3
        elif (av3 > av1) and (av3 <= av2) and (avds > avd):
            nf = (av2 + av3 + avds) / 3
        elif (av3 >= av1) and (av3 >= av2) and (avds > avd) and (av2 < av1):
            nf = (av3 + av1 + avds) / 3
        elif (av3 >= av1) and (av3 >= av2) and (avds <= avd) and (av2 < av1):
            nf = (av3 + av1 + avd) / 3
        elif (av3 >= av1) and (av3 >= av2) and (avds > avd) and (av2 > av1):
            nf = (av3 + av2 + avds) / 3
        elif (av3 >= av1) and (av3 >= av2) and (avds <= avd) and (av2 > av1):
            nf = (av3 + av2 + avd) / 3
        return round(nf, 2)
    except Exception as ex:
        print('ERRO: Não foi possível calcular a media.', ex)

def database():
    try:
        conn = sqlite3.connect("notas.db")
        cursor = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS 'notas' (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                materia TEXT NOT NULL, professor TEXT, dia TEXT, horario TEXT, campus TEXT, av1 REAL NOT NULL, av2 REAL NOT NULL, av3 REAL,
                avd REAL NOT NULL, avds REAL, media REAL) """
        cursor.execute(query)
    except sqlite3.Error as e:
        print('ERRO: Falha ao criar banco/tabela.', e)
    else:
        try:
            cursor.execute("SELECT * FROM 'notas' ORDER BY 'materia' ASC")
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
        except Exception as ex:
            print('ERRO: Falha ao inserir dados na árvore.', ex)
    finally:
        cursor.close()
        conn.close()

def submitData():
    if materia.get() == "":
        resultado = msb.showwarning("", "Por favor, digite qual a matéria.", icon="warning")
    elif (av1.get() == "") and (av2.get() == ""):
        resultado = msb.showwarning("", "Por favor, informe pelo menos a av1 ou av2.", icon="warning")
    elif (avd.get() == "") and (avds.get() == ""):
        resultado = msb.showwarning("", "Por favor, informe pelo menos a avd ou avds.", icon="warning")
    elif (type(materia) is str == False):
        resultado = msb.showwarning("", "Por favor, informe um nome de matéria válido.", icon="warning")
    elif (professor != "") and (type(professor) is str == False):
        resultado = msb.showwarning("", "Por favor, informe um nome de professor válido.", icon="warning")
    elif (campus != "") and (type(campus) is str == False):
        resultado = msb.showwarning("", "Por favor, informe um nome de campus válido.", icon="warning")
    else:
        if av1.get() == "":
            av1.set(0)
        if av2.get() == "":
            av2.set(0)
        if av3.get() == "":
            av3.set(0)
        if avd.get() == "":
            avd.set(0)
        if avds.get() == "":
            avds.set(0)
        try:
            media = calculaMedia(float(av1.get()), float(av2.get()), float(av3.get()), float(avd.get()), float(avds.get()))
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("notas.db")
            cursor = conn.cursor()
            query = """INSERT INTO 'notas' (materia, professor, dia, horario, campus, av1, av2, av3, avd, avds, media) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, (str(materia.get()), str(professor.get()), str(dia.get()), str(horario.get()), str(campus.get()), 
                    str(av1.get()), str(av2.get()), str(av3.get()), str(avd.get()), str(avds.get()), str(media)))
            conn.commit()
        except sqlite3.Error as e:
            print('ERRO: Falha ao inserir dados no banco.', e)
        else:
            try:
                cursor.execute("SELECT * FROM 'notas' ORDER BY 'materia' ASC")
                fetch = cursor.fetchall()
                for data in fetch:
                    tree.insert('', 'end', values=(data))
            except Exception as ex:
                print('ERRO: Falha ao inserir dados na árvore.', ex)
        finally:
            cursor.close()
            conn.close()
            materia.set("")
            professor.set("")
            dia.set("")
            horario.set("")
            campus.set("")
            av1.set("")
            av2.set("")
            av3.set("")
            avd.set("")
            avds.set("")

def updateData():
    try:
        media = calculaMedia(float(av1.get()), float(av2.get()), float(av3.get()), float(avd.get()), float(avds.get()))
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("notas.db")
        cursor = conn.cursor()
        query = """UPDATE 'notas' SET materia = ?, professor = ?, dia = ?, horario = ?, campus = ?, av1 = ?, av2 = ?, 
                av3 = ?, avd = ?, avds = ?, media = ? WHERE id = ?"""
        cursor.execute(query, (str(materia.get()), str(professor.get()), str(dia.get()), 
                str(horario.get()), str(campus.get()), str(av1.get()), str(av2.get()), str(av3.get()), str(avd.get()), str(avds.get()), str(media), int(id)))
        conn.commit()
    except sqlite3.Error as e:
        print('ERRO: Falha ao atualizar dados no banco.', e)
    else:
        try:
            cursor.execute("SELECT * FROM 'notas' ORDER BY 'materia' ASC")
            fetch = cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
        except Exception as ex:
                print('ERRO: Falha ao atualizar dados na árvore.', ex)
    finally:
        cursor.close()
        conn.close()
        materia.set("")
        professor.set("")
        dia.set("")
        horario.set("")
        campus.set("")
        av1.set("")
        av2.set("")
        av3.set("")
        avd.set("")
        avds.set("")

def deleteData():
    if not tree.selection():
        resultado = msb.showwarning(
            "", "Por favor, selecione a materia a ser deletada.", icon="warning")
    else:
        resultado = msb.askquestion("", "Tem certeza que deseja deletar a matéria selecionada?")
        if resultado == 'yes':
            selectItem = tree.focus()
            contents = (tree.item(selectItem))
            selectedItem = contents['values']
            id = selectedItem[0]
            tree.delete(selectItem)
            try:
                conn = sqlite3.connect("notas.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM 'notas' WHERE id = %d" % selectedItem[0])
                conn.commit()
            except sqlite3.Error as e:
                print('ERRO: Falha ao excluir dados no banco.', e)
            finally:
                cursor.close()
                conn.close()


def onSelect(event):
    global id, updateWindow
    selectItem = tree.focus()
    contents = (tree.item(selectItem))
    selectedItem = contents['values']
    id = selectedItem[0]
    materia.set("")
    professor.set("")
    dia.set("")
    horario.set("")
    campus.set("")
    av1.set("")
    av2.set("")
    av3.set("")
    avd.set("")
    avds.set("")
    materia.set(selectedItem[1])
    professor.set(selectedItem[2])
    dia.set(selectedItem[3])
    horario.set(selectedItem[4])
    campus.set(selectedItem[5])
    av1.set(selectedItem[6])
    av2.set(selectedItem[7])
    av3.set(selectedItem[8])
    avd.set(selectedItem[9])
    avds.set(selectedItem[10])
    media.set(selectedItem[11])
    
    
# --------------- FRAMES - ATUALIZAR --------------
    updateWindow = Toplevel()
    updateWindow.title("SISTEMA DE GERENCIAMENTO DE NOTAS")
    FormTitle = Frame(updateWindow)
    FormTitle.pack(side=TOP)
    formContact = Frame(updateWindow)
    formContact.pack(side=TOP, pady=10)
    width = 400
    height = 400
    screen_width = updateWindow.winfo_screenwidth()
    screen_height = updateWindow.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    updateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    updateWindow.resizable(0, 0)

# --------------- LABELS - ATUALIZAR --------------
    lbl_title = Label(FormTitle, text="Atualizando nota", font=('Courier New', 18), bg='#E3D87E', width=300)
    lbl_title.pack(fill=X)
    lbl_materia = Label(formContact, text='Matéria:', font=('arial', 14))
    lbl_materia.grid(row=0, sticky=W)
    lbl_professor = Label(formContact, text='Professor(a):', font=('arial', 14))
    lbl_professor.grid(row=1, sticky=W)
    lbl_dia = Label(formContact, text='Dia:', font=('arial', 14))
    lbl_dia.grid(row=2, sticky=W)
    lbl_horario = Label(formContact, text='Horário:', font=('arial', 14))
    lbl_horario.grid(row=3, sticky=W)
    lbl_campus = Label(formContact, text='Campus:', font=('arial', 14))
    lbl_campus.grid(row=4, sticky=W)
    lbl_av1 = Label(formContact, text='AV1:', font=('arial', 14))
    lbl_av1.grid(row=5, sticky=W)
    lbl_av2 = Label(formContact, text='AV2:', font=('arial', 14))
    lbl_av2.grid(row=6, sticky=W)
    lbl_av3 = Label(formContact, text='AV3:', font=('arial', 14))
    lbl_av3.grid(row=7, sticky=W)
    lbl_avd = Label(formContact, text='AVD:', font=('arial', 14))
    lbl_avd.grid(row=8, sticky=W)
    lbl_avds = Label(formContact, text='AVDS:', font=('arial', 14))
    lbl_avds.grid(row=9, sticky=W)

# --------------- ENTRIES - ATUALIZAR --------------
    materiaEntry = Entry(formContact, textvariable=materia, font=('arial', 11))
    materiaEntry.grid(row=0, column=1)
    professorEntry = Entry(formContact, textvariable=professor, font=('arial', 11))
    professorEntry.grid(row=1, column=1)
    diaEntry = Entry(formContact, textvariable=dia, font=('arial', 11))
    diaEntry.grid(row=2, column=1)
    horarioEntry = Entry(formContact, textvariable=horario, font=('arial', 11))
    horarioEntry.grid(row=3, column=1)
    campusEntry = Entry(formContact, textvariable=campus, font=('arial', 11))
    campusEntry.grid(row=4, column=1)
    av1Entry = Entry(formContact, textvariable=av1, font=('arial', 11))
    av1Entry.grid(row=5, column=1)
    av2Entry = Entry(formContact, textvariable=av2, font=('arial', 11))
    av2Entry.grid(row=6, column=1)
    av3Entry = Entry(formContact, textvariable=av3, font=('arial', 11))
    av3Entry.grid(row=7, column=1)
    avdEntry = Entry(formContact, textvariable=avd, font=('arial', 11))
    avdEntry.grid(row=8, column=1)
    avdsEntry = Entry(formContact, textvariable=avds, font=('arial', 11))
    avdsEntry.grid(row=9, column=1)

# --------------- BOTÃO - ATUALIZAR --------------
    btn_updatecom = Button(formContact, text="Atualizar",width=50, command=updateData)
    btn_updatecom.grid(row=11, columnspan=2, pady=10)

def addData():
    global newWindow
    materia.set("")
    professor.set("")
    dia.set("")
    horario.set("")
    campus.set("")
    av1.set("")
    av2.set("")
    av3.set("")
    avd.set("")
    avds.set("")
    

# --------------- FRAMES - INCLUIR --------------
    newWindow = Toplevel()
    newWindow.title("SISTEMA DE GERENCIAMENTO DE NOTAS")
    FormTitle = Frame(newWindow)
    FormTitle.pack(side=TOP)
    formContact = Frame(newWindow)
    formContact.pack(side=TOP, pady=10)
    width = 400
    height = 400
    screen_width = newWindow.winfo_screenwidth()
    screen_height = newWindow.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    newWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    newWindow.resizable(0, 0)

# --------------- LABELS - INCLUIR --------------
    lbl_title = Label(FormTitle, text="Incluindo nota", font=('Courier New', 18), bg='#F0EC57', width=300)
    lbl_title.pack(fill=X)
    lbl_materia = Label(formContact, text='Matéria:', font=('arial', 14))
    lbl_materia.grid(row=0, sticky=W)
    lbl_professor = Label(formContact, text='Professor(a):', font=('arial', 14))
    lbl_professor.grid(row=1, sticky=W)
    lbl_dia = Label(formContact, text='Dia:', font=('arial', 14))
    lbl_dia.grid(row=2, sticky=W)
    lbl_horario = Label(formContact, text='Horário:', font=('arial', 14))
    lbl_horario.grid(row=3, sticky=W)
    lbl_campus = Label(formContact, text='Campus:', font=('arial', 14))
    lbl_campus.grid(row=4, sticky=W)
    lbl_av1 = Label(formContact, text='AV1:', font=('arial', 14))
    lbl_av1.grid(row=5, sticky=W)
    lbl_av2 = Label(formContact, text='AV2:', font=('arial', 14))
    lbl_av2.grid(row=6, sticky=W)
    lbl_av3 = Label(formContact, text='AV3:', font=('arial', 14))
    lbl_av3.grid(row=7, sticky=W)
    lbl_avd = Label(formContact, text='AVD:', font=('arial', 14))
    lbl_avd.grid(row=8, sticky=W)
    lbl_avds = Label(formContact, text='AVDS:', font=('arial', 14))
    lbl_avds.grid(row=9, sticky=W)

# --------------- ENTRIES - INCLUIR --------------
    materiaEntry = Entry(formContact, textvariable=materia, font=('arial', 11))
    materiaEntry.grid(row=0, column=1)
    professorEntry = Entry(formContact, textvariable=professor, font=('arial', 11))
    professorEntry.grid(row=1, column=1)
    diaEntry = Entry(formContact, textvariable=dia, font=('arial', 11))
    diaEntry.grid(row=2, column=1)
    horarioEntry = Entry(formContact, textvariable=horario, font=('arial', 11))
    horarioEntry.grid(row=3, column=1)
    campusEntry = Entry(formContact, textvariable=campus, font=('arial', 11))
    campusEntry.grid(row=4, column=1)
    av1Entry = Entry(formContact, textvariable=av1, font=('arial', 11))
    av1Entry.grid(row=5, column=1)
    av2Entry = Entry(formContact, textvariable=av2, font=('arial', 11))
    av2Entry.grid(row=6, column=1)
    av3Entry = Entry(formContact, textvariable=av3, font=('arial', 11))
    av3Entry.grid(row=7, column=1)
    avdEntry = Entry(formContact, textvariable=avd, font=('arial', 11))
    avdEntry.grid(row=8, column=1)
    avdsEntry = Entry(formContact, textvariable=avds, font=('arial', 11))
    avdsEntry.grid(row=9, column=1)

# --------------- BOTÃO - INCLUIR --------------
    btn_includecom = Button(formContact, text='Incluir',width=50, command=submitData)
    btn_includecom.grid(row=11, columnspan=2, pady=10)


top = Frame(root, width=500, bd=1, relief=SOLID)
top.pack(side=TOP)
mid = Frame(root, width=500, bg="#0B0A07")
mid.pack(side=TOP)
midleft = Frame(mid, width=100)
midleft.pack(side=LEFT, pady=10)
midleftPadding = Frame(mid, width=100, bg="#0B0A07")
midleftPadding.pack(side=LEFT)
midright = Frame(mid, width=100)
midright.pack(side=RIGHT, pady=10)
bottom = Frame(root, width=200)
bottom.pack(side=BOTTOM)
tableMargin = Frame(root, width=500)
tableMargin.pack(side=TOP)

# --------------- LABEL - PRINCIPAL --------------
lbl_title = Label(top, text="SISTEMA DE GERENCIAMENTO DE NOTAS", font=('Courier New', 16), width=500, bg="#BBCEA8")
lbl_title.pack(fill=X)

lbl_update = Label(bottom, text="Para alterar, clique duas vezes na matéria desejada.", font=('arial black', 12), width=200, bg="#BBCEA8")
lbl_update.pack(fill=X)

# --------------- BUTTONS - PRINCIPAL --------------
btn_add = Button(midleft, text="INCLUIR", bg="#F0EC57", command=addData)
btn_add.pack()
btn_exclude = Button(midright, text="EXCLUIR", bg="#FF0000", command=deleteData)
btn_exclude.pack(side=RIGHT)

# --------------- TABELAS - TREEVIEW --------------
scrollbarX = Scrollbar(tableMargin, orient=HORIZONTAL)
scrollbarY = Scrollbar(tableMargin, orient=VERTICAL)

tree = ttk.Treeview(tableMargin, columns=("ID", "Materia", "Professor", "Dia", "Horario", "Campus", "AV1", "AV2", "AV3", "AVD", "AVDS", "Media"),
            height=400, selectmode="extended", yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
scrollbarX.config(command=tree.xview)
scrollbarX.pack(side=BOTTOM, fill=X)
scrollbarY.config(command=tree.yview)
scrollbarY.pack(side=RIGHT, fill=Y)

tree.heading("ID", text="ID", anchor=W)
tree.heading("Materia", text="Matéria", anchor=W)
tree.heading("Professor", text="Professor", anchor=W)
tree.heading("Dia", text="Dia", anchor=W)
tree.heading("Horario", text="Horário", anchor=W)
tree.heading("Campus", text="Campus", anchor=W)
tree.heading("AV1", text="AV1", anchor=W)
tree.heading("AV2", text="AV2", anchor=W)
tree.heading("AV3", text="AV3", anchor=W)
tree.heading("AVD", text="AVD", anchor=W)
tree.heading("AVDS", text="AVDS", anchor=W)
tree.heading("Media", text="Média", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=1)
tree.column('#1', stretch=NO, minwidth=0, width=30)
tree.column('#2', stretch=NO, minwidth=0, width=200)
tree.column('#3', stretch=NO, minwidth=0, width=130)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=100)
tree.column('#6', stretch=NO, minwidth=0, width=120)
tree.column('#7', stretch=NO, minwidth=0, width=60)
tree.column('#8', stretch=NO, minwidth=0, width=60)
tree.column('#9', stretch=NO, minwidth=0, width=60)
tree.column('#10', stretch=NO, minwidth=0, width=60)
tree.column('#11', stretch=NO, minwidth=0, width=60)

tree.pack()
tree.bind('<Double-Button-1>', onSelect)



if __name__ == '__main__':
    database()
    root.mainloop()
