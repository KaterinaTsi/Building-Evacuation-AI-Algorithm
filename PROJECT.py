import copy
 
  
# The world of the problem represented as a dictionary
# [lower floor from current, upper floor from current]
space = {
    0: ["start", 1],
    1: [0, 2],
    2: [1, 3],
    3: [2, 4],
    4: [3, 5],
    5: [4, "end"]
}

# Initial state
# List contents: [elevator floor, occupants 1st floor, occupants 2nd floor, occupants 3rd floor, occupants 4th floor, people in elevator]

state = [0, 9, 4, 12, 7, 0]
# Goal state
final_state = [5, 0, 0, 0, 0, 0]

###################################################
# Transition operators


def go_floor1(state):
    # Check if elevator has space and first floor has at least one occupant
    if state[5] < 8 and state[1] > 0:                 
        if state[1] > 8-state[5]:            # Check if all occupants can fit
            new_state = [1] + [state[1] + state[5] - 8] + [state[2]] + [state[3]] + [state[4]] + [8]    # Update state 
        else:                                                                                                # οροφο και τον αριθμο των ενοικων μεσα στο ασανσερ
            new_state = [1] + [0] + [state[2]] + [state[3]] + [state[4]] + [state[1] + state[5]]
        return new_state


def go_floor2(state):
    if state[5] < 8 and state[2] > 0:
        if state[2] > 8-state[5]:
            new_state = [2] + [state[1]] + [state[2] + state[5] - 8] + [state[3]] + [state[4]] + [8]
        else:
            new_state = [2] + [state[1]] + [0] + [state[3]] + [state[4]] + [state[2] + state[5]]
        return new_state


def go_floor3(state):
    if state[5] < 8 and state[3] > 0:
        if state[3] > 8-state[5]:
            new_state = [3] + [state[1]] + [state[2]] + [state[3] + state[5] - 8] + [state[4]] + [8]
        else:
            new_state = [3] + [state[1]] + [state[2]] + [0] + [state[4]] + [state[3] + state[5]]
        return new_state


def go_floor4(state):
    if state[5] < 8 and state[4] > 0:
        if state[4] > 8-state[5]:
            new_state = [4] + [state[1]] + [state[2]] + [state[3]] + [state[4] + state[5] - 8] + [8]
        else:
            new_state = [4] + [state[1]] + [state[2]] + [state[3]] + [0] + [state[4] + state[5]]
        return new_state


 # Move all occupants to the roof if elevator is full or all floors empty
def go_roof(state):
    if (state[5] == 8) or (state[5] < 8) and (state[1] + state[2] + state[3] + state[4] == 0):
        new_state = [5] + [state[1]] + [state[2]] + [state[3]] + [state[4]] + [0]
        return new_state

####################################################################################################################
# Function to find children (successor states)

def find_children(state):

    children = []     # Initialize empty list of children

    floor1_state = copy.deepcopy(state)           # Copy the current state to generate the first child
    floor1_child = go_floor1(floor1_state)        # Apply the first operator to create a new state

    floor2_state = copy.deepcopy(state)
    floor2_child = go_floor2(floor2_state)

    floor3_state = copy.deepcopy(state)
    floor3_child = go_floor3(floor3_state)

    floor4_state = copy.deepcopy(state)
    floor4_child = go_floor4(floor4_state)

    roof_state = copy.deepcopy(state)
    roof_child = go_roof(roof_state)

# Append non-None children to the list

    if floor1_child is not None:         
        children.append(floor1_child)   

    if floor2_child is not None:
        children.append(floor2_child)    

    if floor3_child is not None:
        children.append(floor3_child)

    if floor4_child is not None:
        children.append(floor4_child)

    if roof_child is not None:
        children.append(roof_child)

    return children                   

###############################################################################
# Initialize frontier


def make_front(state):
    return [state]


#############################################################################
# Expand frontier based on method


def expand_front(front, method):
    if method=='DFS' or method=='DFS-Q':
        if front:
            print("Front DFS:")
            print(front)
            node=front.pop(0)        # Remove the first state from the frontier for expansion
            for child in find_children(node):       # Find all children of the current state
                front.insert(0,child)        # Add children to the front for DFS
                          
    elif method=='BFS' or method=='BFS-Q':
          if front:
             print("Front BFS:")
             print(front)
             node=front.pop(0)
             for child in find_children(node):
                 front.append(child)            # Add children to the end of frontier for BFS
                
    elif method=='BESTFS':
         if front:
            print("Front BESTFS:")
            print(front)
            node = front.pop(0)
            for child in find_children(node):
                front.append(child)  # Add children to the end (to be sorted by heuristic later)
                
    return front

#############################################################################################
# Initialize queue for path-based search

def make_queue(state):
    return [[state]]

#######################################################################################
# Extend queue with new paths

