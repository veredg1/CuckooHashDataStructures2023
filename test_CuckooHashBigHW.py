from CuckooHashBigHW import * 
import BitHash
import pytest
import random 

#tests that nothing will be found in an empty table by choosing random 
#values to try and find
def test_emptyHashTable():
   test: CuckooHashTable = CuckooHashTable(1)
   
   assert test.find(Link(0,0)) == None
   assert test.find(Link(1,0)) == None
   assert test.find(Link("hi", "link")) == None
   
#a simple test with a simple table that just tests if the right number 
#of items are found in the table 
def test_simpleTable():
   test: CuckooHashTable = CuckooHashTable(100)
    
   count = 0
   for i in range(100):
      if(test.insert(i,i)):
         count += 1
       
      assert len(test) == count
    
   countNew = 0
   for i in range(100):
      if test.find(Link(i,i)) is not None:
         countNew += 1
        
      assert len(test) == count
    
        
#table with random numbers that tests if the right values are inserted 
#by placing the values inserted into the hash table in a dictionary, and making
def test_randomTable():
   test: CuckooHashTable = CuckooHashTable(1000)
    
   count: int = 0
   listRand = [(random.randint(1,100),i) for i in range(100) ]
   
   #the fake hash table
   d: dict() = {}
   for i in range(100):
      if(test.insert(listRand[i],i)):
         #put the values in the fake hashtable
         d[listRand[i]] = i
        
   #check that the values in the fake hashTable are found in the real 
   #hashtable as well
   for key in d.keys():
      assert test.find(Link(key, d[key])) == d[key]
         
      
        
 
#same test as above but with more, and random number of values being inserted into the HashTable 
def test_randomTableNumbers():
   test: CuckooHashTable = CuckooHashTable(1000)
   
   #create a list that will store the values being generated
   listRand = []
   for i in range(random.randint(500,10000)):
      intNew = random.randint(1,1000)
      listRand += [intNew]
   
   #make the fake dictionary and fill it as the cuckooHashTable is being filled
   d = dict()
   for i in range(len(listRand)):
      if test.insert(listRand[i],i) is not None:
         d[listRand[i]] = i
    
   #check that the real and fake cuckooHashTable match    
   for key in d.keys():
      assert test.find(Link(key, d[key])) == d[key]
        
    
 #same test as the above test but with random letters 
 #being tested as well as numbers
def test_randomTableNumbersandLetters():
   test: CuckooHashTable = CuckooHashTable(10000)
   listRand = []
   for i in range(5):
      for i in range(random.randint(5000,10000)):
         newVal = [random.choice("1234567890abcdefghijklmnopqrstuvwxyz") for i in range(random.randint(1,10))]
         listRand += [newVal]
      
      
      d = dict()
      for i in range(len(listRand)):
         string = str(listRand[i])
         if test.insert(string,i) is not None:
            d[string] = i
           
      for key in d.keys():
         assert test.find(Link(key, d[key])) == d[key]
      
 
   
#torture test: same idea as the above tests, but makes a table of a size between
#100 and 10000 and inserts  between 100 and 10000 random numbers or letters 
#that have a length of between 1 and 20 (as keys), converted into a string
#with a random letter as the accompanying data and
#tries this between 1 and 10 times 
def test_torture1():
   test: CuckooHashTable = CuckooHashTable(random.randint(100,10000))
   listRand = []
   for i in range(random.randint(1,10)):
      for i in range(random.randint(100,10000)):
         newVal = [random.choice("1234567890abcdefghijklmnopqrstuvwxyz") for i in range(random.randint(1,20))]
         listRand += [newVal]
      
      
      d = dict()
      for i in range(len(listRand)):
         string = str(listRand[i])
         if test.insert(string,i) is not None:
            d[string] = random.choice("abcdefghijklmnopqrstuvwxyz")
           
      for key in d.keys():
         assert test.find(Link(key, d[key])) == d[key]
      
#torture test 2: similar to the other torture test, except each thing 
#inserted is only a number or a letter, and the data value is a random 
#number between 1 and 100 
def test_torture2():
   test: CuckooHashTable = CuckooHashTable(random.randint(100,1000))
   
   for i in range(random.randint(1,10)):
      listRand = []
      for i in range(random.randint(1000,5000)):
         newVal = random.choice("1234567890abcdefghijklmnopqrstuvwxyz")
         listRand += [newVal]
      
      
      d = dict()
      for i in range(len(listRand)):
      
         if test.insert(listRand[i],i) is not None:
            d[listRand[i]] = random.randint(1,100)
           
      for key in d.keys():
         assert test.find(Link(key, d[key])) == d[key]

pytest.main(["-v","-s","test_CuckooHashBigHW.py"])
