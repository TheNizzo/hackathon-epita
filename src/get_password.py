import csv

def find_correlation_group(letter, correlations):
    for i in range(len(correlations)):
        if letter in correlations[i]:
            return correlations[i]
    
    return [letter]    

def filter_out_repeting(list):
    results = []
    
    for elt in list:
        if len(results) < 2 or results[-1] != elt or results[-2] != elt:
            results.append(elt)
            
    return results   

def get_offset_i(reader, old_i, margin, correlations):
    mismatch_number = 0
    for i in range(old_i + 1, old_i + margin + 1):
        if len(reader) <= i or \
        set(find_correlation_group(reader[old_i][1], correlations)) == set(find_correlation_group(reader[i][1], correlations)):
            return mismatch_number
        
        else:
            mismatch_number += 1
            
    return mismatch_number
            

def filter_out_noise(reader, correlations):
    result = []
    last_letter = None
    last_trame = 0
    i = 1
    
    while i < len(reader):
        if last_trame + 13 < int(reader[i][0]):
            last_letter = None
            
        else:
            offset_i = get_offset_i(reader, i, 13, correlations)
            
            if offset_i != 0:
                last_letter = None
                i += offset_i
            
            else:
                last_letter = reader[i][1]
                  
        last_trame = int(reader[i][0])
        
        if last_letter != None:
            result.append([last_trame, last_letter])
        
        i += 1
    
    return result

def return_if_consecutive(data, consecutive, target):
    if consecutive >= target:
        return [data]
    return []
    
if __name__ == "__main__":
    correlations = [['q', 'w', 'a'],
                    ['h', 'u', 'b'],
                    ['e', 'd'],
                    ['r', 'v', 'f'],
                    ['t', 'y', 'g'],
                    ['p', 'm'],
                    ['x', 'SPACE', 's'],
                    ['SUPPR', '0'],
                    ['2', '3', '4', '1'],
                    ['7', '8', '5'],
                    ['9', '6']]

    with open("result_login_gnb.csv", newline='') as csvfile:
        results = []
        reader = list(csv.reader(csvfile, delimiter = ',', quotechar='|'))
    
        reader = filter_out_noise(reader, correlations)
    
        consecutive_trame = 0
        last_trame = 0
        last_correlation_group = None
    
        for row in reader:
            print(row[0])
        
            if last_trame + 1 != int(row[0]):
                results += return_if_consecutive(last_correlation_group, consecutive_trame, 5)
            
                consecutive_trame = 1
                last_correlation_group = find_correlation_group(row[1], correlations)
        
            else:
                correlation_group = find_correlation_group(row[1], correlations)
            
                if set(last_correlation_group) == set(correlation_group):
                    consecutive_trame += 1
            
                else:
                    results += return_if_consecutive(last_correlation_group, consecutive_trame, 5)
                
                    consecutive_trame = 1
                    last_correlation_group = correlation_group
        
            last_trame = int(row[0])
    
        results += return_if_consecutive(last_correlation_group, consecutive_trame, 5)
   
        print(filter_out_repeting(results))
