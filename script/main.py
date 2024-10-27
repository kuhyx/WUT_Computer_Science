import ray
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
from metadrive import MultiAgentTIntersectionEnv
import random

# Initialize Ray
ray.init(ignore_reinit_error=True)

# Define a custom environment class that switches between three maps
class MultiMapEnv(MultiAgentTIntersectionEnv):
    def __init__(self, config):
        # Define available maps
        self.maps = ["TIntersection", "Roundabout", "Straight"]
        super().__init__(config)

    def reset(self):
        # Randomly choose a map from the available ones at the start of each episode
        self.config["map"] = random.choice(self.maps)
        return super().reset()

# Multi-agent configuration with two independent policies
config = {
    "env": MultiMapEnv,
    "env_config": {
        "num_agents": 2,           # Set to 2 agents for this multi-agent scenario
    },
    "framework": "torch",          # Use PyTorch as the backend
    "num_workers": 1,              # Set to 1 worker for simplicity
    "multiagent": {
        "policies": {
            "policy_1": {},  # Configuration for the first agent's policy
            "policy_2": {},  # Configuration for the second agent's policy
        },
        "policy_mapping_fn": lambda agent_id: "policy_1" if agent_id == "agent_1" else "policy_2",
    },
}

# Initialize the trainer with PPO algorithm
trainer = PPOTrainer(env=MultiMapEnv, config=config)

# Training loop
print("Starting training for two agents across multiple maps...")
for i in range(10):  # Number of training iterations
    result = trainer.train()
    print(f"Iteration {i + 1}: reward = {result['episode_reward_mean']}")

# Clean up resources
trainer.cleanup()
ray.shutdown()
