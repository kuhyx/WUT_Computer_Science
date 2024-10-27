from metadrive.envs.metadrive_env import MetaDriveEnv
import gymnasium as gym
from metadrive.envs.gym_wrapper import createGymWrapper # import the wrapper

env = createGymWrapper(MetaDriveEnv)(config={"use_render": True}) # wrap the environment
obs = env.reset()
for i in range(1000):
    obs, reward, done, info = env.step(env.action_space.sample()) # the return value contains no truncate
    if done:
        env.reset()
env.close()