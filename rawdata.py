import urllib
from bs4 import BeautifulSoup
import string
import csv
import cPickle as pickle
f = open("India_url.pkl","rb")
l1 = pickle.load(f)
f.close()

print 'opening file'
out = open("raw_data.csv","wb")
output = csv.writer(out)
output.writerow(['Opposition','Venue','Batting 1st/2nd',"India's Score",'Opposition score','wickets taken','wickets given','Result'])

print 'getting data'
count = 1
page=[]
for e in l1:
    url = "http://www.howstat.com.au/cricket/Statistics/Matches/MatchScorecard_ODI.asp?MatchCode=" + str(e)
    url_contents=urllib.urlopen(url)
    page = BeautifulSoup(url_contents.read())

    result = page.findAll(attrs={'class':"TextBlack8",'valign':"top"})

    r1 = result[4].contents[0].split()
    if r1[0] == 'No' or r1[0] == 'Match':
        continue

    if r1[0] == 'New' or r1[0] == 'West' or r1[0] == 'East' or r1[0] == 'South' or r1[0] == 'Sri':
        r = r1[0] + r1[1]
    else:
        r = r1[0]


    #venue

    venue = result[1]
#    print '-------------------------------------------------------------------------------------'
#    print venue
    rew = venue.contents[0].split(',')
    venue = rew[-1]
    venue = venue.split()
    venue = venue[0]
#    print venue



    #opposition data  
    opposition = page.findAll(attrs = {'class': "ScoreCardBanner2" })
    l = opposition[0].contents[0]
    l = l.split('v')
#    print l
    l2=l[0].split()       #before versus
    l3=l[1].split()       #after versus


    if 'India' not in l2:
        if l2[-2] == 'New' or l2[-2] == 'West' or l2[-2] == 'Sri' or l2[-2] == 'South' or l2[-2] == 'East':
            oppose = l2[-2] + l2[-1]
        else:
            oppose = l2[-1]
    else:
        if l3[0] == 'New' or l3[0] == 'West' or l3[0] == 'Sri' or l3[0] == 'South' or l3[0] == 'East':
            oppose = l3[0] + l3[1]
        else:
            oppose = l3[0]

  #  print oppose

            
    #batting 1st or 2nd
    bat=page.findAll(attrs={'class':"TextBlackBold8",'valign':"top",'colspan':"2"})
    b1=bat[0].contents[0].split()
    b2=bat[1].contents[0].split()
    if b1[0] == 'India':
        bat1 = '1'
    else:
        bat1 = '0'

    #scores
    score = page.findAll(attrs={'class':"TextBlackBold8",'align':"right" ,'valign':"top"})
    score1 = score[5].contents[0].split()[0]
    score2 = score[17].contents[0].split()[0]
    if bat1 == '1':
        s1 = score1
        s2 = score2
    else:
        s1=score2
        s2=score1

    #wickets
    wicket = page.findAll(attrs={'class':"TextBlackBold8",'valign':"top"})
    w1 = wicket[13].contents[0].split()[0]
    w2 = wicket[30].contents[0].split()[0]
    if w1 == 'SR':       #ths happens when we have note and video clips given in particular match
        w1 = wicket[15].contents[0].split()[0]
        w2 = wicket[32].contents[0].split()[0]
    elif w1 == 'Total':     #this happens when we have only one of note or video clips given in particular match
        w1 = wicket[14].contents[0].split()[0]
        w2 = wicket[31].contents[0].split()[0]
    if w1 == 'All':
        w1 = '10'

 #   print w2
    if w2 == 'All':
        w2 = '10'
    if bat1 == '0':
        wic1 = w1
        wic2 = w2
    else:
        wic1 = w2
        wic2 = w1
       
    output.writerow([oppose,venue,bat1,s1,s2,wic1,wic2,r])
    print count
    count += 1
    

out.close()
    
    
    
    
    

    

