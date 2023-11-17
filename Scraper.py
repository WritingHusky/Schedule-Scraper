from operator import itemgetter
import tkinter
from tkinter import filedialog
from bs4 import BeautifulSoup
import csv

root = tkinter.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

assert file_path.endswith(".html"), "Chosen file is not an HTML file"
HTMLFile = open(file_path, "r")

text = HTMLFile.read()

soup = BeautifulSoup(text, "html.parser")

scheduleTables = soup.find_all("table", {"class": "datadisplaytable", "summary": "This table lists the scheduled meeting times and assigned instructors for this class.."})

classesList = []
header = ["Type", "Location", "Date Range", "Schedule Type", "Instructor", "Start", "End", "CRN", "Course", "Section", "Days"]
# Need: crn, course, section, split times
# Loop through each table and associate title information
headercopy = header.copy()
for table, title in zip(scheduleTables, soup.find_all("th", {"class": "ddtitle"})):

    # find the data
    tableData = table.find_all("td", {"class": "dddefault"})
    classInfo = []
    
    for info in tableData:
        if isinstance(info.text, str):
            classInfo.append(info.text)
        else:
            classInfo.append("TBA")
    
    # "Type","Time","Days","Location","Date Range", "Schedule Type", "Instructor"
    if "(P)" in classInfo[6]:
        classInfo[6] = classInfo[6].replace("(P)", "")
    
    # Split the times
    if '-' in classInfo[1]:
        times = classInfo.pop(1).split('-')
        classInfo.append(times[0])
        classInfo.append(times[1])
    else:
        info = classInfo.pop(1)
        classInfo.append(info)
        classInfo.append(info)
    
    # Add title data
    headercopy = title.a.text.split('-')
    headercopy.pop(0)
    for thing in headercopy:
        classInfo.append(thing)

    # repeat if days repeat
    days = classInfo.pop(1).strip()
    if days != "TBA":
        for day in days:
            newList = classInfo.copy()
            newList.append(day)
            classesList.append(newList)


# Formating the output
#       ["Type", "Location", "Date Range", "Schedule Type", "Instructor", "Start", "End", "CRN", "Course", "Section", "Days"]
order = [  7,       6,              9,          10,              8,          3,        4,    0,      1,          2,      5]
newClassesList = []
def sortArray(array):
    newArray = [None] * 11
    for index, element in zip(order, array):
        newArray[index] = element
    return newArray
    
for array in classesList:
    newClassesList.append(sortArray(array))
header = sortArray(header)
classesList = newClassesList


fileName = "Schedule.csv"

with open(fileName, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(header)
    for row in classesList:
        writer.writerow(row)
