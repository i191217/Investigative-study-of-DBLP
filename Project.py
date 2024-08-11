import tkinter as tk
from tkinter import ttk
import pyodbc
import networkx as nx
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pymysql
import pandas as pd
import csv

# Assignment # 2

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-R5AIEK2\SQLEXPRESS;'
                      'Database=someDB;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Creating instance of Tk() class
window = tk.Tk()
window.title("Hello World")

list = []
list2 = []
data = []
data2 = []
a=0
b=0

def click_me():
    text = name.get()
    #cursor.execute("select author_journal.Author, author_journal.Journal, JournalPortal.Title, JournalPortal.Primary_FoR ,JournalDetails.FORID, JournalDetails.FieldOfResearch from author_journal inner join JournalPortal on author_journal.Journal = JournalPortal.Title inner join JournalDetails on JournalPortal.Primary_FoR = JournalDetails.FORID = ?", (text,))

    cursor.execute("select * from author_journal where Author = ?", (text,))
    for row in cursor:
        program(row.Journal)
        method(row.Journal)

a_Label = ttk.Label(window, text="Enter Author's name")
a_Label.grid(column=0, row=0)

a_Button = ttk.Button(window, text="Search", command=click_me)
a_Button.grid(column=1, row=1)

name = tk.StringVar()
name_entered = ttk.Entry(window, width=25, textvariable= name)
name_entered.grid(column=0, row=1)
name_entered.focus()

b_Label = ttk.Label(window, text="Your output will be diplayed here", foreground="blue")
b_Label.grid(column=0, row=3)


def program(journal):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-R5AIEK2\SQLEXPRESS;'
                          'Database=someDB;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute("select * from ConferencePortal where Title = ?", (journal,))
    #print('1) '+journal)
    for row in cursor:
        #print('2) '+ journal)
        program2(row.Primary_FoR)


def program2(For):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-R5AIEK2\SQLEXPRESS;'
                          'Database=someDB;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    #print(For)
    cursor.execute("select * from ConferenceDetails where FORID = ?", (For,))
    for row in cursor:
        list.append(row.FieldOfResearch+ " " + str(row.FORID))
        break

    for i in list:
        print("Conference: " + i)

    print("No. of Conferences: ", len(list))

    global a
    a=len(list)

def method(journal):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-R5AIEK2\SQLEXPRESS;'
                          'Database=someDB;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    cursor.execute("select * from JournalPortal where Title = ?", (journal,))
    #print('1) ' + journal)
    for row in cursor:
        #print('2) '+ journal)
        method2(row.Primary_FoR)



def method2(For):
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-R5AIEK2\SQLEXPRESS;'
                          'Database=someDB;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()
    #print(For)
    cursor.execute("select * from JournalDetails where FORID = ?", (For,))
    for row in cursor:
        if (For == row.FORID):
            list2.append(row.FieldOfResearch + " " + str(row.FORID))
            break

    for i in list2:
        print("Journal: " + i)

    print("No. of Journals: ", len(list2))
    global b
    b=len(list2)
    print(a, " ", b)

    if(a >= b):
        for i in list:
            b_Label.configure(text="FoR is: " + i)
    else:
        for i in list2:
            b_Label.configure(text="FoR is: " + i)






# Assignment # 3

db = pymysql.connect("localhost","root","********","somedb" )

cursor2 = db.cursor()

cursor2.execute("SELECT name FROM somedb.for")
data2 = cursor2.fetchall()


def graph():
    print("FOR: ", FoR.get(), "x =", x.get())
    c = FoR.get()
    c = c.replace("{", "")
    c = c.replace("}", "")
    d=x.get()

    cursor2.execute("select id from somedb.for where name= %s", (c,))
    data3 = cursor2.fetchone()[0]
    cursor2.execute("select * from somedb.g%s where combinepublication >= %s", (data3, d) )
    data4 = cursor2.fetchall()

    f = open("g1203.txt", "w+")
    for row in data4:
        f.write(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + "\n")
    f.close()

    g = nx.read_edgelist("g1203.txt", create_using=nx.Graph(), nodetype=int, data=(('weight', int),))
    nx.info(g)
    g.number_of_nodes()
    g.selfloop_edges()

    print(g.nodes())
    print(g.edges())

    pos = nx.spring_layout(g)
    new_labels = dict(map(lambda x: ((x[0], x[1]), str(x[2]['weight'])), g.edges(data=True)))
    nx.draw_networkx(g, pos=pos)

    nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=new_labels)
    nx.draw_networkx_edges(g, pos, width=4, edge_color='g', arrows=False)

    plt.show()


