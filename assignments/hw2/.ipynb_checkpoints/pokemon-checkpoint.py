import csv
from collections import Counter

def check():
    with open('pokemonTrain.csv') as infile:
        reader = csv.reader(infile)
        next(reader)
        count = 0
        for index,row in enumerate(reader):
            if(len(row) != 10):
                count += 1
        print('Number of rows with too few or too many values: ', str(count))

def method1():
    count_fire = 0.0
    count_fire_above40 = 0.0
    reader = csv.DictReader(open('pokemonTrain.csv'))
    for index,row in enumerate(reader):
        if row['type'] == 'fire':
            count_fire += 1
            try:
                if float(row['level']) >= 40:
                    count_fire_above40 += 1
            except:
                continue
                
    perc = (count_fire_above40/count_fire)*100
    perc_r = round(perc)
    print('count-fire: ', str(count_fire))
    print('count-fire-above40: ', str(count_fire_above40))
    print('Percentage of fire type Pokemons at or above level 40 = ', str(perc))
    print('Percentage of fire type Pokemons at or above level 40 = ', str(perc_r))
    with open('pokemon1.txt', 'w') as outfile:
        outfile.write(str(perc_r) + '\n')

                
def method2_helper():
    
    with open('pokemonTrain.csv') as file:
        
        #create a dictionary:
        #key: weakness
        #value: counterDict where the key is a type and the value is the number of entries of this type and 
        #weakness
        
        reader = csv.DictReader(file)
        d = {}
        
        for index, row in enumerate(reader):
            if row['type'] == 'NaN':
                continue;
            if row['weakness'] in d:
                d[row['weakness']].update([row['type']])
            else:
                d[row['weakness']] = Counter([])
                d[row['weakness']].update([row['type']])
                
        print(d) 
        return d

def method2():
    
    #read in all the rows into a list
    #result: list of lists where each internal list is a row
    rowList = []
    with open('pokemonTrain.csv') as bfile:
        reader = csv.reader(bfile)
        for num,row in enumerate(reader):
            rowList.append(row)
            
    #get dictionary about info of different weaknesses and the common types they are associated with
    w_t = method2_helper() 
           
    #go through all the rows, 
    #fill in the entry of a missing type according to the dictionary recieved from the helper
    #write the row to the file
    with open('pokemonTrain.csv', 'w', newline = '') as afile:   
            writer = csv.writer(afile, delimiter=',')
            
            for row in rowList:
                
                #The type column is the 5th column (would be at index 4 in the row)
                
                if row[4] == 'NaN':
                    #d is the counter dictionary that stores the associated types for weakness in this row
                    #weakness is the 6th element (index 5 of row)
                    d = w_t[row[5]]
                    sorted_d = sorted(d.items(), key=lambda item: (-item[1], item[0]))
                    type_value = sorted_d[0][0]
                    row[4] = type_value
                
                writer.writerow(row)
               
        
def method3_helper():
    
    #calculate the average value of the atk, def, hp for those rows whose level threshold is above 40
 
    atk_a40 = 0.0
    atk_a40_count = 0.0
    def_a40 = 0.0
    def_a40_count = 0.0
    hp_a40 = 0.0
    hp_a40_count = 0.0
    
    atk_b40 = 0.0
    atk_b40_count = 0.0
    def_b40 = 0.0
    def_b40_count = 0.0
    hp_b40 = 0.0
    hp_b40_count = 0.0
    
    with open('pokemonTrain.csv') as file:
        reader = csv.DictReader(file)
        
        
        for index, row in enumerate(reader):
            
            if float(row['level']) > 40:
                
                if row['atk'] != 'NaN':
                    atk_a40 += float(row['atk'])
                    atk_a40_count += 1
                
                if row['def'] != 'NaN':
                    def_a40 += float(row['def'])
                    def_a40_count += 1
                     
                if row['hp'] != 'NaN':
                    hp_a40 += float(row['hp'])
                    hp_a40_count += 1
                

            else:
                
                if row['atk'] != 'NaN':
                    atk_b40 += float(row['atk'])
                    atk_b40_count += 1
                
                if row['def'] != 'NaN':
                    def_b40 += float(row['def'])
                    def_b40_count += 1
                     
                if row['hp'] != 'NaN':
                    hp_b40 += float(row['hp'])
                    hp_b40_count += 1
           
         
    atk_a40_avg = round(atk_a40/atk_a40_count, 1)
    atk_b40_avg = round(atk_b40/atk_b40_count, 1)
    def_a40_avg = round(def_a40/def_a40_count, 1)
    def_b40_avg = round(def_b40/def_b40_count, 1)
    hp_a40_avg = round(hp_a40/hp_a40_count, 1)
    hp_b40_avg = round(hp_b40/hp_b40_count, 1)
    
    print('Average attack for above 40: ', str(atk_a40_avg))
    print('Average attack for below 40: ', str(atk_b40_avg))
    print('Average defense for above 40: ', str(def_a40_avg))
    print('Average defense for below 40: ', str(def_b40_avg))
    print('Average hit points for above 40: ', str(hp_a40_avg))
    print('Average hit points for below 40: ', str(hp_b40_avg))
    
    return atk_a40_avg, atk_b40_avg, def_a40_avg, def_b40_avg, hp_a40_avg, hp_b40_avg

def method3():
    
    atk_a40_avg, atk_b40_avg, def_a40_avg, def_b40_avg, hp_a40_avg, hp_b40_avg = method3_helper()
    
    #read in all the rows into a list
    #result: list of lists where each internal list is a row
    rowList = []
    with open('pokemonTrain.csv') as bfile:
        reader = csv.reader(bfile)
        for num,row in enumerate(reader):
            rowList.append(row) 
            
    
    #go through all the rows, 
    #fill in the entry of a missing atk, def, hp values according to the info recieved from the helper
    #write the row to the file
    
    
  
    
  
#testing
check()
method1()
method2()
method3()


        