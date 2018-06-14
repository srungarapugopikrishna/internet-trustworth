from mediabias_urlextractor import extract_url

high = "/home/gsrungarapu/Heroku/trustworth/internet-trustworth/fakelinkshub/resources/mediabiasfactcheck_High.txt"
fake = "/home/gsrungarapu/Heroku/trustworth/internet-trustworth/fakelinkshub/resources/mediabiasfactcheck_fake.txt"
low = "/home/gsrungarapu/Heroku/trustworth/internet-trustworth/fakelinkshub/resources/mediabiasfactcheck_Low.txt"
mixed = "/home/gsrungarapu/Heroku/trustworth/internet-trustworth/fakelinkshub/resources/mediabiasfactcheck_Mixed.txt"
veryhigh = "/home/gsrungarapu/Heroku/trustworth/internet-trustworth/fakelinkshub/resources/mediabiasfactcheck_VeryHigh.txt"
files = [high, fake, low, mixed, veryhigh]
count = 0
urllist = []
for file in files:
    with open(file) as fp:
        for line in fp:
            count += 1
            # print(line)
            txt = line
            url = txt[17:txt.find('">')]
            urllist.append(url)
            print("Url:", url)
            if 'mediabiasfactcheck.com/' in url:
                print(extract_url(url))
            txt = txt[txt.find('">')+2:]
            print("Name :", txt[:txt.find("</a>")])
            txt = txt[txt.find("</td>"):]
            txt = txt[txt.find('">')+2:]
            print("Bias :", txt[:txt.find("</td>")])
            txt = txt[txt.find("</td>")+5:]
            txt = txt[txt.find('">')+2:]
            print("Reporting :", txt[:txt.find("</td>")])
            txt = txt[txt.find("<td"):]
            txt = txt[txt.find('">')+2:]
            print("References :", txt[:txt.find("</td>")])

print(count)
print(len(set(urllist)), "\n", urllist)