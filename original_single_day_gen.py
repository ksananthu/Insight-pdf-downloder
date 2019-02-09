import bs4
import requests
from xhtml2pdf import pisa             # import python module
from xhtml2pdf.config.httpconfig import httpConfig
from urllib import parse


res = requests.get("https://www.insightsonindia.com/2019/01/31/insights-daily-current-affairs-pib-31-january-2019/")
soup = bs4.BeautifulSoup(res.text, 'html.parser')
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
<html lang="en"> 

<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
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
  font-family:  Times New Roman;
  font-size: 165%;
}
p  {
  color: black;
  font-family:   Times New Roman;
  font-size: 165%;
}
ol  {
  color: black;
  font-family:   Times New Roman;
  font-size: 165%;
}

ul  {
  color: black;
  font-family:   Times New Roman;
  font-size: 165%;
}
</style>
    
    """

second = """</body>
</html>"""
sourceHtml = first + str(pf) +second
outputFilename = "test.pdf"

# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename):
    # open output file for writing (truncated binary)

    httpConfig.save_keys('nosslcheck', True)

    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(sourceHtml, dest=resultFile, encoding="utf8")


    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err

# Main program
if __name__ == "__main__":
    pisa.showLogging()
    convertHtmlToPdf(sourceHtml, outputFilename)