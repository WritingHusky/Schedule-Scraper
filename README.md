# Scheduler 

## Description

This is a Scrapper for the TRU Class Schedules aimed for the use of professors and faculty. 

## Getting Started

### Dependencies

* Python
* BeautifulSoup v4
* Tkinter
* openyxl

BeautifulSoup is not a in the default Python Libary so it will need to be intalled. This can be done in the terminal using,
```
pip install beautifulsoup4
```

### Installing

* Clone the repo
* Make sure that Beautiful Soup is intalled 


### Executing program

* Download a copy of the website to scrape the data from (Class Schedule Listing)
* Run the Scrapper.py
* You will be asked to choose a file
    * Choose the html file of the website you just downloaded
* A CSV file will be created of the data scraped from the file
* Go to the Scheduler.py file 
    * At the bottom of the file in main(), uncomment one of the lines to choose what to schedule
    * Line 216, 217, or 218
* Run Scheduler.py
* Choose the CSV file to make the Schedule off of
* An xlsx (Excel) file will be made 


## Next Additions 

* Arguments to chose the output of the Scheduler
* Multi sheet output
* Scrape the Capacity 
* Better control of the order of the CSV file

## Authors

- Ethan Gelinas 

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Code Basis / help
* [ChatGPT](https://chat.openai.com/)