window.geometry('700x550')
window.resizable(False, False)

z_Label = ttk.Label(window, text="Select an FoR")
z_Label.grid(column=0, row=30)
FoR = tk.StringVar()
FoR_chosen = ttk.Combobox(window, width=45, textvariable=FoR, state='readonly')
FoR_chosen['values'] = data2
FoR_chosen.grid(column=0, row=32)
FoR_chosen.current(0)

x = tk.StringVar()
box_entry = ttk.Entry(window, width=12, textvariable=x)
box_entry.grid(column=2, row=32)

search = ttk.Button(window, text="Show Graph", command=graph)
search.grid(column=4, row=32)




# Assignment # 4

# Predicting Journals/Conferences through Gaussian Naive Bayes

db = pymysql.connect("localhost","root","********","data123" )
cursor3 = db.cursor()

cursor3.execute("select distinct journal_id from someView where year < 2017 order by journal_id")
data20 = cursor3.fetchall()

z_Label2 = ttk.Label(window, text="Journal ID")
z_Label2.grid(column=0, row=40)

FoR3 = tk.IntVar()
FoR_chosen3 = ttk.Combobox(window, width=45, textvariable=FoR3, state='readonly')
FoR_chosen3['values'] = data20
FoR_chosen3.grid(column=0, row=65)
FoR_chosen3.current(0)

k_Label20 = ttk.Label(window, text="Predicted publications are..", foreground = "blue", font = 7)
k_Label20.grid(column=0, row=75)


