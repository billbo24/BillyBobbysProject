# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 19:52:15 2021

@author: dingl
to do:
    you've got to clean alternative dates.  Anatoly Tarsov has his dates
    as day-month-year and you assumed month-day-year. 
"""



#wikipedia package
import wikipedia
import time
import re
import pandas as pd
import datetime
import numpy as np

months = ['zero','January','February','March',
          'April','May','June','July','August',
          'September','October','November','December']

#alright now I'm going to have to make a few assumptions here.  This 
#wikipedia package makes it prett easy to query the page and all links.  
#This is kinda helpful since a great deal of people will have links (the ones 
#who matter anywa)
#Current plan is to loop through.  Query the links and then look in the
#beginning of the text for a parenthesis (this is where they put birth
#and death dates)

#Now it takes a long time to run these full page pulls....

def scrape_and_save(page,bad_words,my_data,dead_person_cap =-1):
    my_page = wikipedia.page(page)
    list_o_links = my_page.links

    dead_people_found = 0 #scraping takes awhile so while were testing set a limit on the number of people we look for
    
    #print(list_o_links)
    good_candidates = []
    #here's some initial cleaning to trim down the list of names
    for i in list_o_links:
        if i[0].isnumeric():
            continue
        
        #a ton of stuff begins with a single character.  These cant be names
        if i[1] == " ":
            continue
        
        words = i.split()
        if words[0] in bad_words:
            continue
        
        if "(" in i:
            continue
        
        words = i.split()
        
        if len(words) == 1 or len(words) > 3:
            #one word generally isn't a name and anything with more than 3 is rare
            continue
        
        good_candidates.append(i)
    
    counter = 0
    
    for i in good_candidates:
    
        #alright here's my assumption: if it's a persons page there should be a
        #parenthesis after their name (now keep in mind some folks also have their
        #nome de guerre in the parentheses)
        #That means if their name is x characters we only need to check the first x or
        #so characters for a paranthesis.  If there isn't one
        #then that means that it's probably not a person.  
        length_of_name = len(i)
    
        #a ton of links are just to different year academy awards.  no interest
        if i[0].isnumeric():
            continue
        
        #a ton of stuff begins with a single character.  These cant be names
        if i[1] == " ":
            continue
        
        words = i.split()
        if words[0] == "Academy":
            continue
        
        #we can double it for good measure
        length_of_name *= 4
        
        try:
            x = wikipedia.summary(i)
            print(i)
            
        except:
            continue
        
        #now check the first length_of_name characters for a left parenthesis
        if "(" in x[:length_of_name]:
            #Alright it's pretty crude but this gets us someone who
            #has a parenthesis.  Now we need to look inside that parenthesis for a hyphen
            #this is used to separate birth and death
            left = x.find("(")
            right = x.find(")")
            #last character is a ) so we don't care and first is a (
            dates = x[left+1:right]
            if "–" in dates: #indicates a dead person because we have a hyphen seprating two dates
            #note it's not a normal hyphen but a...slightly wider one?
                print("Found a dead person, ",i)
                #alright I believe we're close
                info = re.split(',|\s',dates) #strips spaces and commas
                #the first character is some weird (; thing so we'll ditch that too
                final_info = [i for i in info if i not in  ["–",'']]
                final_info1 = []
                
                
                for q in final_info:
                    try: #this should be a day or year
                        final_info1.append(int(q))
                    except: #should be month
                        #just in case though we'll do one more
                        #By a stroke of luck this also solves 
                        #the 'foreign name' problem.  
                        try:
                            #here's what we're going to do.  
                            #we're going to use this hacky way to see if the word
                            #is a month, but keep it as a month
                            
                            grandma = months.index(q)
                            
                            final_info1.append(q)
                            
                        except:
                            continue
                
                
                #BIG NOTE
                #WE MUST ACCOUNT FOR THE CANADA PROBLEM i.e.
                #DATE IS DAY MONTH YEAR
                
                #So we're going to check if the first entry is a number.  
                #If it is then that's the canadian way and we have to fix it
                
                #there are a number of ways this can go wrong.  One guy
                #only had years for his birthday, 
                #another had june 20 or 30 lol
                if len(final_info1) != 6:
                    continue
                
                if type(final_info1[0]) == str:
                    final_info2 = [i for i in final_info1]
                else:
                    #shuffle them around.  I'm sure there's a better way but who cares
                    final_info2 = [final_info1[1],final_info1[0],final_info1[2],final_info1[4],final_info1[3],final_info1[5]]
                
                #now replace the month string with the number
                final_info2[0] = months.index(final_info2[0])
                final_info2[3] = months.index(final_info2[3])
                
                #now we should really only have month, day, year, month, day, year
                if len(final_info2) == 6: #there should only be 6 data points
                    #do need to pad the data to match the number of columns
                       final_info2 = [i] + final_info2 + [0,0,0]
                       my_data.loc[len(my_data)] = final_info2
                       counter += 1
                       #if counter == 5:
                           #break

                dead_people_found += 1
                if dead_people_found == dead_person_cap:
                    break
    
    
    #alright looks like we're going to have a lot less cleaning to do this time around.  
    #All dates are Month DD, YYYY.  Need to remove those commas.  
    
    total_count = 0
    before_birthday = 0
    after_birthday = 0
    on_birthday = 0 
    
    
    
    for index,row in my_data.iterrows():
        #Alright all that's left to do is check the month first.  If it's 
        #less than its a miss, if its greater its a hit, and if its equal we have to check the day
        total_count += 1
        
        if row['Birth Month'] > row['Death Month']:
            #birth month is greater than death month, fail
            before_birthday += 1
        elif row['Birth Month'] < row['Death Month']:
            #birth month is before death month
            after_birthday += 1
            row['BirthDeathBool'] = 1
        else: #months match
            #check day
            if row['Birth Day'] > row['Death Day']:
                #didn't see birthday
                before_birthday += 1
            elif row['Birth Day'] < row['Death Day']:
                #did see birthday
                after_birthday += 1
                row['BirthDeathBool'] = 1
            else:
                #died on their birthday! How odd
                row['BirthDeathBool'] = 1
                row['BirthdayDeath'] = 1
                on_birthday += 1
        #let's also append their age
        if row['BirthDeathBool'] == 1:
            row['Age'] = (row['Death Year']-row['Birth Year'])
        else:
            row['Age'] = (row['Death Year']-row['Birth Year']-1)
    print(after_birthday / total_count)
    return my_data

pages = ["List of Members Baseball Hall of Fame",
         "List of Members Hockey Hall of Fame",
         "List of Members Football Hall of Fame",
         "List of People with the Most Children"]

headers = ['Name','Birth Month','Birth Day','Birth Year','Death Month','Death Day','Death Year','BirthDeathBool','Age','BirthdayDeath']


bad_words = ["Chicago","AFL","AFC","National","American","Academy"]\

#Weird note: When you loop through page values, if you don't do "pages[3:]"
#Or something that results in a vector, it will run but with like weird meta links

#Still need to figure out how to save all this data
my_data  = pd.DataFrame(columns=headers)
for page in pages[:1]:
    my_data = scrape_and_save(page,bad_words,my_data,5)


#I think it's also kinda fun to see who died before their birthday earliest in the year
#and who lived past it latest in the year.  


#We'll calculate the "delta" i.e. how close people died to their birthday

#This vectorize function seems worth learning better.  
my_data['birthdate'] = np.vectorize(lambda x,y,z: datetime.date(month=x,day=y,year=z))(my_data['Birth Month'],my_data['Birth Day'],my_data['Birth Year'])
my_data['deathdate'] = np.vectorize(lambda x,y,z: datetime.date(month=x,day=y,year=z))(my_data['Death Month'],my_data['Death Day'],my_data['Death Year'])
my_data['birthday_death_year']  = np.vectorize(lambda x,y,z: datetime.date(month=x,day=y,year=z))(my_data['Birth Month'],my_data['Birth Day'],my_data['Death Year'])

my_data['delta'] = my_data['deathdate'] - my_data['birthday_death_year']

print(my_data)