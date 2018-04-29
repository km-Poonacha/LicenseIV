# -*- coding: utf-8 -*-
"""
Spyder Editor

Code for developing the network for n-stage least square. 
Calculate the license restrictiveness of the SC
"""

import csv
import json
import ast


CSCREPO_CSV = "C:/Users/kmpoo/Dropbox/HEC/Project 2 -   License/ICIS18/Data/Lvl2/ExportedISRDataCollabSCCalL2_27042018.csv"

def findlicrest(licj):
    """Find license restrictiveness from the JSON data"""
    strongcopy_license = ["GNU Affero General Public License v3.0",
                          "GNU General Public License v2.0",
                          "GNU General Public License v3.0"
                          ]
    
    weakcopy_license = ["Eclipse Public License 1.0",
                        "GNU Lesser General Public License v2.1",
                        "GNU Lesser General Public License v3.0",
                        "Microsoft Reciprocal License",
                        "Mozilla Public License 2.0", 
                        "SIL Open Font License 1.1", 
                        "Creative Commons Attribution Share Alike 4.0 International",
                        "Eclipse Public License 2.0",
                        "European Union Public License 1.1",
                        "European Union Public License 1.2",
                        "Open Software License 3.0"
                         ]
   
    if licj:
        try:
            lic_json = ast.literal_eval(licj)
            lic_name = lic_json.get('name', None)
        except:
            print("***** Failed to parse *****")
            return False , 0
        if lic_name in strongcopy_license:
#            print(lic_name," STRONG ")
            return True , 2
        elif lic_name in weakcopy_license:
#            print(lic_name," WEAK ")
            return True , 1
        elif lic_name in ['Other','Not Found','','None',False]:
#            print(lic_name," NA ")
            return False , 0
        else:
#            print(lic_name," PERMISSIVE ")
            return True , 0
    
        
    else:
        return False, 0
    
    
def main():
    """ Open repo_csv and find all the repo subscribed to which were started before the strat if the project and  """

