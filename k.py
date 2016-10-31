from __future__ import print_function


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

        node = Node(init_state, None, init_state.actions, 0)
        if node.state == goal_states[0]:
            return self.self.__solution(node)

        self.__frontier = [node]
        self.__explored = []

        while self.__frontier:
            if not self.__frontier:
                return "EMPTY?"

            node = self.__frontier.pop()
            # i = Action(State(""), )
            if node.state.is_goal != True:
                node.state.is_goal = True
                self.__explored.append(node.state.name)
                for each in node.action:
                    child = Node(each.next_state, node, each.next_state.actions, each.step_cost)
                    if child.state.name not in self.__explored and child not in self.__frontier:  # and node.state.is_goal != True:
                        self.__frontier.append(child)
                        if child.state == goal_states[0]:
                            self.__explored.append(child.state.name)
                            self.__solution(child)
                            self.__print_diagnostics(node)
                            return self.__explored
            self.__print_diagnostics(node)

        return self.__explored

    def __solution(self, goal_node):
        # Returns a string representation of the solution containing the
        # state names starting from the initial state to the given goal node.
        # It should also contain information about the path cost although the
        # search methods implemented here do not use the cost while finding the goal.
        solution = []
        solution.append(goal_node.state.name)
        return solution

    def __print_diagnostics(self, node):
        print('Explored node {}'.format(node.state.name))
        print('  Frontier: {}'.format([i.state.name for i in self.__frontier]))

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

    print([i for i in problem.depth_first_search(a, [g])])