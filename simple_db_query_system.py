import csv
import json
#alptug01

tempdict={} #for select
rows={} #all datas
columns=[] #column names
print_columns=[]
def select(commands): #select operations
    if (commands[2] == "FROM"  and commands[4] == "WHERE" and commands[-3] == "ORDER" and commands[-2] == "BY"):
        if(commands[-1]=="ASC" or commands[-1]=="DSC"):
            global rows
            global columns
            global print_columns
            if(rows=={}):
                reading_csv(f"{commands[3].lower()}.csv")
            templ = []
            and_or = ""
            try:
                for i in range(len(commands) - 1):
                    if (commands[i] == "AND" or commands[i] == "OR"): #getting conditions
                        and_or = commands[i]
                        columns.index(commands[i - 3])
                        for j in range(3):
                            templ.append(commands[i - j - 1])
                    elif (commands[i] == "ORDER"):
                        columns.index(commands[i - 3])
                        for j in range(3):
                            templ.append(commands[i - j - 1])
                        break
            except ValueError:
                print("Please check the conditions")
            templ.reverse()
            global tempdict
            condition_num = len(templ)
            if (condition_num > 6):
                print("Maximum two conditions")
            elif (not (condition_num == 6 or condition_num == 3)):
                print("Please check the conditions")
            else:
                key_str = ""
                operator = ""
                search_value = ""
                operators = ["=", "!=", "<", ">", "<=", ">=", "!<", "!>"]
                print_columns = commands[1].split(",")
                if (condition_num == 3): #one condition situation
                    if (operators.__contains__(templ[1]) == False): #checking operator
                        print("Wrong operator in command")
                    else:
                        key_str = templ[0]
                        operator = templ[1]
                        search_value = templ[2]
                        tempdict.update(operator_operations(operator, search_value, rows, key_str)) #updating tempdict
                        tempdict = sorting_operations(commands, print_columns, tempdict) #sorting

                else: #two condition situation
                    if (operators.__contains__(templ[1]) == False or operators.__contains__(templ[4]) == False):
                        print("Wrong operator in command")
                    else:
                        key_str = templ[0]
                        operator = templ[1]
                        search_value = templ[2]
                        key_str2 = templ[3]
                        operator2 = templ[4]
                        search_value2 = templ[5]
                        tempdict.update(
                            two_conditions(and_or, key_str, operator, search_value, key_str2, operator2, search_value2,
                                           rows))
                        tempdict = sorting_operations(commands, print_columns, tempdict)
        else:
            print("Please check the order type")
    else:
        print("Please check the command ")

def sorting_operations(commands,print_columns,dic): #sorting operations
    if (commands[-1] == "ASC"):
        if (print_columns[0] != "ALL" and print_columns[0] != "ID"):
            dic = dict(sorted(dic.items(), key=lambda item: item[1][print_columns[0]]))
        else:
            dic = dict(sorted(dic.items()))
    else:
        if (print_columns[0] != "ALL" and print_columns[0] != "ID"):
            dic = dict(reversed(sorted(dic.items(), key=lambda item: item[1][print_columns[0]])))
        else:
            dic = dict(reversed(sorted(dic.items())))
    return dic

def two_conditions(and_or,column_name1,operator1,s_v1,column_name2,operator2,s_v2,rows):
    tmpdic={}
    if(and_or=="AND"):
        tmpdic=operator_operations(operator1, s_v1, rows, column_name1)
        tmpdic=operator_operations(operator2, s_v2,tmpdic,column_name2)
    else:
        tmpdic2={}
        tmpdic = operator_operations(operator1, s_v1, rows, column_name1)
        tmpdic2 = operator_operations(operator2, s_v2, rows, column_name2)
        for i in tmpdic2:
            tmpdic[i]=tmpdic2[i]
    return tmpdic

