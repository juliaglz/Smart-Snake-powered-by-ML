"""
Snake Eater Q learning basic algorithm
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""
import numpy as np
import random
import json
import time

class QLearning:
    def __init__(self, n_states, n_actions, alpha=0.5, gamma=0.9, epsilon=0.01, epsilon_min=0.01, epsilon_decay=0.999999):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.load_q_table()

    def choose_action(self, state, allowed_actions):
        if np.random.uniform(0, 1) < self.epsilon:
            action = random.choice(allowed_actions)  # Explore
        else:
            action = np.argmax(self.q_table[self.translate_state(state)])  # Exploit

        self.epsilon = max(self.epsilon_min, self.epsilon_decay * self.epsilon)
        return action

    def translate_state(self, state):
        # Convert the binary state list into a single integer
        if state == None:
            return None
        [food_dir_x, food_dir_y, horizontal_obstacle, vertical_obstacle] = state

        # Translate the tuple to a number
        number = (food_dir_x * 3 * 2 * 2 +
                  food_dir_y * 2 * 2 +
                  horizontal_obstacle * 2 +
                  vertical_obstacle)

        return number


    def update_q_table(self, state, action, reward, next_state):
        # Your code here
        # Update the current Q-value using the Q-learning formula
        # if terminal_state:
        # Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + 0)
        # else:
        # Q(state,action) <- (1-self.alpha) Q(state,action) + self.alpha * (r + self.discount * max a' Q(nextState, a'))
        row_state = self.translate_state(state)
        row_new = self.translate_state(next_state)
        old_value = self.q_table[row_state][action]
        if row_new == None:
            updatedQValue = (1 - self.alpha) * old_value + self.alpha * reward
        else:
            future_max = max(self.q_table[row_new])
            updatedQValue = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * future_max)
        self.q_table[row_state][action] = updatedQValue
    def save_q_table(self, filename="q_table.txt"):
        np.savetxt(filename, self.q_table)

    def load_q_table(self, filename="q_table.txt"):
        try:
            self.q_table = np.loadtxt(filename)
        except IOError:
            # If the file doesn't exist, initialize Q-table with zeros as per dimensions
            self.q_table = np.zeros((self.n_states, self.n_actions))
