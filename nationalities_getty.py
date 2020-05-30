import csv
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Main page
# http://www.getty.edu/research/tools/vocabularies/ulan/?find=Bene%C5%A1%20Vincenc&role=&nation=&page=1&fbclid=IwAR23jdNLequT5VaR3QPz1ROzTESUH9Sv9V5d-1dgwh83cqheSIGCwq3Uksk

# DOC page
# http://www.getty.edu/research/tools/vocabularies/obtain/index.html?fbclid=IwAR1a0gCE8hfkgYHXVO90uGlwcn0gh9qtgnJ1LGe0dxRIaDJbmRAvMwjpfl0

# Download centre
# http://www.getty.edu/research/tools/vocabularies/obtain/download.html

# API page
# https://www.getty.edu/research/tools/vocabularies/obtain/download.html

# API doc
# https://www.getty.edu/research/tools/vocabularies/vocab_web_services.pdf

class FirstTest(unittest.TestCase):
    # SETS UP CHROME
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--proxy-server='direct://'")
        # chrome_options.add_argument("--proxy-bypass-list=*")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def test_scrape_authors_nationalities(self):
        self.setUp()

        authors = []
        # Open CSV
        with open('source.csv', newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_NONE)
            for row in csv_reader:
                # Add authors to the array of unique authors
                if row[2] not in authors and row[2] != 'Autor':
                    authors.append(row[2])

            print(authors)
            print(f'There is {len(authors)} authors.')
            index = 1
            bug_index = 0

        with open('output.csv', mode='w', encoding='utf-8', newline='') as csv_write_file:
            csv_writer = csv.writer(csv_write_file, delimiter='|')

            for author in authors:
                # make from it the string of names connected with plus or not
                self.driver.get(f'http://www.getty.edu/vow/ULANServlet?english=Y&find={author}&role=&page=1&nation=')

                try:
                    name = self.driver.find_element_by_xpath(
                        "/html/body/div[1]/table/tbody/tr[2]/td[2]/table[1]/tbody/tr[22]/td[4]/span[@class='page']/a/b").text.strip().split('\n')[0]
                    description = self.driver.find_element_by_xpath(
                        "/html/body/div[1]/table/tbody/tr[2]/td[2]/table[1]/tbody/tr[23]/td[3]/span[@class='page']").text.strip().split('\n')[0]
                except:
                    name = 'AUTHORNOTFOUND'
                    description = "AUTHORNOTFOUND"
                    bug_index += 1

                print(f'{index}/{len(authors)} - Getting {author} info: {name} / {description}')

                csv_writer.writerow([index, author, name, description])
                csv_write_file.flush()
                index += 1

        print(f'{bug_index} authors were not found out of {len(authors)}')

    def tearDown(self):
        self.driver.quit()


test = FirstTest()
test.test_scrape_authors_nationalities()
test.tearDown()