def operator_operations(operator, search_value, rows, key_str): #operator operations
    tmpdic={}
    if (operator == "="):
        tmpdic = adding_dict_w_rows(key_str, search_value, rows)
    elif (operator == "!="):
        tmpdic = inequality(key_str, search_value, rows)
    elif (key_str == "GRADE"):
        tmpdic = compare(operator, search_value, rows, key_str)
    elif (key_str == "ID"):
        tmpdic = compare_ids(operator, search_value, rows)
    else:
        print("Please check the conditions")
        return None
    return tmpdic

def compare(operator,search_value,rows,column_name): #only for grade
    tmpdic = {}
    keys=[]
    search_value=int(search_value)
    if(operator=="<"):
        keys = [k for k, v in rows.items() if v[column_name] < search_value]
    elif(operator==">"):
        keys = [k for k, v in rows.items() if v[column_name] > search_value]
    elif(operator==">=" or operator=="!<"):
        keys = [k for k, v in rows.items() if v[column_name] >= search_value]
    elif(operator=="<=" or operator=="!>"):
        keys = [k for k, v in rows.items() if v[column_name] <= search_value]
    for i in keys:
        tmpdic[i] = rows[i]
    return tmpdic
def compare_ids(operator,search_value,rows): #comparing ids (keys)
    tmpdic={}
    search_value = int(search_value)
    keys = []
    if (operator == "<"):
        keys=[k for k in rows.keys() if k < search_value]
    elif (operator == ">"):
        keys = [k for k in rows.keys() if k > search_value]
    elif (operator == ">=" or operator == "!<"):
        keys=[k for k in rows.keys() if k >= search_value]
    elif (operator == "<=" or operator == "!>"):
        keys=[k for k in rows.keys() if k <= search_value]
    for i in keys:
        tmpdic[i] = rows[i]
    return tmpdic

def inequality(key_str,search_value,rows): #inequality situation
    tmpdic={}
    if(key_str=="ID" or key_str=="GRADE"):
        search_value=int(search_value)
    if (key_str == "ID"):
        keys=[k for k in rows.keys() if k != search_value]
        for i in keys:
            tmpdic[i] = rows[i]
    else:
        keys = [k for k, v in rows.items() if v[column_name] != search_value]
        for i in keys:
            tmpdic[i] = rows[i]
    return tmpdic
def adding_dict_w_rows(key_str,search_value,rows): #adding dictionary
    tmpdic={}
    if (key_str == "ID" or key_str == "GRADE"):
        search_value = int(search_value)
    if (key_str == "ID"):
        tmpdic[search_value]=rows[search_value]
    else:
        tmpdic = adding_temp_dict(search_value, key_str, rows)
    return tmpdic
def adding_temp_dict(search_value,column_name,dic): #equality situation
    if (column_name == "ID" or column_name == "GRADE"):
        search_value = int(search_value)
    keys = [k for k, v in dic.items() if v[column_name] == search_value]
    tmpdic={}
    for i in keys:
        tmpdic[i] = dic[i]
    return tmpdic

def column_name(columns,string):
    for i in range(len(columns) - 1):
        if(string==columns[i]):
            return True
    return False
def reading_csv(filename): #reading csv
    try:
        global columns
        global rows
        file = open(filename)
        csvreader = csv.reader(file)
        header = next(csvreader)
        columns = header[0].upper().split(';')
        #print(header)
        for row in csvreader:
            elements = row[0].upper().split(";")
            elements[0]=int(elements[0])
            rows[elements[0]] = {}
            for i in range(len(elements) - 1):
                if(i+1==1):
                    rows[elements[0]]["NAME"]=elements[1]
                elif(i+1==2):
                    rows[elements[0]]["LASTNAME"] = elements[2]
                elif(i+1==3):
                    rows[elements[0]]["EMAIL"] = elements[3]
                elif(i+1==4):
                    rows[elements[0]]["GRADE"] = int(elements[4])
        rows = dict(sorted(rows.items()))
        col_row=[columns,rows]
        file.close()
        return col_row
    except FileNotFoundError:
        print("File not found, please check the file name")