def Journal_GNB():
    db = pymysql.connect("localhost", "root", "********", "data123")
    cursor = db.cursor()

    s = FoR3.get()
    row = []
    row2 = []

    cursor.execute("SELECT * FROM someView where year < 2017 AND journal_id = %s", (s,))
    some = cursor.fetchall()

    cursor.execute("SELECT * FROM someView where year >= 2017 AND journal_id = %s", (s,))
    some2 = cursor.fetchall()
    print(some2)

    for i in some:
        row.append(i)
    with open('training.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["journal_id", "year", "count"])
        writer.writerows(row)

    for i in some2:
        row2.append(i)
    with open('testing.csv', 'w', newline='') as file2:
        writer = csv.writer(file2)
        writer.writerow(["journal_id", "year", "count"])
        writer.writerows(row2)

    file = pd.read_csv('training.csv')
    x_train = file.drop("count", axis=1)
    y_train = file["count"]

    file2 = pd.read_csv('testing.csv')
    x_test = file2.drop("count", axis=1)
    y_test = file2["count"]

    model = GaussianNB()
    model.fit(x_train, y_train)

    actual = y_test
    predict = model.predict(x_test)
    k_Label20.configure(text = "2017 = " + str(predict[0]) + "\n" + "2018 = " + str(predict[1]) + "\n" + "2019 = " + str(predict[2]) )

    # print("Data used for prediction",x_test)
    # print("Actual output", y_test)
    # print("Prediction output", predict)

    print(metrics.classification_report(actual, predict))

search2 = ttk.Button(window, text="Execute", command=Journal_GNB)
search2.grid(column=2, row=65)







# Predicting Journals/Conferences through Support Vector Machine(SVM)

db = pymysql.connect("localhost","root","********","data123" )
cursor4 = db.cursor()

cursor4.execute("select distinct journal_id from someView where year < 2017 order by journal_id")
data21 = cursor4.fetchall()

z_Label3 = ttk.Label(window, text="Journal ID")
z_Label3.grid(column=0, row=100)

FoR4 = tk.IntVar()
FoR_chosen4 = ttk.Combobox(window, width=45, textvariable=FoR4, state='readonly')
FoR_chosen4['values'] = data21
FoR_chosen4.grid(column=0, row=115)
FoR_chosen4.current(0)

k_Label21 = ttk.Label(window, text="Predicted publications are..", foreground = "blue", font = 7)
k_Label21.grid(column=0, row=130)


def Journal_SVM():
    row = []
    row2 = []
    s = FoR4.get()

    db = pymysql.connect("localhost", "root", "********", "data123")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM someView where year < 2017 AND journal_id = %s", (s,))
    some = cursor.fetchall()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM someView where year >= 2017 AND journal_id = %s", (s,))
    some2 = cursor.fetchall()

    for i in some:
        row.append(i)
    with open('Before_SVM_J.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["journal_id", "year", "count"])
        writer.writerows(row)

    for i in some2:
        row2.append(i)
    with open('After_SVM_J.csv', 'w', newline='') as file2:
        writer = csv.writer(file2)
        writer.writerow(["journal_id", "year", "count"])
        writer.writerows(row2)

    file = pd.read_csv('Before_SVM_J.csv')
    x_train = file.drop("count", axis=1)
    y_train = file["count"]

    file2 = pd.read_csv('After_SVM_J.csv')
    x_test = file2.drop("count", axis=1)
    y_test = file2["count"]

    clf = SVC(kernel='linear')
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    k_Label21.configure(text="2017 = " + str(y_pred[0]) + "\n" + "2018 = " + str(y_pred[1]) + "\n" + "2019 = " + str(y_pred[2]))

    # print("Data used for prediction",x_test)
    # print("Actual output", y_test)
    # print("Prediction output", y_pred)

    print(accuracy_score(y_test, y_pred))

search3 = ttk.Button(window, text="Execute", command=Journal_SVM)
search3.grid(column=2, row=115)







# Predicting FoR through Gaussian Naive Bayes

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-R5AIEK2\SQLEXPRESS;'
                      'Database=Assignment4;'
                      'Trusted_Connection=yes;')
cursor4 = conn.cursor()

cursor4.execute("select distinct forid from someView2 where year < 2017 order by forid")
data22 = cursor4.fetchall()
print(data22)

z_Label4 = ttk.Label(window, text="FoR ID")
z_Label4.grid(column=0, row=140)

FoR5 = tk.IntVar()
FoR_chosen5 = ttk.Combobox(window, width=45, textvariable=FoR5, state='readonly')
FoR_chosen5['values'] = data22
FoR_chosen5.grid(column=0, row=155)
FoR_chosen5.current(0)

k_Label222 = ttk.Label(window, text="Predicted publications are..", foreground = "blue", font = 7)
k_Label222.grid(column=0, row=170)

def FoR_GNB():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-R5AIEK2\SQLEXPRESS;'
                          'Database=Assignment4;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    s = FoR5.get()
    row = []
    row2 = []

    cursor.execute("SELECT * FROM someView2 where year < 2017 AND forid = ?", (s,))
    some = cursor.fetchall()

    cursor.execute("SELECT * FROM someView2 where year >= 2017 AND forid = ?", (s,))
    some2 = cursor.fetchall()

    for i in some:
        row.append(i)
    with open('training.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["journal_id", "year", "count"])
        writer.writerows(row)

    for i in some2:
        row2.append(i)
    with open('testing.csv', 'w', newline='') as file2:
        writer = csv.writer(file2)
        writer.writerow(["journal_id", "year", "count"])
        writer.writerows(row2)

    file = pd.read_csv('training.csv')
    x_train = file.drop("count", axis=1)
    y_train = file["count"]

    file2 = pd.read_csv('testing.csv')
    x_test = file2.drop("count", axis=1)
    y_test = file2["count"]

    model = GaussianNB()
    model.fit(x_train, y_train)

    actual = y_test
    predict = model.predict(x_test)
    print(predict)
    k_Label222.configure(text = "2017 = " + str(predict[0]) + "\n" + "2018 = " + str(predict[1]) + "\n" + "2019 = " + str(predict[2]) )

    # print("Data used for prediction",x_test)
    # print("Actual output", y_test)
    # print("Prediction output", predict)

    print(metrics.classification_report(actual, predict))

search4 = ttk.Button(window, text="Execute", command=FoR_GNB)
search4.grid(column=2, row=155)










# Predicting FoR through Support Vector Machine(SVM)


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-R5AIEK2\SQLEXPRESS;'
                      'Database=Assignment4;'
                      'Trusted_Connection=yes;')
cursor5 = conn.cursor()

cursor5.execute("select distinct forid from someView2 where year < 2017 order by forid")
data23 = cursor5.fetchall()
print(data23)

z_Label5 = ttk.Label(window, text="FoR ID")
z_Label5.grid(column=0, row=185)

FoR6 = tk.IntVar()
FoR_chosen6 = ttk.Combobox(window, width=45, textvariable=FoR6, state='readonly')
FoR_chosen6['values'] = data23
FoR_chosen6.grid(column=0, row=200)
FoR_chosen6.current(0)

k_Label22 = ttk.Label(window, text="Predicted publications are..", foreground = "blue", font = 7)
k_Label22.grid(column=0, row=215)


def FoR_SVM():
    row = []
    row2 = []
    s = FoR6.get()

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-R5AIEK2\SQLEXPRESS;'
                          'Database=Assignment4;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM someView2 where year < 2017 AND forid = ?", (s,))
    result = cursor.fetchall()

    cursor.execute("SELECT * FROM someView2 where year >= 2017 AND forid = ?", (s,))
    result2 = cursor.fetchall()

    for i in result:
        row.append(i)
    with open('Before_SVM_FoR.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["forid", "year", "count"])
        writer.writerows(row)

    for i in result2:
        row2.append(i)
    with open('After_SVM_FoR.csv', 'w', newline='') as file2:
        writer = csv.writer(file2)
        writer.writerow(["forid", "year", "count"])
        writer.writerows(row2)

    file = pd.read_csv('Before_SVM_FoR.csv')
    x_train = file.drop("count", axis=1)
    y_train = file["count"]

    file2 = pd.read_csv('After_SVM_FoR.csv')
    x_test = file2.drop("count", axis=1)
    y_test = file2["count"]

    clf = SVC(kernel='linear')
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    k_Label22.configure(text="2017 = " + str(y_pred[0]) + "\n" + "2018 = " + str(y_pred[1]) + "\n" + "2019 = " + str(y_pred[2]))

    # print("Data used for prediction",x_test)
    # print("Actual output", y_test)
    # print("Prediction output", y_pred)

    print(accuracy_score(y_test, y_pred))

search4 = ttk.Button(window, text="Execute", command=FoR_SVM)
search4.grid(column=2, row=200)










# Number of publications in coming years through Naive Bayes



db = pymysql.connect("localhost","root","********","data123" )
cursor8 = db.cursor()

cursor8.execute("SELECT year FROM data123.yearwise where year >= 2017")
data212 = cursor8.fetchall()

z_Label42 = ttk.Label(window, text="FoR ID")
z_Label42.grid(column=0, row=230)

FoR51 = tk.IntVar()
FoR_chosen51 = ttk.Combobox(window, width=45, textvariable=FoR51, state='readonly')
FoR_chosen51['values'] = data212
FoR_chosen51.grid(column=0, row=245)
FoR_chosen51.current(0)

k_Label32 = ttk.Label(window, text="Predicted publications in a given year..", foreground = "blue", font = 7)
k_Label32.grid(column=0, row=260)


def method():
    row = []
    row2 = []

    db = pymysql.connect("localhost", "root", "********", "data123")
    cursor = db.cursor()
    cursor.execute("select * from data123.yearwise where year < 2017")
    some = cursor.fetchall()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM data123.yearwise where year >= 2017")
    some2 = cursor.fetchall()

    for i in some:
        row.append(i)
    with open('train.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Year", "Publications"])
        writer.writerows(row)

    for i in some2:
        row2.append(i)
    with open('test.csv', 'w', newline='') as file2:
        writer = csv.writer(file2)
        writer.writerow(["Year", "Publications"])
        writer.writerows(row2)

    file = pd.read_csv('train.csv')
    x_train = file.Year
    y_train = file.Publications

    file2 = pd.read_csv('test.csv')
    x_test = file2.Year

    y_test = file2.Publications

    model = GaussianNB()
    model.fit(x_train, y_train)

    actual = y_test
    predict = model.predict(x_test)
    k_Label32.configure(text=predict)

    print("Data used for prediction",x_test)
    print("Actual output", y_test)
    print("Prediction output", predict)

    #print(metrics.classification_report(actual, predict))

search40 = ttk.Button(window, text="Execute", command=method)
search40.grid(column=2, row=245)







window.mainloop()




















