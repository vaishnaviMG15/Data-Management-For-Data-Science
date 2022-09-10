import csv
import re

headers = ['ID', 'age', 'sex', 'city', 'province', 'country', 'latitude', 'longitude', 'date_onset_symptoms', 'date_admission_hospital', 'date_confirmation', 'symptoms']

def round_ages():
  
    reader = csv.DictReader(open("covidTrain.csv", "r"))
    finalLst = []
    for r in reader:
        if str(r['age']).find('-') >= 0:
            a = r['age'].split('-')
            a1 = int(a[0])
            a2 = int(a[1])
            avg = (a1+a2)/2
            r['age'] = round(avg)
        
        finalLst.append(r)
    writer = csv.DictWriter(open("covidTrain.csv", "w", newline=''), delimiter=',', fieldnames=headers)
    writer.writerow(dict((heads, heads) for heads in headers))
    writer.writerows(finalLst)

def change_dates():
  
    reader = csv.DictReader(open("covidTrain.csv", "r"))
    finalLst = []
    for r in reader:
        date = r['date_onset_symptoms'] 
        date2 = r['date_admission_hospital']
        date3 = r['date_confirmation']
        r['date_onset_symptoms'] = re.sub(r'(\d{1,2}).(\d{1,2}).(\d{4})', '\\2.\\1.\\3', date)
        r['date_admission_hospital'] = re.sub(r'(\d{1,2}).(\d{1,2}).(\d{4})', '\\2.\\1.\\3', date2)
        r['date_confirmation'] = re.sub(r'(\d{1,2}).(\d{1,2}).(\d{4})', '\\2.\\1.\\3', date3)
        
        finalLst.append(r)
    writer = csv.DictWriter(open("covidTrain.csv", "w", newline=''), delimiter=',', fieldnames=headers)
    writer.writerow(dict((heads, heads) for heads in headers))
    writer.writerows(finalLst)

def fill_location():
  
    reader = csv.DictReader(open("covidTrain.csv", "r"))
    finalLst = []
    avg = {}
    #key = province value: [latSum, latCount, longSum, longCount]
    for r in reader:
        if r['province'] in avg.keys():
            if r['latitude'] != 'NaN':
                avg[r['province']][0] += float(r['latitude'])
                avg[r['province']][1] += 1
            if r['longitude'] != 'NaN':  
                avg[r['province']][2] += float(r['longitude'])
                avg[r['province']][3] += 1
        else:
            if r['latitude'] != 'NaN' and r['longitude'] != 'NaN':
                    avg[r['province']] = [float(r['latitude']), 1, float(r['longitude']), 1,]
            elif r['latitude'] != 'NaN':
                avg[r['province']] = [float(r['latitude']), 1, 0, 0]
            elif r['longitude'] != 'NaN':
                avg[r['province']] = [0,0, float(r['longitude']), 1]
            else:
                avg[r['province']] = [0, 0, 0, 0]
    
    for k, v in avg.items():
        avgLat = 0
        avgLong = 0
        if v[1] != 0:
            avgLat = round(v[0]/v[1], 2)
        if v[3] != 0:
            avgLong = round(v[2]/v[3], 2)
        
        avg[k] = [avgLat, avgLong]
    
    #print(avg)
    reader2 = csv.DictReader(open("covidTrain.csv", "r"))
    for r in reader2:
        if r['latitude'] == 'NaN' and r['province'] in avg.keys():
            r['latitude'] = avg[r['province']][0]
        if r['longitude'] == 'NaN' and r['province'] in avg.keys():
            r['longitude'] = avg[r['province']][1]
    
        finalLst.append(r)
    writer = csv.DictWriter(open("covidTrain.csv", "w", newline=''), delimiter=',', fieldnames=headers)
    writer.writerow(dict((heads, heads) for heads in headers))
    writer.writerows(finalLst)
    
def sort_helper(dictionary):
    for k, dic in dictionary.items():
        dictionary[k] = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1], reverse = True)}
        maxCount = list(dictionary[k].values())[0]
        lst = [k for k,v in dic.items() if v == maxCount]
        dictionary[k] = sorted(lst)
    return dictionary

def fill_cities():
  
    reader = csv.DictReader(open("covidTrain.csv", "r"))
    finalLst = []
    cities = {}
    for r in reader:
        if r['province'] in cities.keys() and r['city'] != 'NaN':
            if r['city'] in cities[r['province']].keys():
                cities[r['province']][r['city']] += 1
            else:
                cities[r['province']][r['city']] = 1
            
        else:
            if r['city'] != 'NaN':
                cities[r['province']] = {r['city']: 1}
    #print(cities)
    cities = sort_helper(cities)
    #print('\n\n\n After')
    #print(cities)

    reader2 = csv.DictReader(open("covidTrain.csv", "r"))
    for r in reader2:
        if r['city'] == 'NaN' and r['province'] in cities.keys():
            r['city'] = cities[r['province']][0]
        
        finalLst.append(r)
    writer = csv.DictWriter(open("covidTrain.csv", "w", newline=''), delimiter=',', fieldnames=headers)
    writer.writerow(dict((heads, heads) for heads in headers))
    writer.writerows(finalLst)

def fill_symptoms():
  
    reader = csv.DictReader(open("covidTrain.csv", "r"))
    finalLst = []
    symptoms = {}
    for r in reader:
        if r['symptoms'] != 'NaN':
            lst = r['symptoms'].split(';')
            if r['province'] in symptoms.keys():
                for s in lst:
                    s = s.strip()
                    if s in symptoms[r['province']].keys():
                        symptoms[r['province']][s] += 1
                    else:
                        symptoms[r['province']][s] = 1
            
            else:
                symptoms[r['province']] = {}
                for s in lst:
                    s = s.strip()
                    symptoms[r['province']][s] = 1
    
    symptoms = sort_helper(symptoms)
        
    reader2 = csv.DictReader(open("covidTrain.csv", "r"))
    for r in reader2:
        if r['symptoms'] == 'NaN' and r['province'] in symptoms.keys():
            r['symptoms'] = symptoms[r['province']][0]
        
        finalLst.append(r)
    writer = csv.DictWriter(open("covidTrain.csv", "w", newline=''), delimiter=',', fieldnames=headers)
    writer.writerow(dict((heads, heads) for heads in headers))
    writer.writerows(finalLst)
    
    #now writing the whole data into the results
    writer2 = csv.DictWriter(open("covidResults.csv", "w", newline=''), delimiter=',', fieldnames=headers)
    writer2.writerow(dict((heads, heads) for heads in headers))
    writer2.writerows(finalLst)

round_ages()
change_dates()
fill_location()
fill_cities()
fill_symptoms()