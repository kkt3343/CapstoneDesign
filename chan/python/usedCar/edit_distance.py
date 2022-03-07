def edit_distance(first , second):
    first = first.encode(encoding='cp949')
    second = second.encode(encoding='cp949')
    
    first_len , second_len = len(first) , len(second) 
  
    if first_len > second_len : 
        first , second = second , first 
        first_len , second_len = second_len , first_len 
    current = range(first_len+1) 
  
    for i in range(1,second_len+1): 
        previous , current = current , [i]+[0]*second_len 
  
        for j in range(1,first_len+1): 
            add , delete = previous[j]+1 , current[j-1]+1 
            change = previous[j-1] 
            if first[j-1] != second[i-1]: 
                change = change + 1 
  
            current[j] = min(add , delete , change) 
  
    return current[first_len] 
