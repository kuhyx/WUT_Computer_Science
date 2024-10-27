from metadrive.envs.metadrive_env import MetaDriveEnv
import gymnasium as gym

env = MetaDriveEnv(config={"use_render": True})
obs, info = env.reset()
for i in range(1000):
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    if terminated or truncated:
        env.reset()
env.close()