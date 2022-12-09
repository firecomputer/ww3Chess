import gym
from game import *

class CustomEnv(gym.Env):
    def __init__(self,env_config={}):
        #self.observation_space = gym.spaces.box
        #self.action_space = <gym.space>
        self.game = Game()
        self.action_space = gym.spaces.Tuple((gym.spaces.discrete(WIDTH),gym.spaces.discrete(HEIGHT)))

    def reset(self):
        # reset the environment to initial state
        game.reset()
        self.state = (game.board.armies)
        return self.state

    def step(self, action):
        # perform one step in the game logic
        return observation, reward, done, info