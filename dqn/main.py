import logging
import gymnasium as gym
import ale_py
from matplotlib import pyplot as plt
import torch

from utils.wrappers import *
from agent import DQNAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename="dqn.log",
    encoding="utf-8",
    filemode="a",
)

gym.register_envs(ale_py)
torch.set_num_threads(7)


def play(agent):
    agent.epsilon = 0
    while True:
        obs, _ = env.reset()
        episode_over = False
        episode_reward = 0

        while not episode_over:
            action = agent.get_action(obs)
            obs, reward, terminated, truncated, _ = agent.env.step(action)
            episode_reward += reward
            episode_over = terminated or truncated

        print(f"Episode reward: {episode_reward}")
        input("Press Enter to continue...")


def test(agent, episodes=50):
    agent.epsilon = 0.05

    episode_rewards = []
    # avg_episode_rewards = []

    # plt.ion()
    # fig, ax = plt.subplots()

    for episode in range(1, episodes + 1):
        obs, _ = agent.env.reset()

        done = False
        episode_reward = 0
        while not done:
            action = agent.get_action(obs)
            obs, reward, terminated, truncated, _ = agent.env.step(action)

            done = terminated or truncated
            episode_reward += reward

        print(f"Episode: {episode}/{episodes}, Reward: {episode_reward}")
        episode_rewards.append(episode_reward)
        # avg_episode_rewards.append(np.mean(episode_rewards[-10:]))

        # ax.cla()
        # ax.plot(episode_rewards)
        # ax.plot(avg_episode_rewards)
        # ax.set_xlabel("Episode")
        # ax.set_ylabel("Reward per Episode")
        # fig.canvas.flush_events()

    print(f"Average: {np.mean(episode_rewards)}")


def main():
    pass


if __name__ == "__main__":
    env = gym.make(
        "ALE/Pong-v5", obs_type="grayscale", render_mode="rgb_array", difficulty=0
    )
    # env = gym.make("ALE/MsPacman-v5", obs_type="grayscale", render_mode="rgb_array")

    # env = gym.wrappers.RecordVideo(
    #     env,
    #     video_folder=f"videos/{env.spec.name}",
    #     name_prefix=f"{env.spec.name}",
    #     episode_trigger=lambda x: x % 100 == 0,
    # )
    env = PreprocessFrameWrapper(env)
    env = StackFramesWrapper(env, 4)
    # env = gym.wrappers.AtariPreprocessing(env)

    agent = DQNAgent(env, num_actions=6, memory_size=300000)
    logging.info("Loading model parameters...")
    agent.load("model_params/Pong.params copy.tmp")

    # agent.learn(episodes=10000)
    # play(agent)
    test(agent)
