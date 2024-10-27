import metadrive

# Initialize the MetaDrive environment
env = metadrive.MetaDriveEnv()

# Reset the environment to start a new episode
env.reset()

# Run the environment for a few steps
for _ in range(10):
    env.step(env.action_space.sample())  # Take random actions

print("Hello, MetaDrive World!")  # Print a greeting

# Close the environment after use
env.close()