#    prev_row =["REPO_ID","NAME","OWNER","OWNER_TYPE","SIZE","CREATE_DATE","PUSHED_DATE","MAIN_LANGUAGE","NO_LANGUAGES","SCRIPT_SIZE","STARS","SUBSCRIPTIONS","OPEN_ISSUES","FORKS","LICENCE_NAME","DESCRIPTION","NO_CONTRIBUTORS","NO_PUSHES","NO_PULLS","NO_TASKS","NO_NODES","DEG_SUPER","AVG_COMMITS_PULLREQ","OWNER_PUBLICREPO","OWNER_FOLLOWERS","OWNER_FOLLOWING","OWNER_CREATED","OWNER_HIREABLE","OWNER_EMAIL","TOTAL_CONTRIBUTORS","CONTRIBUTORS_PRE2015","AVG_COMMITS_COMMITTER	","SD_FLAG","C_IDLETIME","S_IDLETIME	","T_IDLETIME","S_SDCNT","T_SDCNT	",
#               "SCNT","TCNT","COMPLETED_FLAG","MONTH_CREATED","SURVIVAL_PERIOD","	DEATH_EVENT","PUSHED_0917","STARS_0917","SUBSCRIBERS_0917","FORKS_0917","SIZE_0917","LICENCE_0917","PUSHED_1017","STARS_1017","SUBSCRIBERS_1017","FORKS_1017","SIZE_1017","LICENCE_1017","CREATED_DAY","PUSHED_MONTH_1017","PUSHED_DAY_1017	","SURVIVAL_PERIOD_1017_MONTH","SURVIVAL_PERIOD_1017_DAY","DEATH_EVENT_1Y","DEATH_EVENT_2Y","DEATH_EVENT_3Y","script_size_kb","script_size_mb","logsize_kb","OWNER_FLAG","GNU_FLAG","str_cl","wk_cl","no_cl","logstars","logsize",
#               "logownerexp","FINAL_CONTRIBUTORS","logcont","deg_sup_sq","deg_sup_cu","int_sup","int_sup_sq","month_jan_flag","month_feb_flag","month_mar_flag","month_apr_flag","month_may_flag","month_jun_flag","log_com_preq","PD1","PD2","PD3","avg_idletime","n_main_language","logstars_1017	","yhat","opt_deg_sup_ind	","opt_deg_sup_org","_st","_d","_t","_t0","outliers_AOM","cooksd	","COLLABORATORS","Flag","NO_COLLABORATOR","NO_CONTRIBUTOR","TOTAL_COLLAB_CONTRIBUTIONS","TOTAL_CONTRIBUTOR_CONTRIBUTIONS","LIC_REST_Lvl1","NO_Lvl1"]
    prev_row =[]
    lic_perm = 0
    lic_rest = 0
    found_sc = 0
    tot_sc = 0
    lic_perm_L2 = 0
    lic_rest_L2 = 0
    found_sc_L2 = 0
    tot_sc_L2 = 0    
    lic_perm_L1_org = 0
    lic_rest_L1_org = 0
    tot_found_sc_L1_org = 0     
    for i in range(1,17):
        SCREPO_CSV = "C:/Users/kmpoo/Dropbox/HEC/Project 2 -   License/ICIS18/Data/Lvl2/ExportedISRDataCollabSCLvl2_25042018_"+str(i)+".csv"
        print(SCREPO_CSV)
        with open (SCREPO_CSV, 'rt', encoding = 'latin-1') as repocsvobj:
            repocsvstrc = csv.reader(repocsvobj)        
            for row in repocsvstrc:	
                if row[0] != '': 
                    prev_row.append(lic_perm)
                    prev_row.append(lic_rest)
                    prev_row.append(found_sc)
                    prev_row.append(tot_sc)
                    prev_row.append(lic_perm_L2)
                    prev_row.append(lic_rest_L2)
                    prev_row.append(found_sc_L2)
                    prev_row.append(tot_sc_L2)
                    prev_row.append(lic_perm_L1_org)
                    prev_row.append(lic_rest_L1_org)
                    prev_row.append(tot_found_sc_L1_org)                    
                    with open(CSCREPO_CSV,'at',encoding='utf-8',newline='') as screpo_obj:
                        screpo_strc = csv.writer(screpo_obj)
                        screpo_strc.writerow(prev_row)
                        
                    owner_name = row[2]
                    create_date = row[5]
    
                    print("REPO ", row[0]," - ",lic_rest," - ",tot_sc)
                    lic_perm = 0
                    lic_rest = 0
                    found_sc = 0
                    tot_sc = 0
                    lic_perm_L2 = 0
                    lic_rest_L2 = 0
                    found_sc_L2 = 0
                    tot_sc_L2 = 0    
                    lic_perm_L1_org = 0
                    lic_rest_L1_org = 0
                    tot_found_sc_L1_org = 0   
                    prev_row = row  
                elif row[1] != '':
                    if row[3] != owner_name and create_date > row[8]:
                        found , restrictiveness = findlicrest(row[15])
                        owner_name_L1 = row[3]
                        create_date_L1 = row[8]
                        tot_sc = tot_sc + 1
                        if found == True:
                            found_sc = found_sc + 1
                            if int(restrictiveness) > 0:
                                lic_rest = lic_rest + int(restrictiveness)
                            else:
                                lic_perm = lic_perm + 1 
                        if row[5] == 'Organization':
                            tot_found_sc_L1_org = tot_found_sc_L1_org + 1
                            if int(restrictiveness) > 0:
                                lic_rest_L1_org = lic_rest_L1_org + int(restrictiveness)
                            else:
                                lic_perm_L1_org = lic_perm_L1_org+ 1
                    else:
                        owner_name_L1 = row[3]
                        create_date_L1 = row[8]
                elif row[2] != '':
                    if row[4] != owner_name_L1 and create_date_L1 > row[9] and create_date > create_date_L1:
                        print(row[3],"  ",create_date,"  ",create_date_L1,"  ",row[9])
                        found , restrictiveness = findlicrest(row[16])
                        tot_sc_L2 = tot_sc_L2 + 1
                        if found == True:
                            found_sc_L2 = found_sc_L2 + 1
                            if int(restrictiveness) > 0:
                                lic_rest_L2 = lic_rest_L2 + int(restrictiveness)
                            else:
                                lic_perm_L2 = lic_perm_L2 + 1 

main()
        