def insert(commands): #insert operations
    try:
        if (commands[1] == "INTO"):
            values=commands[3].strip("VALUES()").split(",")
            tempstr = commands[3].strip("VALUES()")
            reading_csv(f"{commands[2].lower()}.csv")
            global tempdict
            if(len(values)==len(columns)):
                if(tempdict=={}): #if no selection is made, it inserts it to the main dictionary
                    if(rows.get(values[0])==None):
                        rows[values[0]] = {"NAME": values[1], "LASTNAME": values[2], "EMAIL": values[3],"GRADE": values[4]}
                    else:
                        print("This id already exist")

                else: #if dictionary of select exists
                    if (tempdict.get(values[0]) == None):
                        tempdict[values[0]]={"NAME":values[1],"LASTNAME":values[2],"EMAIL":values[3],"GRADE":values[4]}
                    else:
                        print("This id already exist")
            else:
                print("Please check the values")
        else:
            print("Please check the commands")
    except FileNotFoundError:
        print("File not found, please check the filename")

def delete(commands):
    try:
        global rows
        if(rows=={}):
            reading_csv(f"{commands[2].lower()}.csv")
        dic_del={} #items to be deleted are kept in a temporary dictionary
        condition_len = len(commands) - 4
        if(commands[1]=="FROM" and commands[3]=="WHERE" and (condition_len==3 or condition_len==7)):
            operators = ["=", "!=", "<", ">", "<=", ">=", "!<", "!>"]
            global tempdict
            if(condition_len==3):
                if (operators.__contains__(commands[5]) == False):
                    print("Wrong operator in command")
                else:
                    key_str = commands[4]
                    operator = commands[5]
                    search_value = commands[6]
                    dic_del.update(operator_operations(operator, search_value, rows, key_str))
                    if(tempdict=={}):
                        rows.update(delfromdic(dic_del,rows))
                    else:
                        tempdict.update(delfromdic(dic_del,tempdict))
            elif(condition_len==7):
                if (operators.__contains__(commands[5]) == False or operators.__contains__(commands[9]) == False):
                    print("Wrong operator in command")
                else:
                    key_str = commands[4]
                    operator = commands[5]
                    search_value = commands[6]
                    key_str2 = commands[8]
                    operator2 = commands[9]
                    search_value2 = commands[10]
                    and_or=commands[7]
                    dic_del.update(two_conditions(and_or, key_str, operator, search_value, key_str2, operator2, search_value2,rows))
                    if (tempdict == {}):
                        rows.update(delfromdic(dic_del, rows))
                    else:
                        tempdict.update(delfromdic(dic_del, tempdict))
        else:
            print("Please check the commands")
    except KeyError:
        print("There are no such record, please check the conditions")

def delfromdic(dic1,dic2): #deleting common items of two dictionaries
    for i in dic1:
        if (dic2.get(i) != None):
            dic2.pop(i)
    return dic2
def json_operations(): #json operations
    if(tempdict!={}):
        if(print_columns[0]!="ALL"):
            array=[]
            for d in tempdict.values():
                dic1 = {}
                for k, v in d.items():
                    if (print_columns.__contains__(k)):
                        dic1[k] = v
                dictionary_copy = dic1.copy()
                array.append(dictionary_copy)
            json_object = json.dumps(array, indent=5)
        else:
            json_object = json.dumps(tempdict, indent=5)
        print(json_object)
    elif(rows!={}):
        json_object = json.dumps(rows, indent=5)
        print(json_object)
    else:
        print("no action taken")

def main():
    while (True):
        command = input(">")
        command = command.upper()
        commands=command.split(" ")
        if(commands[0]=="SELECT"):
            select(commands)
        elif(commands[0]=="INSERT"):
            insert(commands)
        elif(commands[0]=="DELETE"):
            delete(commands)
        elif(commands[0]=="EXIT"):
            json_operations()
            break
        else:
            print("Please check the commands")
main()