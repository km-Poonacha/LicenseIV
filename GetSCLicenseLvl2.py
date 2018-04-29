# -*- coding: utf-8 -*-
"""
Spyder Editor

Code for developing the network for n-stage least square. 
Step 1: Find the repos started by the owner of the projects. Only individual owned projects 
Step 2: See which of the repos are forks started prior to 2014
Step 3: Find the license of the forked repositories
Step 4: Find the likelihood of choice of license

 FACED MAJOR ISSUES WITH A SPACE BEING ADDED AT THE END OF SOME OF THE CSV FILES . NOT SURE WHY
"""

import csv
import json

SCREPO_CSV = "C:/Users/USEREN/Dropbox/HEC/Project 2 -   License/ICIS18/Data/ExportedISRDataCollabSC_24042018.csv"
PW_CSV = 'C:/Users/USEREN/Dropbox/HEC/Python/PW/PW_GitHub.csv'

TRIP = 0


def getGitHubapi(url):
    """This function uses the requests.get function to make a GET request to the GitHub api
    TRIP flag is used to toggle GitHub accounts. The max rate for searches is 30 per hr per account"""
    import requests
    from time import sleep

    global TRIP
    """ Get PW info """
    PW_list = []
    
    with open(PW_CSV, 'rt', encoding = 'utf-8') as PWlist:
        PW_handle = csv.reader(PWlist)
        del PW_list[:]
        for pw in PW_handle:
            PW_list.append(pw)
    if TRIP == 0:
        repo_req = requests.get(url, auth=(PW_list[0][0], PW_list[0][1]))
        print(repo_req.status_code)
        TRIP = 1
    elif TRIP == 1:
        repo_req = requests.get(url, auth=(PW_list[1][0], PW_list[1][1]))
        print(repo_req.status_code)
        TRIP = 2
    else:
        repo_req = requests.get(url, auth=(PW_list[2][0], PW_list[2][1]))
        print(repo_req.status_code)
        TRIP = 0
        
    if repo_req.status_code == 200: 
        print(repo_req.headers['X-RateLimit-Remaining'])
        if int(repo_req.headers['X-RateLimit-Remaining']) <= 3:
            """  Re-try if Github limit is reached """
            print("************************************************** GitHub limit close t obeing reached.. Waiting for 10 mins" )
            """ Provide a 10 mins delay if the limit is close to being reached  """
            sleep(600)
            
        """ Return the requested data  """
        return repo_req
    else:
        print("Error accessing url = ",url)
        repo_json = repo_req.json()
        print("Error code = ",repo_req.status_code,". Error message = ",repo_json['message'])
        return 0   

def getSCrepo(user,SCREPOL2_CSV):
    user_url = "https://api.github.com/users/"+user+"/subscriptions?page=1&per_page=100"
    rel = ''
    last_page = False
    new_row = []
    while(not last_page):
        print(user_url)
        sub_req = getGitHubapi(user_url)

        if sub_req == 0 or sub_req == None:
            print("************************* Error Finding Subscriptions on URL - "+user_url)
            return 1
        else:   
            # Get the owner and subscriptions information
            sub_json = sub_req.json()

            for subcriptions in sub_json:
                del  new_row[:]
                new_row.append("")
                new_row.append("")
                new_row.append(subcriptions['id'])
                new_row.append(subcriptions['full_name'])
                new_row.append(subcriptions['owner']['login'])
                new_row.append(subcriptions['owner']['id'])
                new_row.append(subcriptions['owner']['type'])
                new_row.append(subcriptions['description'])
                new_row.append(subcriptions['fork'])
                new_row.append(subcriptions['created_at'])
                new_row.append(subcriptions['pushed_at'])
                new_row.append(subcriptions['size'])
                new_row.append(subcriptions['stargazers_count'])
                new_row.append(subcriptions['watchers_count'])
                new_row.append(subcriptions['language'])
                new_row.append(subcriptions['forks_count'])
                new_row.append(subcriptions['license'])
                # Write subscription row             
                with open(SCREPOL2_CSV,'at',encoding='utf-8', newline='') as screpo_obj:
                    screpo_strc = csv.writer(screpo_obj)
                    screpo_strc.writerow(new_row)
                
            # Complete Pagination 
            link = sub_req.headers.get('link',None)
            rel = ""    
            if link is not None:
                rel_temp = link.split("rel")[2]
                rel = rel_temp[2:7]
                parse_url = link.split('rel="next"')[0]
                next_url = parse_url.split('>;')[-2]
                user_url = next_url.split('<')[1]
                if rel == "first":
                    last_page = True
                
            else: last_page = True
            


def main():
    """ Open repo_csv and find the owner name is it is an individual owned repo """
    with open (SCREPO_CSV, 'rt', encoding = 'utf-8') as repocsvobj:
        repocsvstrc = csv.reader(repocsvobj)  
        owner_name = ''
        user_list = []
        count = 1
        csv_no = 1
        SCREPOL2_CSV = "C:/Users/USEREN/Dropbox/HEC/Project 2 -   License/ICIS18/Data/ExportedISRDataCollabSCLvl2_25042018_1.csv"
        for row in repocsvstrc:
            with open(SCREPOL2_CSV,'at',encoding='utf-8',newline='') as screpo_obj:
                screpo_strc = csv.writer(screpo_obj)
                screpo_strc.writerow(row)
            if row[0] == '':
                if owner_name != row[3] and row[5] == 'User' and row[3] not in user_list : 
                    getSCrepo(row[3],SCREPOL2_CSV)
                    user_list.append(row[3])
            else:
                owner_name = row[2]
                print(user_list)
                del user_list [:]
                if count == 200:
                    csv_no = csv_no + 1
                    SCREPOL2_CSV = "C:/Users/USEREN/Dropbox/HEC/Project 2 -   License/ICIS18/Data/ExportedISRDataCollabSCLvl2_25042018_"+str(csv_no)+".csv"
                    print("*****************************STARTING csv no -",csv_no)
                    count = 1
                else:
                    count = count + 1


main()
        