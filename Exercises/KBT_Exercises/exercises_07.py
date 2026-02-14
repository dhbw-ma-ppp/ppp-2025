import pandas as pd
import numpy as np

path = "data/exercise_cave.txt"

df = pd.read_fwf(
    path,
    widths=[1] * 100,    
    header=None,       
    nrows=100,            
    dtype="int64"           
)

matrix = df.to_numpy()

class CaveEnvironment:
    def __init__(self, matrix):
        self.matrix = matrix
        self.pos = (0, 0)
        self.actions = ["up", "down", "left", "right"]
        self.goal = (99, 99)

    def step(self, action):
        row, col = self.pos

        if action == "up": row -= 1
        elif action == "down": row += 1
        elif action == "left": col -= 1
        elif action == "right": col += 1

        row = max(0, min(row, 99))
        col = max(0, min(col, 99))

        self.pos = (row, col)
   
        reward = -self.matrix[row][col]
        done = self.goal_reached()
        
        return self.pos, reward, done

    def goal_reached(self):
        return self.pos == self.goal

    def reset(self):
        self.pos = (0, 0)   
        return self.pos
    
def evaluate(Q, env, max_steps=500):
    state = env.reset()
    path = [state]
    total_cost = 0
    done = False
    steps = 0

    while not done and steps < max_steps:
        state_idx = state[0] * 100 + state[1]
        action_idx = np.argmax(Q[state_idx])
        action = env.actions[action_idx]

        state, reward, done = env.step(action)
        path.append(state)
        total_cost += -reward
        steps += 1

    print("Path length:", len(path))
    print("Total cost:", total_cost)
    print("Path:", path[:10], "...")


def training_loop(num_episodes=10000):
    env = CaveEnvironment(matrix)
    Qtable = np.zeros((100*100, 4))

    alpha, gamma = 0.1, 0.9
    epsilon = 1.0  # start with full exploration

    for episode in range(num_episodes):
        state = env.reset()
        state_idx = state[0] * 100 + state[1]
        done = False
        total_reward = 0
        steps = 0
        visited = set()

        while not done and steps < 500:  # step limit
            # ε-greedy action selection
            if np.random.rand() < epsilon:
                action_idx = np.random.randint(4)
            else:
                action_idx = np.argmax(Qtable[state_idx])

            action = env.actions[action_idx]
            next_state, reward, done = env.step(action)
            next_state_idx = next_state[0] * 100 + next_state[1]

            # Add penalties
            reward -= 0.1  # small penalty per step
            if next_state in visited:
                reward -= 1.0  # penalty for revisiting
            visited.add(next_state)

            # Q-learning update
            Qtable[state_idx, action_idx] += alpha * (
                reward + gamma * np.max(Qtable[next_state_idx]) - Qtable[state_idx, action_idx]
            )

            state_idx = next_state_idx
            total_reward += reward
            steps += 1

        # Decay epsilon slowly
        epsilon = max(0.01, epsilon * 0.999)

        # Log progress every 100 episodes
        if episode % 100 == 0:
            print(f"Episode {episode}, Total Reward: {total_reward}, Steps: {steps}")
            evaluate(Qtable, env)

    return Qtable

training_loop()

