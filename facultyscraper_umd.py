#This program searches through the faculty profiles at the University of Maryland's Department of Government and Politics 
#website for user-inputted search words or phrases. 
#The purpose is to help find faculty members whose research interests match your own.
#The program outputs the number of results (faculty members with "interesting" profiles)
#and the links to their profile pages, and other documents such as CVs where applicable.

import urllib, re, time
from bs4 import BeautifulSoup

url_base = 'http://www.gvpt.umd.edu/facultystaff/area'
#url = raw_input('Enter URL: ')
area = raw_input('Research Area?\n\n1 - American Politics\n2 - Methodology\n3 - Political Theory\n4 - Comparative Politics\n5 - International Relations\n\n')
search = raw_input('Enter search word/phrase : ')
position = raw_input('Filter out assistant and associate professors? y/n ')

#code needs updating to catch invalid user input
if area == '1': url = url_base + "?taxonomy_vocabulary_4_tid=10"
elif area == '2': url = url_base + "?taxonomy_vocabulary_4_tid=61"
elif area == '3': url = url_base + "?taxonomy_vocabulary_4_tid=62"
elif area == '4': url = url_base + "?taxonomy_vocabulary_4_tid=27"
elif area == '5': url = url_base + "?taxonomy_vocabulary_4_tid=12"

def fac_scrape(url, search, position):
    sleep_time = 1.2 #in seconds
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
    #print(soup.prettify())
    tables = soup('table')

    atags = []
    links = []
    urls = []

    for table in tables:
        if re.search("Permanent Faculty", str(table), re.IGNORECASE) != None:
            perm_fac = table
            tds = perm_fac('td')
        
    for td in tds:
        if len(td) > 3:
            if position == 'y':
                if re.search("Assistant Professor", str(td.contents[3]), re.IGNORECASE) == None and re.search("Associate Professor", str(td.contents[3]), re.IGNORECASE) == None:
                    atags.append(td('a'))
            if position == 'n':
                atags.append(td('a'))

    for atag in atags:
        a_str = str(atag)[1:len(str(atag))-1]
        links.append(re.search('href="(.+)">', a_str).group(1))

    for link in links:
        fac_page_url = 'http://www.gvpt.umd.edu%s' % link
        urls.append(fac_page_url)

    cool_fac_urls = []
    
    print "Searching... Please wait."

    for u in urls:
        time.sleep(sleep_time)
        html2 = urllib.urlopen(u).read()
        soup2 = BeautifulSoup(html2)
        stripped_strings = []

        for string in soup2.stripped_strings:
            stripped_strings.append(string)

        soup2text = " ".join(stripped_strings)
        menu = "Menu About Us People Undergraduate Graduate Research"
        bottom = "Department of Government and Politics"
        reg_this = re.escape(menu) + '(.+)?' + re.escape(bottom)
        text2 = re.search(reg_this, soup2text).group(1)

        if re.search(search, text2, re.IGNORECASE) != None:
            cool_fac_urls.append(u)
    
    print "%d results found" % len(cool_fac_urls)
    
    counter = 1
    
    for item in cool_fac_urls:
        time.sleep(sleep_time)
        html3 = urllib.urlopen(item).read()
        soup3 = BeautifulSoup(html3)
        stripped_strings2 = []
        atags3 = soup3('a')
        
        usplit = item.split("/")
        name = usplit[5] + " " + usplit[4]
        print "\nRetrieving..."
        print "%d out of %d\n" % (counter, len(cool_fac_urls))
        print name
        print item

        for atag3 in atags3:
            if re.search('http://www.gvpt.umd.edu/sites/gvpt.umd.edu/files/', str(atag3.get('href'))) != None:
                print str(atag3.get('href'))
        
        counter += 1
    print "\nDone"

fac_scrape(url, search, position)