"""
Code used to solve MountainCar-v0 gymnasium problem using Q-Learning algorithm
"""
from datetime import datetime
import gymnasium as gym
import numpy as np


def initialize_environment():
    """
    Initialize environment and video recording
    """
    # Initialize environment
    env = gym.make('MountainCar-v0', render_mode='rgb_array')
    # Save video
    now = datetime.now()
    time_string = now.strftime("%H:%M:%S")
    env = gym.wrappers.RecordVideo(
        env,
        video_folder='vid',
        episode_trigger=lambda x: x == 1,
        disable_logger=False,
        name_prefix=time_string)
    return env


def initialize_q_table(env):
    """
    Initialize "empty" Q-table
    """
    # Initialize Q-table
    n_actions = env.action_space.n  # Number of possible actions, should be 3
    # 0 accelerate left
    # 1 dont accelerate
    # 2 accelerate to the right
    q_table = np.zeros((n_actions,))
    return q_table


def initialize_hyperparameters():
    """
    Initialize hyperparameters used by algorithm
    """
    hyperparameters = {
        "learning_rate": 0.1,
        "discount_factor": 0.99,
        "epsilon": 0.2,
        "max_episodes": 1
    }
    return hyperparameters


def choose_action(hyperparameters, env, q_table):
    """
    Choose one of 3 actions possible for the algorithm
    """
    # hyperparameters["epsilon"]-greedy exploration-exploitation tradeoff
    if np.random.uniform(0, 1) < hyperparameters["epsilon"]:
        action = env.action_space.sample()  # Choose a random action
    else:
        # Choose the action with the highest Q-value
        action = np.argmax(q_table)
    return action


def update_q_table(q_table, action, hyperparameters, reward):
    """
    Update q_table with newest reward
    """
    # Q-table update
    q_value = q_table[action]
    max_q_value = np.max(q_table)
    new_q_value = (1 - hyperparameters["learning_rate"]) * q_value + \
        hyperparameters["learning_rate"] * \
        (reward + hyperparameters["discount_factor"] * max_q_value)
    q_table[action] = new_q_value
    return q_table


def movement(hyperparameters, env, q_table, total_reward=0):
    """
    Choose action and observe consequences
    """
    action = choose_action(hyperparameters, env, q_table)
    # Take the action and observe the next state
    _, reward, terminated, truncated, _ = env.step(action)
    done = terminated or truncated
    q_table = update_q_table(q_table, action, hyperparameters, reward)

    total_reward += reward
    return hyperparameters, env, q_table, done, total_reward


def episode_step(env, hyperparameters, q_table, episode_rewards):
    """
    Actions done with every episode
    """
    env.reset()  # Reset the environment to an initial state
    done = False  # Boolean to indicate episode completion
    total_reward = 0  # Accumulate rewards for the episode

    while not done:
        hyperparameters, env, q_table, done, total_reward = movement(
            hyperparameters, env, q_table, total_reward)

    episode_rewards.append(total_reward)
    return env, hyperparameters, q_table, episode_rewards


def training_loop(hyperparameters, env, q_table):
    """
    Actual training for MountainCar
    """
    episode_rewards = []  # List to store episode rewards

    for _ in range(hyperparameters["max_episodes"]):
        env, hyperparameters, q_table, episode_rewards = episode_step(
            env, hyperparameters, q_table, episode_rewards)

    return env, q_table


def inference(env, q_table):
    """
    Inference using the updated Q-table
    """
    env.reset()
    done = False

    while not done:
        # Choose the action with the highest Q-value
        action = np.argmax(q_table)
        # Take the action and observe the next state
        _, _, terminated, truncated, _ = env.step(action)
        done = terminated or truncated


if __name__ == '__main__':
    ENV = initialize_environment()
    Q_TABLE = initialize_q_table(ENV)
    HYPERPARAMETERS = initialize_hyperparameters()
    ENV, Q_TABLE = training_loop(HYPERPARAMETERS, ENV, Q_TABLE)
    inference(ENV, Q_TABLE)

    ENV.close()
