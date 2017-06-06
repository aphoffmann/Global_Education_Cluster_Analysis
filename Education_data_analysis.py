#!/usr/local/anaconda/bin/python
# Alex Hoffmann

import csv
from math import sqrt

######################################################################
class Vector(list):
    def __init__(self, *args):
        '''Constructor invokes list constructor on the collection of args given.'''
        list.__init__(self, list(args))

        # Make Vector's printed representation look pretty.
    def __repr__(self):
        '''Replace standard list brackets with angle brackets.'''
        S = list.__repr__(self)
        return('<{0}>'.format(S[1:len(S)-1]))

    def magnitude(self):
        '''Returns scalar magnitude of self.'''
        return(sqrt(sum( [ val*val for val in self ])))

    def normalize(self):
        '''Normalize self to unit magnitude.'''
        mag = self.magnitude()
        if mag > 0:
            for i in range(len(self)):
                self[i] = self[i]/mag 

    # zip() used to simplify the code.
    def dproduct(self, other):
        '''Dot product of self and another vector.'''
        return(sum([ pair[0]*pair[1] for pair in zip(self,other) ]))

    def eproduct(self, other):
        '''Finds Euclidian distance between two x-dimensional Vectors'''
        #Normalize Vectors 
        self.normalize() 
        other.normalize()
        
        eList = [] #accumulates squared differences
        x = 0
        while x < len(self) and x < len(other):
            eList.append((self[x] - other[x])**2)
            x +=1
        
        #Find edistance
        edistance = sqrt(sum(eList))
        return(edistance)
        

######################################################################
class Dataset():
    def __init__(self, codefile='codes.csv', defnfile='defn.csv', datafile='data.csv'):
        '''Initialize Attributes, Trigger Data Collection, Normalize Data'''
        #Data containing Attributes
        self.V = {}
        self.P = {}
        self.D = {}
        self.C = {}
        
        #Used in Normalization
        self.means = {}
        self.stddev = {}
        
        #Read Data
        self.readDefinitions(defnfile)
        self.readCodes(codefile)
        self.readData(datafile)
                
        #Create P             
        self.P = {series:len(self.V[series]) for series in self.V}
    
        #Helper Functions. Put them here instead of as methods to play on autograders safe side
        def findVariables(self):
            '''Finds means and standard deviations'''        
            for series in self.V:
                strd = 0.0            
            #find the mean
                values = [float(x) for x in self.V[series].values() if x != ".."]
            
                if len(values) <= 1:
                    continue  
                
                mean = sum(values)/len(values)
                self.means.update({series:mean})
        
                #find the standard deviation
                strd = sqrt(sum([(float(x) - mean)**2 for x in self.V[series].values() if x != ".."])/(len(values)-1))
                self.stddev.update({series:strd})
            
        def featureNormilization(self): 
            '''Traverses V and normalizes data points with respect to series'''     
            for series in self.V:      
                for value in self.V[series]:
                    if self.P[series] < 2 or self.stddev[series] == 0:
                        self.V[series][value] = 0
                        continue
               
                    #set Z-score
                    self.V[series][value] = (float(self.V[series][value]) - self.means[series]) / self.stddev[series]
        
        #Calls Hellper function
        findVariables(self)
        featureNormilization(self) 
       
        
        
    def readDefinitions(self, filename):
        # Open the filename for reading.
        with open(filename, newline='', encoding='latin-1') as file:
             # Use csv reader.
            reader = csv.reader(file)
            # Skip the header!
            next(reader)
            # Process each row.
            for row in reader:
                self.D[row[0]] = row[1:2]
                # Ugly fix for badly formatted World Bank file where
                # double quotes in string were not properly escaped.
                self.D[row[0]].append(' '.join([ x.rstrip('"') for x in row[2:-1] ]).rstrip('"'))
                self.D[row[0]].append(row[-1])


    def readCodes(self, filename):
        '''Creates a dict C of {Country Code : (Country, Region)} from filename'''
        
        with open(filename, newline='', encoding='latin-1') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.C[row[0]] = (row[1], row[2])
        
    def readData(self, filename):
        '''Creates dicts V and P from data in filename'''
        with open(filename, newline='', encoding='latin-1') as file:
            reader = csv.DictReader(file, fieldnames = ("Country", "Country Code", "Series", "Series Code", "2015 [YR2015]"))
            #skip Header            
            next(reader)
            for row in reader:
                #create V
                #checks if series code is already in dictionary
                if row["Series Code"] in self.V and row["2015 [YR2015]"] != "" and row["2015 [YR2015]"] != ".." and row["Country Code"] in self.C:
                    self.V[row["Series Code"]].update({row["Country Code"]:row["2015 [YR2015]"]})
                
                #if not in dictionary, add to dictionary
                elif row["2015 [YR2015]"] != "" and row["2015 [YR2015]"] != ".." and row["Country Code"] in self.C:
                    self.V[row["Series Code"]] = {row["Country Code"]:row["2015 [YR2015]"]}                
                
        
                
######################################################################
class Analysis():
    def __init__(self, D, j=5):
        '''Creates Dictionary keyed to country of vectors representing j most common series self.U
        Create a dictionary keyed to country of lists of the most similar countries with respect to their vectors'''
        self.C = D.C # give KNN access to country name and region
        self.P = list(sorted(D.P, reverse=True, key=lambda x: D.P[x]))[:j] # Creates list P of j most common series
        self.U = {country:Vector() for  country in D.C} # creates U
        
        #Cycle through D.V appending to vectors in U indexed by country
        for country in self.U:
            for series in self.P:
                if country in D.V[series]:
                    self.U[country].append(D.V[series][country])
                else:
                    self.U[country].append(0)
            
            #Remove if magnitude == 0
            if self.U[country].magnitude() == 0:
                self.U.pop('country', None)
            else:
                self.U[country].normalize()
            
        self.E = {country:sorted([(self.U[country].eproduct(self.U[a]), a) for a in self.U if a != country ], key=lambda x: x[0])
                 for country in self.U}

            
    def KNN(self, target, k=5):
        '''a K-nearest neighbor search algorithm that takes two parameters,
        a target country code target and an integer count k
        and returns a list of k tuples (country code, distance, country, region)'''
        return([i + self.C[i[1]] for i in self.E[target][:k]])
    
    
    
    
    