def extend_queue(queue, method):
    if method=='DFS-Q':
        print("Queue:")
        print(queue)
        node=queue.pop(0)                  # Remove the first path from the queue  
        queue_copy=copy.deepcopy(queue)
        children=find_children(node[-1])   # Expand the last state in the current path (most recent child)
  
        for child in children:                    # For each child, create a new path including it
            path=copy.deepcopy(node)                # Copy the current path
            path.append(child)                    # Append the child to the path
            queue_copy.insert(0,path)             # Insert new paths at the front (DFS-Q) or end (BFS-Q) of the queue
            
    elif method=='BFS-Q':
        print("Queue:")
        print(queue)
        node=queue.pop(0)
        queue_copy=copy.deepcopy(queue)
        children=find_children(node[-1])
        for child in children:
            path=copy.deepcopy(node)
            path.append(child)
            queue_copy.append(path)       # For BFS-Q: append the new path at the end of the queue
    
    return queue_copy

######################################################################################################################################
# Heuristic function
# Computes the cost of each state in the frontier based on a heuristic
# Returns a list of costs to guide the selection of the next state to expand

def heuristic(front):
    h=[]        # List to store cost of each state
    
    for i in range(len(front)):            # Iterate through all states in the frontier
        count=0                                # Initialize score: 0 if floor empty, 1 if 0<people<8, 2 if overflow (>8)
        for k in range(1,5):              # Check floors 1 to 4 (ignore elevator floor at index 0)
            temp=front[i][k]/8             # Divide by elevator capacity to determine moves needed
            if temp == 0:
                count= count + 0        
            elif temp <= 1:
                count = count + 1
            elif temp > 1:                    # Each score represents the estimated elevator trips needed for an elevator that fits 8 people to a specific floor
                count = count + 2             # Sum scores to get the total heuristic for the state
           

            h.append(count)                 # Append the heuristic score for this state

                                         
        
    return h                            


########################################################################################################################
# Main recursive function to construct the search tree and find the solution path
# Parameters:
# - front: list of unexpanded states (the frontier)
# - closed: list of expanded states (states whose children have been generated)
# - goal: the target goal state
# - method: chosen search method (DFS, BFS, DFS-Q, BFS-Q, BESTFS)
# This function does not return a value; it prints the solution when found.

def find_solution(front, queue, closed, goal, method):  
   

    if not front:                           # If the state is already in the closed list, skip it
        print('_NO_SOLUTION_FOUND_')
        
    elif method=='DFS-Q' or method=='BFS-Q':
         if front[0] in closed:                          # If state is already in the front we erase from the front and call the quene retrospectively
             new_front=copy.deepcopy(front)              
             new_front.pop(0)
             new_queue=copy.deepcopy(queue)
             new_queue.pop(0)
             find_solution(new_front, new_queue, closed, goal, method)
           
             
         elif front[0]==goal:            # If goal state is found, stop the search
             print('_GOAL_FOUND_')
             print(front[0])
             print('Queue:')
             print(queue[0])
             print('PATH IS')
             print(closed)
            
             
         else:
             closed.append(front[0])
             front_copy=copy.deepcopy(front)
             front_children=expand_front(front_copy, method)   # επεκταση μετωπου
             queue_copy=copy.deepcopy(queue)
             queue_children=extend_queue(queue_copy, method)       # επεκταση ουρας
             closed_copy=copy.deepcopy(closed)
             find_solution(front_children, queue_children, closed_copy, goal, method) # καλουμε ξανα την συναρτηση με τις νεες παραμετρους 
                     
             

    elif front[0] in closed:                   # If current state is in closed, remove it and continue
        new_front = copy.deepcopy(front)
        new_front.pop(0)
        find_solution(new_front, 0, closed, goal, method)
        
        
        
    elif front[0] == goal:         # If current state is the goal, terminate
        print('_GOAL_FOUND_')
        print(front[0])
        print('PATH IS')
        print(closed)


    ##############################################
    elif method=='DFS' or method=='BFS':  
             closed.append(front[0])     # Add current state to the closed list       
             front_copy = copy.deepcopy(front)
             front_children = expand_front(front_copy, method)   # Expand frontier by adding children
             closed_copy = copy.deepcopy(closed)
             find_solution(front_children, 0, closed_copy, goal, method)
             
    ##########################################################################################         
             
    elif method=='BESTFS':
        closed.append(front[0])
        front_copy = copy.deepcopy(front)
        front_children = expand_front(front_copy, method)
        h_copy = heuristic(front_children)                    # Call heuristic function to get costs of frontier states
        x = h_copy.index(min(h_copy))                        # Find the state with the lowest cost
        y = front_children.pop(x)                            # Remove it from frontier
        front_children.insert(0,y)                            # Insert it at the front to prioritize expansion
        closed_copy = copy.deepcopy(closed)
        find_solution(front_children, 0, closed_copy, goal, method)
        
        

#######################################################################################
# Main execution
def main():
    initial_state = [0, 9, 4, 12, 7, 0]
    goal = [5, 0, 0, 0, 0, 0]
    

    method = input('ENTER DFS OR BFS OR DFS-Q OR BFS-Q OR BESTFS:')

    print('____BEGIN__SEARCHING____')
    
    if method=='DFS-Q' or 'BFS-Q':
                 find_solution(make_front(initial_state), make_queue(initial_state), [], goal, method)
    
    else:
        find_solution(make_front(initial_state), 0, [], goal, method)       # Start search without queue for simple DFS/BFS
   


if __name__ == "__main__":
    main()

