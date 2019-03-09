from tkinter import Tk, Entry, Button, INSERT

import bs4
import requests
from xhtml2pdf import pisa
import os
from urllib import parse


root = Tk()


def Openfolder(directory):
    os.startfile(directory)

def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result




map = []

# Create single line text entry box
entry2 = Entry(root)
entry2.pack()

entry3 = Entry(root)
entry3.pack()

def open_folder():
    d2_x = entry2.get()
    month = str(d2_x)

    d3_x = entry3.get()
    year = str(d3_x)

    month_year = month + '-' + year

    dir = 'G:\\civil\\insight\\current\\'+ month_year + '\\new'

    if not os.path.exists(dir):
        os.makedirs(dir)

    os.chdir(dir)
    Openfolder(dir)

button = Button(root, text='Open Folder', command=open_folder)
button.pack()

entry = Entry(root)
entry.pack()

entry1 = Entry(root)
entry1.pack()



# Insert some default text
entry1.insert(INSERT, '32')
entry2.insert(INSERT, 'march')
entry3.insert(INSERT, '2019')

# Print the contents of entry widget to console
def download_date():
    d_x = entry.get()
    d_y = int(d_x)

    d1_x = entry1.get()
    d1_y = int(d1_x)

    d2_x = entry2.get()
    month = str(d2_x)

    d3_x = entry3.get()
    year = str(d3_x)

    month_year = month + '-' + year

    dir = 'G:\\civil\\insight\\current\\'+ month_year + '\\new'
    os.chdir(dir)
    Openfolder(dir)

    for q in range(d_y, d1_y):

        if q < 10:
            x = '0' + str(q) + '-' + month_year 
        else:
            x = str(q) + '-' + month_year            

        res = requests.get('https://www.insightsonindia.com/insights-ias-upsc-current-affairs/')
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        for link in soup.find_all('a', href=True):
            id = link['href']
            if id.find('/insights-daily-current-affairs') != -1:
                if id.find(x) != -1:
                    map.append(id)

        for s in getUniqueItems(map):
            res = requests.get(s)
            soup = bs4.BeautifulSoup(res.text, 'lxml')
            dates = soup.select_one('div > ul > li.post_date.h6 > span')
            pf = soup.find("div", class_="pf-content")

            imgs = pf.find_all('img')
            for img in imgs:
                url = img['src']
                scheme, netloc, path, params, query, fragment = parse.urlparse(url)
                new_path = parse.quote(path)
                new_url = parse.urlunparse((scheme, netloc, new_path, params, query, fragment))
                img['src'] = new_url

            # Define your data
            first = """<html>
                    <head>
                    <style>
                        @page {
                            size: a4 portrait;
                            @frame header_frame {           /* Static Frame */
                                -pdf-frame-content: header_content;
                                left: 50pt; width: 512pt; top: 20pt; height: 10pt;
                            }
                            @frame content_frame {          /* Content Frame */
                                left: 50pt; width: 472pt; top: 21pt; height: 747; right: 40pt;

                            }

                            @frame footer_frame {           /* Another static Frame */
                                -pdf-frame-content: footer_content;
                                left: 270pt; width: 292pt; top: 777pt; height: 15pt;
                            }
                      }   
                    </style>

                    </head>

                    <body>
                        <!-- Content for Static Frame 'header_frame' -->
                        <div id="header_content"></div>

                        <!-- Content for Static Frame 'footer_frame' -->
                        <div id="footer_content">  Page <pdf:pagenumber>
                            of <pdf:pagecount> 
                        </div>

                        <!-- HTML Content -->
                        <style>
                    h1 {
                      color: black;
                      font-family:  Verdana;
                      font-size: 145%;
                    }
                    h3 {
                      color: black;
                      font-family:  Verdana;
                      font-size: 145%;
                    }
                    p  {
                      color: black;
                      font-family:   Verdana;
                      font-size: 145%;
                    }
                    ol  {
                      color: black;
                      font-family:   Verdana;
                      font-size: 145%;
                    }

                    ul  {
                      color: black;
                      font-family:   Verdana;
                      font-size: 145%;
                    }
                    </style>

                        """

            second = """</body>
                    </html>"""
            sourceHtml = first + str(pf) + second


            # o = s.replace('https://www.insightsonindia.com/2019/02/', '')       # change here
            # v = o.replace('/insights-daily-current-affairs-pib', '')
            # z = v.replace('/', '')

            # outputFilename = z + ".pdf"

            outputFilename = str(dates.text) + ".pdf"

            # Utility function
            def convertHtmlToPdf(sourceHtml, outputFilename):
                # open output file for writing (truncated binary)
                resultFile = open(outputFilename, "w+b")

                # convert HTML to PDF
                pisaStatus = pisa.CreatePDF(sourceHtml, dest=resultFile)

                # close output file
                resultFile.close()  # close output file

                # return True on success and False on errors
                return pisaStatus.err

            # Main program
            if __name__ == "__main__":
                pisa.showLogging()
                convertHtmlToPdf(sourceHtml, outputFilename)
            print(
                "############################---" + outputFilename + "---download complete ##############################")
            map.clear()






# Create a button that will print the contents of the entry


button1 = Button(root, text='download', command=download_date)
button1.pack()

# Make window 300x150 and place at position (50,50)
root.geometry("300x150+50+50")


root.mainloop()