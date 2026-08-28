#!/usr/bin/env python3
"""Code used to solve MountainCar-v0 gymnasium problem using Q-Learning algorithm."""

import logging
from datetime import UTC, datetime

import gymnasium as gym
import numpy as np

# Only record video once the agent has had time to learn something.
VIDEO_FROM_EPISODE = 600
# NumPy's legacy np.random.* functions share one global state; Generator is
# the modern API and is what NPY002 asks for.
RNG = np.random.default_rng()
logger = logging.getLogger(__name__)

# Helper function to discretize the state


def discretize_state(state: object, env: object, *, first_time: bool = False) -> object:
    # f"state: {state}, state[0]: {state[0]}, env.observation_space.low:
    # {env.observation_space.low}")
    """Bucket a continuous observation into the Q-table's grid."""
    if first_time:
        substract_from_state = state[0] - env.observation_space.low
    else:
        substract_from_state = state - env.observation_space.low
    discretized_state = (substract_from_state) * np.array([10, 100])
    return np.round(discretized_state, 0).astype(int)


def initialize_environment() -> object:
    """Initialize environment and video recording."""
    # Initialize environment
    env = gym.make("MountainCar-v0", render_mode="rgb_array")
    # Save video
    now = datetime.now(tz=UTC)
    time_string = now.strftime("%H:%M:%S")
    return gym.wrappers.RecordVideo(
        env,
        video_folder="vid",
        disable_logger=True,
        name_prefix=time_string,
        episode_trigger=lambda x: x > VIDEO_FROM_EPISODE and x % 2 == 0,
    )


def initialize_q_table(env: object) -> object:
    """Initialize "empty" Q-table."""
    # Initialize Q-table
    # 0 accelerate left
    # 1 dont accelerate
    # 2 accelerate to the right
    num_states = (env.observation_space.high - env.observation_space.low) * np.array(
        [10, 100]
    )
    num_states = np.round(num_states, 0).astype(int) + 1
    return np.zeros((num_states[0], num_states[1], env.action_space.n))


def initialize_hyperparameters() -> dict[str, object]:
    """Initialize hyperparameters used by algorithm."""
    return {
        "learning_rate": 0.1,
        "discount_factor": 0.99,
        "epsilon": 0.2,
        "max_episodes": 1000,
        "max_steps": 500,
        "min_max_car_position": [-1.2, 0.6],
        "min_max_car_velocity": [-0.07, 0.07],
        "goal_x": 0.5,
        "truncation": 200,
    }


def choose_action(
    hyperparameters: dict[str, object],
    env: object,
    q_table: object,
    discretized_state: object,
) -> int:
    """Choose one of 3 actions possible for the algorithm."""
    # hyperparameters["epsilon"]-greedy exploration-exploitation tradeoff
    if RNG.uniform(0, 1) < hyperparameters["epsilon"]:
        action = env.action_space.sample()  # Choose a random action
    else:
        # Choose the action with the highest Q-value
        action = np.argmax(q_table[discretized_state[0], discretized_state[1]])
    return action


def update_q_table(
    q_table: object, action: int, hyperparameters: dict[str, object], reward: float
) -> object:
    """Update q_table with newest reward."""
    # Q-table update
    q_value = q_table[action]
    max_q_value = np.max(q_table)
    new_q_value = (1 - hyperparameters["learning_rate"]) * q_value + hyperparameters[
        "learning_rate"
    ] * (reward + hyperparameters["discount_factor"] * max_q_value)
    q_table[action] = new_q_value
    return q_table


def movement(
    hyperparameters: dict[str, object],
    env: object,
    q_table: object,
    discretized_state: object,
    progress: tuple[float, int] = (0.0, 0),
) -> tuple[dict[str, object], object, object, float]:
    """Choose action and observe consequences.

    ``progress`` is (total_reward, episode_number); they travel together
    through the whole training loop, so they are passed together.
    """
    total_reward, episode_number = progress
    action = choose_action(hyperparameters, env, q_table, discretized_state)
    # Take the action and observe the next state
    next_state, reward, terminated, truncated, _ = env.step(action)
    discretized_next_state = discretize_state(next_state, env, first_time=False)
    q_table[discretized_state[0], discretized_state[1], action] += hyperparameters[
        "learning_rate"
    ] * (
        reward
        + hyperparameters["discount_factor"]
        * np.max(q_table[discretized_next_state[0], discretized_next_state[1]])
        - q_table[discretized_state[0], discretized_state[1], action]
    )

    total_reward += reward
    discretized_state = discretized_next_state
    done = terminated or truncated
    if terminated:
        logger.info("Destination reached on episode:  %s", episode_number)
    return hyperparameters, env, q_table, done, discretized_state, total_reward


def episode_step(
    env: object,
    hyperparameters: dict[str, object],
    q_table: object,
    episode_rewards: list[float],
    episode_number: int,
) -> tuple[object, dict[str, object], object, list[float]]:
    """Actions done with every episode."""
    state = env.reset()  # Reset the environment to an initial state
    discretized_state = discretize_state(state, env, first_time=True)
    done = False  # Boolean to indicate episode completion
    total_reward = 0  # Accumulate rewards for the episode

    for _step in range(hyperparameters["max_steps"]):
        hyperparameters, env, q_table, done, discretized_state, total_reward = movement(
            hyperparameters,
            env,
            q_table,
            discretized_state,
            (total_reward, episode_number),
        )
        if done:
            break

    episode_rewards.append(total_reward)
    return env, hyperparameters, q_table, episode_rewards


def training_loop(
    hyperparameters: dict[str, object], env: object, q_table: object
) -> tuple[object, object]:
    """Actual training for MountainCar."""
    episode_rewards = []  # List to store episode rewards

    for episode_number in range(hyperparameters["max_episodes"]):
        env, hyperparameters, q_table, episode_rewards = episode_step(
            env, hyperparameters, q_table, episode_rewards, episode_number
        )

    return env, q_table


def inference(env: object, q_table: object) -> None:
    """Inference using the updated Q-table."""
    env.reset()
    done = False

    while not done:
        # Choose the action with the highest Q-value
        action = np.argmax(q_table)
        # Take the action and observe the next state
        _, _, terminated, truncated, _ = env.step(action)
        done = terminated or truncated


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    HYPERPARAMETERS = initialize_hyperparameters()
    ENV = initialize_environment(HYPERPARAMETERS)
    Q_TABLE = initialize_q_table(ENV)
    ENV, Q_TABLE = training_loop(HYPERPARAMETERS, ENV, Q_TABLE)
    inference(ENV, Q_TABLE)

    ENV.close()
