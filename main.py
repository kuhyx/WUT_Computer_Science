import gymnasium as gym

if __name__ == "__main__":
    # init env
    env = gym.make("MountainCar-v0", render_mode="rgb_array")

    # wrapper to record the video at 3rd episode and saves it to the folder
    # 'vid'
    env = gym.wrappers.RecordVideo(
        env, video_folder="vid", episode_trigger=lambda x: x == 3
    )

    # an episode ends if goal is reached or other game ending factors (e.g.
    # reached max steps)
    n_episodes = 4
    for episode in range(n_episodes):  # iterate episodes
        state, info = env.reset()  # reset the env to an initial state
        done = False  # boolean to stop an episode
        
        while not done:  # iterate steps
            # randomly choose a sample
            action = env.action_space.sample()
            # take the action (step) and observe the state and reward
            next_state, reward, terminated, truncated, info = env.step(action)
            # condition to stop an episode
            done = terminated or truncated

    env.close()
