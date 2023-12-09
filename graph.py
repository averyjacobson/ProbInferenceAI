import random

class Graph:

    #Create graph object
    def __init__(self, inputFile):
        
        #Nodes list
        self.nodes = []

        with open(inputFile, 'r+') as f:
            for line in f:
                
                #Check if variable
                if "variable" in line:
                
                    nodeName = line.split(' ')[1]
                    variableLine = next(f)

                    #Grab String between {}
                    res = self.strGraber(variableLine,'{','}')
                
                    #Split string into list items
                    res = res.split(",")
                    for domain in range(len(res)):
                        res[domain] = res[domain].strip()

                    #Add to node list
                    self.nodes.append(Node(nodeName,res))

                #Check if CPT table
                elif "probability" in line: 
                    probLine = line
                    
                    #Grab String between ()
                    dependentVars = self.strGraber(probLine,'(',')')

                    #Split string into elements of list
                    dependentVars = dependentVars.split("|")

                    #The probability we're looking for
                    probVar = dependentVars[0].strip()
                    
                    #If top layer, evidence is the variable
                    if len(dependentVars) == 1:
                        evidence = dependentVars[0].strip()

                    #If not put evidence into list
                    if len(dependentVars) > 1:
                        evidence = dependentVars[1].split(",")
                        for i in range (len(evidence)):
                            evidence[i] = evidence[i].strip()

                    CPT = ConditionalProbabilityTable(probVar, evidence)

                        


                #Grab next line
                probLine = next(f)
                
                #Iterate through table
                while "}" not in probLine:

                    #Check if table
                    if "table " in probLine:

                        key = "table"
                        values = ''

                        #Grab table values
                        for idx in range(7, len(probLine) -2):
                            values = values + probLine[idx]

                        #Add values to list
                        values = values.split(",")
                        for i in range(len(values)):
                            values[i] = values[i].strip()
                        
                        #Update CPT
                        CPT.map[key] = values
                    
                    #Normal CPT table
                    else:
                        
                        #Key
                        idx1 = probLine.index('(')
                        idx2 = probLine.index(')')

                        key = ''
                        for idx in range(idx1 + 1, idx2):
                            key = key + probLine[idx]

                        #Values
                        values = ''

                        for idx in range(idx2 + 1, len(probLine) -2):
                            values = values + probLine[idx]

                        values = values.split(",")
                        for i in range(len(values)):
                            values[i] = values[i].strip()

                        CPT.map[key] = values
                    

                    #Grab next line
                    probLine = next(f)
                
                    for node in self.nodes:
                        if node.name == probVar:
                            node.cpt = CPT 
                            for evidenceName in evidence:
                                for evNode in self.nodes:
                                    if evNode.name == evidenceName:
                                        if evNode not in node.parents:
                                            node.parents.append(evNode)

    #Grab string between two characters
    def strGraber(self, inputStr, startChar, endChar):
        idx1 = inputStr.index(startChar)
        idx2 = inputStr.index(endChar)        
        res = ''            
        for idx in range(idx1 + len(startChar + endChar), idx2):
            res = res + inputStr[idx]
        return res


    def __str__(self):

        for node in self.nodes:
            
            print("Variable: ", node.name)
            print("Values: ", node.domain)
            print("Current Value: ", node.value)
            print("CPT table: \n")
            
            print("Probability of", node.name , "given", node.cpt.evidence)
            
            print(node.cpt.map)
          
            print("_______________________________________________________")
            print()
        return "\n"
    
    def getApproximateProbability(self, statement, iterations): 
        # Get the conditional probability from a CPT given a variable(Node) and evidence(List<Node>)
        statementNodes = list()
        evidenceNodes = list()

        # parse statement I.E "HYPOVOLEMIA, LVFAILURE, ERRLOWOUTPUT | HRBP=HIGH; CO=LOW; BP=HIGH"
        statement = statement.replace(" ", "")
        statement = statement.split("|")
        variables = statement[0].split(",")
        eVariables = statement[1].split(";")

        # find corresponding Node
        for node in self.nodes:
            for varName in variables:
                if node.name == varName:
                    statementNodes.append(node)
            for evarName in eVariables:
                if node.name == evarName.split("=")[0]:
                    #This updates evidence Values
                    node.value = evarName.split("=")[1]
                    evidenceNodes.append(node)
        #Generate Init State
        self.setInitialState(evidenceNodes)
        #Perform sampling for N iterations
        for i in range(iterations):
            if i < 200:
                #burnIn
                self.GibbsSample(evidenceNodes, True)
            else:
                self.GibbsSample(evidenceNodes, False)
                
        #Return Query values
        for query in statementNodes:
            if query not in evidenceNodes:
                totalIterations = 0
                for num in query.counts:
                    totalIterations += num
                print(query.name+ ": ", query.domain[query.counts.index(max(query.counts))], str(100*max(query.counts)/totalIterations)+ "% Probability")
            else: 
                print(query.name+ ": ", query.value+ "  100% Probability")


    def setInitialState(self, evidenceNodes):
        # Start with an initial state for the unobserved (hidden) variables by random sampling
        for node in self.nodes:
            if node not in evidenceNodes: #evidence nodes remain fixed
                if len(node.parents) == 0: #if discrete table exists, use weighted sampling
                    node.value = weightedSample(node, "table")
                else: #if parents exist, take random
                    node.value = node.domain[random.randrange(0,len(node.domain) -1)]
  
    def GibbsSample(self, evidenceNodes, burnIn):
        #select random unobserved variable
        randVar = random.choice(self.nodes)
        while randVar in evidenceNodes:
            randVar = random.choice(self.nodes)
        # print(randVar.name +": "+ randVar.value)
        if len(randVar.parents) == 0:
            #what to do if no parents? weighted sampling
            randVar.value = weightedSample(randVar, "table")
            #increment the count of each value chosen
            if not burnIn:
                randVar.counts[randVar.domain.index(randVar.value) -1] += 1

        else:
            key = ''
            for parent in randVar.parents:
                key += str(parent.value) + ", "
            key = key[:-2] #remove trailing ', '
            randVar.value = weightedSample(randVar, key)
            #increment the count of each value chosen
            # print(randVar.domain.index(randVar.value))
            randVar.counts[randVar.domain.index(randVar.value) -1] += 1
        #     print("Parent Values: "+key)
        # print("Adjusted Value: "+ randVar.value)
    
    def getExactProbability(self,query,evidence):

        

        factors = []

        for node in self.nodes:
            newFactor = Factor()
            newFactor.name.append(node.name)
            
            for parentName in node.parents:
                newFactor.parents.append(parentName.name)    

            newFactor.cpt = node.cpt
            factors.append(newFactor)

        for factor in factors:
            print(factor)

        # print("END OF FACTORS")

        elimOrder = self.eliminationOrder(query,factors)

        


        for eliminationVariable in elimOrder:
            print("Eliminating", eliminationVariable)
            factorsToJoin = []
            for factor in factors:
                if factor.contains(eliminationVariable):
                    factorsToJoin.append(factor)

            joinedFactor = self.join(factorsToJoin,eliminationVariable)

            
        

            

                 
        
            

    def join(self,factorsToJoin,joiningOn):

        #Get list of variables
        listOfVariables = []
        for factor in factorsToJoin:
            for variable in factor.combinedList():
                if variable not in listOfVariables:
                    listOfVariables.append(variable)

        #Get domain of node being joined on
        for node in self.nodes: 
            if node.name == joiningOn:
                domain = node.domain


        for factorObj in factorsToJoin:
            if factorObj.name == joiningOn:
                print("")
                
        for factor in factorsToJoin:
            #Check if top layer variable
            if len(factor.parents) == 0:
                print("Top layer elimination")
                newFactor = Factor()
                if len(factorsToJoin) == 2:
                    print("joining")
                    

        

        
            

        

    def eliminationOrder(self,query,factors):
        
        elimOrder = []



        for node in self.nodes:
            if not (query == node.name):

                elimOrder.append(node.name)

        

        removeList = []

        for eliminationVariable in elimOrder:
            occursCount = 0
            
            
            for factor in factors:
                
                if factor.contains(eliminationVariable):
                    occursCount += 1
                    
                   

            if occursCount == 1 :
                removeList.append(eliminationVariable)
                
            occursCount = 0

        
        elimOrder = list(set(elimOrder) - set(removeList))

        # print("Elim",elimOrder)
        # print("Removed",removeList)    
        
        return elimOrder
        




class Node:

    def __init__(self,name, positions):
        self.name = name
        self.domain = positions 
        self.counts = [0] * len(positions)
        self.value = None
        self.parents = list()
        self.cpt = None
        self.value = None


class ConditionalProbabilityTable:

    def __init__(self, var, evi):
        self.variable = var
        self.evidence = evi
        self.map = dict()

    def __str__(self):
        print(self.map)
        return("")
        


def weightedSample(node, key):
    cumulativeProb = 0
    randNum = random.random()
    for index, value in enumerate(node.cpt.map[key]):
        cumulativeProb += float(value)
        if randNum <= cumulativeProb:
            selectedIndex = index
            break
    return node.domain[selectedIndex]



class Factor:

    def __init__(self):
        
        self.name = []
        
        self.parents = []

        self.cpt = None

    


    def __str__(self):
        if self.parents:
            hasParents = "|" 
        else:
            hasParents = ""
        

        print("F(", self.name, hasParents,self.parents,")"  )

        #print("CPT Table:")
        #print(self.cpt)
        return("")
    
    def combinedList(self):
        return self.parents + self.name

    def contains(self,comparison):
        combined = self.combinedList()

        if comparison in combined:
            return True
        else:
            return False

    
        