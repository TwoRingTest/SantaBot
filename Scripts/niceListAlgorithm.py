import random #needed for random assignment
from typing import Dict, List

class Node(object):
# create a node that represents a person
    def __init__(self, name_list1, name_list2):
        self.to_list = list(name_list1)   #list of people that Node may be assigned to
        self.from_list = list(name_list2) #list of people that may be assigned to Node
        self.assigned_to = None          #track who Node is assigned to
        self.assigned_from = None        #track who is assigned to Node
   
    def removeEdgeFrom(self, node):      
    #remove a name from list of incoming edges to the node
        self.from_list.remove(node)
    
    def removeEdgeTo(self, node):       
    #remove a name from the list of outgoing edges from the node
        self.to_list.remove(node)
        
def permuteList(ordered_list: List):           
#ensure nondeterministic outputs
        old_list: List = list(ordered_list)
        new_list: List = []
        
        for i in range(len(old_list)):
            randIndex = random.randint(0, len(old_list) - 1)
            new_list.append(old_list.pop(randIndex))
         
        return new_list

def santaAssign(emails: List, not_allowed: List):
    nodeHash: dict = {}
    # dictionary mapping <name> to the Node that represents <name>
    emailsToList = permuteList(emails)
    emailsFromList = permuteList(emails) #randomize
    for email in emails:
        # create node, then ensure that a person is not assigned to themselves
        nodeHash[email] = Node(emailsToList,emailsFromList)
        nodeHash[email].removeEdgeFrom(email)
        nodeHash[email].removeEdgeTo(email)
        
    for i,j in not_allowed:
        # ensure compliance with restricted pairings
        nodeHash[i].removeEdgeTo(j)
        nodeHash[j].removeEdgeFrom(i)
        
    n: int = 0
    m: int = 0
    
    while True:
        # use depth first search to find a suitable assignment for everyone
        activeNode = nodeHash[emails[n]]
        if nodeHash[activeNode.to_list[m]].assigned_from == None:
            # assign the mth person on the nth persons to_list has been assigned, if they are available
            activeNode.assigned_to = activeNode.to_list[m]
            nodeHash[activeNode.assigned_to].assigned_from = emails[n]
            n += 1
            m = 0
            if n == len(emails):
            # if the algorithm has assigned someone to the nth person, then a solution has been found
                solution = []
                for email in emails:
                    solution.append((email,nodeHash[email].assigned_to))
                return solution
        elif m < len(activeNode.to_list) - 1:
            # if the mth person on the nth person's to_list was unavailable, increment m
            m += 1
        else:
            # if everyone on the nth person's to_list has been assigned, decrement n until an assignment can be made
            while True:
                n -= 1
                if n == -1:
                    # if the algorithm cycles backwards to the first person, and there is no one left on their to_list, then there is no solution
                    return "No solution available"
                activeNode = nodeHash[emails[n]]
                m = activeNode.to_list.index(activeNode.assigned_to) + 1
                nodeHash[activeNode.assigned_to].assigned_from = None
                activeNode.assigned_to = None
                if m < len(activeNode.to_list):
                    break
                
        
          
with open('dummy_data/emails.txt','r') as e_File:
    emailList = e_File.read().split()
    emailList = list(set(emailList))

with open('dummy_data/not_allowed.txt','r') as na_File:
    forbiddenPairsRaw = na_File.read().split()
    forbiddenPairsRaw = list(set(forbiddenPairsRaw))

forbiddenPairs = []
for i in range(len(forbiddenPairsRaw)):
    a, b = forbiddenPairsRaw[i].strip("()").replace("'","").split(',')
    forbiddenPairs.append((a,b))
    try:
        emailList.index(a)
    except ValueError:
        raise SystemExit("The name %r is in not_allowed.txt, but not in emails.txt" % a)
    try:
        emailList.index(b)
    except ValueError:
        raise SystemExit("The name %r is in not_allowed.txt, but not in emails.txt" % b)

print(emailList)
print(forbiddenPairs)
print(santaAssign(permuteList(emailList),forbiddenPairs))