import tkinter
from tkinter import filedialog
from bs4 import BeautifulSoup
import csv

def sortArray(array, order):
    # Sort the array based on the specified order.
    newArray = [None] * 11
    for index, element in zip(order, array):
        newArray[index] = element
    return newArray

def extract_schedule_tables(file_path):
    # Extract schedule tables from an HTML file.
    with open(file_path, "r") as HTMLFile:
        text = HTMLFile.read()

    soup = BeautifulSoup(text, "html.parser")
    # Find tables with specific attributes.
    scheduleTables = soup.find_all("table", {"class": "datadisplaytable", "summary": "This table lists the scheduled meeting times and assigned instructors for this class.."})
    return soup, scheduleTables

def process_table_data(table, title):
    # Process table data and yield class information for each row.
    classInfo = []

    tableData = table.find_all("td", {"class": "dddefault"})
    for info in tableData:
        # Append the text or "TBA" if it's not a string.
        classInfo.append(info.text if isinstance(info.text, str) else "TBA")

    if "(P)" in classInfo[6]:
        # Remove "(P)" from the Schedule Type.
        classInfo[6] = classInfo[6].replace("(P)", "")

    if '-' in classInfo[1]:
        # Split and extend times if there's a hyphen.
        times = classInfo.pop(1).split('-')
        classInfo.extend(times)
    else:
        # Duplicate info if no hyphen.
        info = classInfo.pop(1)
        classInfo.extend([info, info])

    headercopy = title.a.text.split('-')[1:]
    classInfo.extend(headercopy)

    days = classInfo.pop(1).strip()
    if days != "TBA":
        # Duplicate rows for each day if it's not "TBA".
        for day in days:
            newList = classInfo.copy()
            newList.append(day)
            yield newList

def main():
    root = tkinter.Tk()
    root.withdraw()

    # Open file dialog to choose HTML file
    file_path = filedialog.askopenfilename()
    
    assert file_path.endswith(".html"), "Chosen file is not an HTML file"

    # Extract schedule tables from the HTML file.
    soup, scheduleTables = extract_schedule_tables(file_path)

    classesList = []

    for table, title in zip(scheduleTables, soup.find_all("th", {"class": "ddtitle"})):
        # Process each table and associate title information.
        classesList.extend(process_table_data(table, title))

    # Define the order of columns for sorting
    order = [7, 6, 9, 10, 8, 3, 4, 0, 1, 2, 5]

    # Filter columns based on default or user input
    header = ["CRN", "Course", "Section", "Start", "End", "Day", "Location", "Schedule Type", "Instructor", "Date Range", "Type"]

    newClassesList = [sortArray(array, order) for array in classesList]

    fileName = "Schedule.csv"
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header and rows to a CSV file.
        writer.writerow(header)
        writer.writerows(newClassesList)

if __name__ == "__main__":
    main()
