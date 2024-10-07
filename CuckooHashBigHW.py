from BitHash import *
import random 
#"I hereby certify that this program is solely the result of my own work and 
#is in compliance with the Academic Integrity policy of the course syllabus 
#and the academic integrity policy of the CS department.”

#The Hash table contains Link Objects and this class defines those objects
#that will be inserted into the Hash Table 
class Link(object):
    def __init__(self,key,data):
        self.__key = key
        self.__data = data
        
    def getKey(self):
        return self.__key
    
    def getData(self):
        return self.__data 
    
    def __str__(self):
        return str(self.__key) + "," + str(self.__data)
    
class CuckooHashTable(object): 
        
    def __init__(self, size: int):
        
        self.__hashArray1: list = [None] * (size) #primary hash array
        self.__hashArray2: list[Link] = [None] * (size) #secondary hash array
        self.__numLinks: int = 0 #number of actual items in the hashTable (s)


    #grows the hash Tables if they are too full 
    #hashes the link to it's correct table 1 position and places it in
    def __rebuild(self): 
        
        ResetBitHash() #reset the hashing 
        newLength: int = len(self.__hashArray1) * 2 #growing the arrays to this length
        listAllLinks: list = [] #stores the links from both hash Arrays
    
        #gets together all of the links from the original hash arrays into a list
        for i in range(len(self.__hashArray1)):
            if self.__hashArray1[i] is not None:
                listAllLinks +=[self.__hashArray1[i]]
                    
            if self.__hashArray2[i] is not None:
                listAllLinks +=[self.__hashArray2[i]]
        
        #remake the hasharrays  with their new length           
        self.__hashArray1 = [None  for i in range(newLength)] 
        self.__hashArray2 = [None for i in range(newLength)]  
        self.__numLinks = 0
        
        
        #insert all of the keys into the appropriate hash arrays 
        for i in range(len(listAllLinks)):
            self.insert(listAllLinks[i].getKey(), listAllLinks[i].getData())
            
 
    #hashes the link into the appropriate position in the first table
    #if something else is there, it's placed into the next table 
           #while a link evicts another, this process is continued 
           #if this happens a certain number of times then the rebuild function
           #is called 
     
    #This function inserts key,data pairs into the HashTable by hashing
    #it into the appropriate place and moving what's already there into the other
    #Hash Tableif something is there. if this process continues 100 times
    #then the lists will be grown using the __rebuild function
    #if the key is already in the HashTable, it won't
    #be inserted and the function will return false, otherwise it will 
    #return True
    def insert(self, key, data) -> bool:
        
        link: Link = Link(key, data) #make a link out of the key,data pair
        
        #only inserts unique key,data pairs into the Cuckoo Hash Table  
        if self.find(link) is not None:
            return False 
        
        else:
            bucket1: int = BitHash(link.getKey(), 1) % len(self.__hashArray1) #hash into first array
            temp: Link = None #will be used to store existing link if it exists 
            
            
                
            #if a link already is in that position place it into the temp variable
            if self.__hashArray1[bucket1] is not None: 
                temp = self.__hashArray1[bucket1] 
                
            self.__hashArray1[bucket1] = link #put the new link in that position
            
            #if there was a link that was "kicked out"
            if temp is not None: 
                count: int = 0
                
                #while there is a link that's supposed to be in the table that isn't 
                while temp is not None :
                    count += 1
                                
                    
                                    
                    #look in the second table every other time
                    if count % 2 != 0: 
                        bucketF2 = BitHash(temp.getKey(),2) % len(self.__hashArray2) 
                        #store the link that's about to be placed in the table
                        link = temp 
                        
                        #if there's a link to be kicked out store it in the temp variable
                        if self.__hashArray2[bucketF2] is not None: 
                            temp = self.__hashArray2[bucketF2] 
                            
                        #otherwise tell the code it's done  
                        else: 
                            temp = None 
                        
                        #put the link in it's proper place
                        self.__hashArray2[bucketF2] = link 
                      
                    #look in the first table every other time   
                    else: 
                        #same process except being done in the first table
                        bucketF1 = BitHash(temp.getKey(),1) % len(self.__hashArray1)
                        link = temp
                        
                        if self.__hashArray1[bucketF1] is not None:
                            temp = self.__hashArray1[bucketF1] 
                            
                        else:
                            temp = None
                        
                        self.__hashArray1[bucketF1] = link    
                        
                    
                    
                    
                    #if it looks like we are getting into an infinite loop
                    if temp is not None and count > 100:
    
                        #reset the count 
                        count = 0
                        
                        #rebuild the table 
                        self.__rebuild()
                        
            #update the length of the cuckoo hash table 
            self.__numLinks += 1    
            return True    
  
  
    #the find function looks for the link in it's expected location in both 
    # of the two tables  if the link is found in either table, the function returns 
    #the data of that link 
    #otherwise it returns None
    
    def find(self, link):
        #hash into first array
        bucket1: int = BitHash(link.getKey(),1) % len(self.__hashArray1) 
        
        #hash into second array
        bucket2: int = BitHash(link.getKey(),2) % len(self.__hashArray2) 
        
        #if the first location has the link we are looking for return it's data
        if self.__hashArray1[bucket1] is not None:
            if self.__hashArray1[bucket1].getKey() == link.getKey(): 
                return link.getData()
        
        #if the second location has the link we are looking for return it's data
        if self.__hashArray2[bucket2] is not None:
            if self.__hashArray2[bucket2].getKey() == link.getKey(): 
                return link.getData()  
        
        
        #otherwise, the link hasn't been found, and it should return None 
        else: 
            return None  
    
    
    #a function that will delete a given link if it is found in 
    #either position in the table that it's expected to be found in
    #returns True if a deletion has occured and False if not.
    
    def delete(self, link: Link) -> bool: 
        bucket1 = BitHash(link.getKey()) % len(self.__hashArray1)
        bucket2 = BitHash(link.getKey()) % len(self.__hashArray2)
        
        #if it's found in the first table delete it from that table 
        #decrement the number of links in the Hash Table and return True
        if self.__hashArray1[bucket1] == link:
            self.__hashArray1[bucket1] = None 
            self.__numLinks -= 1
            return True 
        
        #if it's found in the second table do the same process as before for the second table instead
        elif self.__hashArray2[bucket2] == link: 
            self.__hashArray2[bucket2] = None
            self.__numLinks -= 1
            return True
        
        #if it isn't found then a deletion won't occur
        else: 
            return False 
            
     
    # modifies the length() function to set the length of the cuckoo hash table
    #to the number of links that have been inserted in the two underlying hash
    #tables 
    
    def __len__(self) -> int:
        return self.__numLinks;
    
    
    #modifies the str() function to allow the cuckoo hash table to be printed
    #out in a way that humans can see what is going on in the table 
    def __str__(self) -> str:
        listLinks1: str = "" 
        listLinks2: str  = ""
        
        #converts the underlying Hash Arrays into understandable strings 
        for i in range(len(self.__hashArray1)):
            if self.__hashArray1[i] is not None:
                listLinks1 +="["  + str(self.__hashArray1[i]) + "]" + " " 
                    
            if self.__hashArray2[i] is not None:
                listLinks2 += "[" + str(self.__hashArray2[i]) + "]" + " "
           
        #return those underlying Hash Arrays     
        return "table 1: " + listLinks1 + "\ntable 2:" + listLinks2 
        
        
#gentle test         
def main():
    #build a table
    test: CuckooHashTable = CuckooHashTable(100)
    
    #add in a bunch of values and display them
    for i in range(80):
        test.insert(random.randint(1,20),i)
        print(test)
    print(len(test))
  
        

if __name__ == "__main__":
    main()
       