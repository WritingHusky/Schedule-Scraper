import tkinter
from tkinter import filedialog
from bs4 import BeautifulSoup
import pandas as pd
import csv

root = tkinter.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

assert file_path.endswith(".html"), "Chossen file is not an html file"
HTMLFile = open(file_path,"r")

text = HTMLFile.read()

soup = BeautifulSoup(text, "html.parser")

fullTable = soup.find_all("th",{"class": "ddtitle"})
titleList = []
for title in fullTable:
    header = title.a.text.split('-')
    header.pop(0)
    singleHeader = []
    for thing in header:
        singleHeader.append(thing) 
    titleList.append(singleHeader)  

scheduleTables = soup.find_all("table",{"class": "datadisplaytable", "summary":"This table lists the scheduled meeting times and assigned instructors for this class.."})

classesList = []
header = ["Type","Location","Date Range", "Schedule Type", "Instructor","Start", "End","CRN","Course","Section","Days"]
# Need: crn, course, section, split times
# Loop through each table 
for table in scheduleTables:
    
    # find the data
    tableData = table.find_all("td",{"class": "dddefault"})
    classInfo =[]
    for info in tableData:
        classInfo.append(str(info.text))
    # "Type","Time","Days","Location","Date Range", "Schedule Type", "Instructor"
    if "(P)" in classInfo[6]:
        classInfo[6] = classInfo[6].replace("(P)","")
    #  Split the times
    if '-' in classInfo[1]:
        times = classInfo.pop(1).split('-')
        classInfo.append(times[0])
        classInfo.append(times[1])
    else:
        info = classInfo.pop(1)
        classInfo.append(info)
        classInfo.append(info)
        
    
    # Add title data
    for titleInfo in titleList.pop(0):
        titleInfo = titleInfo.replace("S0","").strip()
        classInfo.append(titleInfo)
        
    # repeat if days repeat
    days = classInfo.pop(1).strip()
    # print(days)
    length = len(days)
    # print(length)
    for day in days:
        # print(i)
        newList = classInfo.copy()
        # print(newList)
        newList.append(day)
        # print(newList)
        classesList.append(newList)
        # print("AHHH ----")
        
# print(classesList)

fileName = "Schedule.csv"

with open(fileName, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(header)
    for row in classesList:
        # print(row)
        writer.writerow(row)
    # writer.writerows(classesList)
    
    
