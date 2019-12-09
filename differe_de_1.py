def differe_de_1(d) :

    couples=[]

    for i in d['itemsets'] :
        for j in d['itemsets'] :
            if d.loc[d['itemsets']==i].index[0]!=d.loc[d['itemsets']==j].index[0] :
               
                new_1=i.difference(j)
                new_2=j.difference(i)
                
                if len(new_1)==1 and len(new_2)==1:
                    
                    couples.append([[i.difference(new_1.union(new_2))],[new_1,new_2]])
                    
    return couples