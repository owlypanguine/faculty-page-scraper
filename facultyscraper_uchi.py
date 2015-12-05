import urllib, re, time
from bs4 import BeautifulSoup

sleep_time = 1.1 #in seconds

print "Note: This program takes some to initialize. You may need to wait 30-40 seconds after the second prompt. The rest of the program will run smoothly."

class CacheFetcher:
    def __init__(self):
        self.cache = {}
    def fetch(self, url, max_age=0):
        if self.cache.has_key(url):
            if int(time.time()) - self.cache[url][0] < max_age:
                return self.cache[url][1]
        # Retrieve and cache
        time.sleep(sleep_time)
        data = urllib.urlopen(url).read()
        self.cache[url] = (time.time(), data)
        return data

fetcher = CacheFetcher()

def get_fac(url):
    html = fetcher.fetch(url, 60 * 15)
    soup = BeautifulSoup(html)
    #print(soup.prettify())
    trs = soup('tr')

    fac_dict = {}

    for tr in trs:
        atags = soup('a')
        for atag in atags:
            if len(atag.contents[0]) > 1:
                split = atag.contents[0].split(" ")
                if len(split) > 1 and re.search('uchicago.edu', split[0]) == None and re.search('^/people/faculty/', atag.get('href', None)):
                    #page = url + unicode(atag.get('href', None)
                    fac_dict.update({atag.contents[0] : 'http://political-science.uchicago.edu' + atag.get('href', None)})
                    
    return fac_dict

def search_page(search, pg):
    html2 = fetcher.fetch(pg, 60 * 15)
    soup2 =  BeautifulSoup(html2)
        
    text_list = []
    
    for string in soup2.stripped_strings:
        if len(string) > 1:
            text_list.append((unicode(string)))

    text = " ".join(text_list)
 
    header = "The University of Chicago Political Science Search: Connect: Facebook Twitter Home People Faculty Staff Graduate Students PhDs on the Market Graduate Program Program Brochure Program Requirements Funding & Fellowships Teaching Opportunities Research Projects Comprehensive Exams Admissions Admissions FAQ Placement History Undergraduate Program Program Requirements Admissions Academics Courses Course Archive Resources UChicago Catalogs Academic Calendars Workshops Contact PEOPLE Faculty Staff Graduate Students PhDs on the Market"
    footer = "University of Chicago Connect: Facebook Twitter The University of Chicago The Department of Political Science" 
    reg_this = re.escape(header) + '(.+)?' + re.escape(footer)
    
    if re.search(reg_this, text) != None:
        text2 = re.search(reg_this, text).group(1)
    else:
        text2 = text
    
    mod_search = ' ' + search + '[^\w]'
    if len(search) <5 and " " not in search:
        search = mod_search
        
    found = re.search(search, text2, re.IGNORECASE)
    return found

def filter_fac(fac_dict):
    #sleep_time = 1 #in seconds
    full_fac_dict = {}
 
    for key, value in fac_dict.iteritems():
        #time.sleep(sleep_time)

        if search_page('assistant professor', value) == None and search_page('associate professor', value) == None:
            full_fac_dict.update({key:value})
            
    return full_fac_dict

def fac_scrape(url, search, position):
    #sleep_time = 1 #in seconds
    dict = get_fac(url)
    if position == "y":
        dict = filter_fac(dict)
    
    cool_fac_dict = {}
    
    for key, value in dict.iteritems():
        #time.sleep(sleep_time)
        if search_page(search, value) != None:
            cool_fac_dict.update({key:value})
            
    print "%d results found" % len(cool_fac_dict)

    counter = 1
    
    for key, value in cool_fac_dict.iteritems():
        html3 = fetcher.fetch(value, 60 * 15)
        soup3 = BeautifulSoup(html3)
        stripped_strings2 = []
        atags3 = soup3('a')
        
        print "\nRetrieving..."
        print "%d out of %d\n" % (counter, len(cool_fac_dict))
        print unicode(key)
        print value
        
        for atag3 in atags3:
            if re.search('cv', str(atag3.get('href')), re.IGNORECASE) != None and re.search('.pdf', str(atag3.get('href'))) != None:
                print 'http://political-science.uchicago.edu/' + str(atag3.get('href'))
        
        counter += 1
    print "\nDone"

while True: 
    while True:
        search = raw_input('Enter search word/phrase: ')
        if len(search) > 1: break
        else:   
            continue

    while True:
        position = raw_input('Filter out assistant and associate professors? y/n ')
        print "Searching... Please wait."
        if position in ["y", "n"]:
            break
        else:
            print "Invalid selection. Enter y or n."
            continue
    
    fac_scrape('http://political-science.uchicago.edu/people/faculty.shtml', search, position)
    
    quit = raw_input('Quit program? y/n ')
    if quit == 'y':
        break
    else:
        continue
