from __future__ import print_function
from collections import deque  # you will use it for breadth-first search

class State:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.is_goal = False

    def add_action(self, action):
        self.actions.append(action)


class Action:
    def __init__(self, name, next_state, step_cost):
        self.name = name
        self.next_state = next_state
        self.step_cost = step_cost


class Node:
    #Class that represents nodes in the search algorithm. Use the
    #constructor to initialize the state, parent node, action at the parent
    #node and the path cost. In this homework, heuristic value is not used.
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost


class Problem:
    def __init__(self, name):
        self.__name = name
        self.__init_state = None
        self.__frontier = None
        self.__explored = None
        self.__goal_states = None

    def depth_first_search(self, init_state, goal_states):
        #Computes the depth-first search result from the initial state to the
        #goal state. When a goal node is drawn from the frontier list it is checked
        #if it is a goal node. If node.state is not a goal state it is explored
        #If it is a goal state it should return the value of self.__solution(goal_node).
        #Depth-first search needs a LIFO queue (stack) for the frontier variable.

        node = Node(init_state, None, init_state.actions, 0)
        if node.state == goal_states[0]:
            return self.self.__solution(node)

        self.__frontier = [node]
        self.__explored = []

        while self.__frontier:

            node = self.__frontier.pop() # pop the A from list to begin from it

            self.__explored.append(node.state.name) # ADD A (root) to explored list

            if node.state.name == goal_states[0].name:
                return self.__solution(node)

            for each in node.action: # for all childs
                child = Node(each.next_state, node, each.next_state.actions, each.step_cost + node.path_cost) # create the child
                if child.state.name not in self.__explored and child not in self.__frontier: # check the child if it is not in explored and frontier list
                    self.__frontier.append(child) # add it to frontier list
                    if child.state == goal_states[0]: # if it is G return the solution
                        self.__explored.append(child.state.name) # ADD the last item G even it is not explored.

            self.__print_diagnostics(node) # print every other nodes' diagnotics

    def breadth_first_search(self, init_state, goal_states):
        # Computes the breadth-first search result from the initial state to the
        # goal state. When a goal node is drawn from the frontier list it is checked
        # if it is a goal node. If node.state is not a goal state it is explored
        # If it is a goal state it should return the value of self.__solution(goal_node).
        # Breadth-first search needs a FIFO queue for the frontier variable.

        node = Node(init_state, None, init_state.actions, 0)

        self.__frontier = deque()
        self.__frontier.append(node)
        self.__explored = []

        while self.__frontier:
            node = self.__frontier.popleft() # pop the A from list to begin from it

            if node.state.name not in self.__explored:
                self.__explored.append(node.state.name)

            if node.state.name == goal_states[0].name:
                return self.__solution(node)

            for each in sorted(node.action, key=lambda obj: obj.next_state.name):
                child = Node(each.next_state, node, each.next_state.actions, each.step_cost + node.path_cost)

                if child.state.name not in self.__explored and child not in self.__frontier:
                    self.__frontier.append(child)
                    self.__explored.append(child.state.name)

            self.__print_diagnostics(node)

    def __solution(self, goal_node):
        # Returns a string representation of the solution containing the
        # state names starting from the initial state to the given goal node.
        # It should also contain information about the path cost although the
        # search methods implemented here do not use the cost while finding the goal.

        path = []
        path.append(goal_node)
        while goal_node.parent != None:
            path.append(goal_node.parent)
            goal_node = goal_node.parent
        return '->'.join([node.state.name for node in reversed(path)]) + " path_cost " + str(path[0].path_cost)

    def __print_diagnostics(self, node):
        print('Explored node ({0},{1})'.format(node.state.name, node.path_cost)) # + str(node.path_cost)
        print('  Frontier: {}'.format([(i.state.name, i.path_cost) for i in self.__frontier]))

    @staticmethod
    def connect_states(source_state, dest_state, step_cost):
        source_initial = source_state.name[0].lower()
        dest_initial = dest_state.name[0].lower()
        action_name = source_initial + dest_initial
        source_state.add_action(Action(action_name, dest_state, step_cost))

    @staticmethod
    def connect_states_both_ways(state0, state1, step_cost):
        Problem.connect_states(state0, state1, step_cost)
        Problem.connect_states(state1, state0, step_cost)


if __name__ == '__main__':
    a = State('A')
    b = State('B')
    c = State('C')
    d = State('D')
    e = State('E')
    f = State('F')
    g = State('G')

    Problem.connect_states_both_ways(a, b, 10)

    Problem.connect_states_both_ways(a, d, 15)
    Problem.connect_states_both_ways(b, c, 120)
    Problem.connect_states_both_ways(c, e, 70)
    Problem.connect_states_both_ways(c, g, 10)
    Problem.connect_states_both_ways(d, e, 40)
    Problem.connect_states_both_ways(e, f, 140)
    Problem.connect_states_both_ways(f, g, 20)

    problem = Problem('p1')

    print('*** Depth-First Search algorithm from a to g ***')
    print(problem.depth_first_search(a, [g]))

    print('*** Breadth-First Search algorithm from a to g ***')
    print(problem.breadth_first_search(a, [g]))

    print(' -------- A new link between a and f is added ----------')
    # Add a link between a and f with cost 50, then perform depth-first search
    # again for 'a' node to 'g' node.
    Problem.connect_states_both_ways(a, f, 50)
    print(problem.depth_first_search(a, [g]))
