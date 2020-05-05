#!/usr/bin/env python3

import os
import numpy as np
import gym
from stable_baselines import PPO1


def main():

    # Load a .zip model file
    model_name = os.path.join(os.getcwd(), "ppo1_cc_0.zip")
    model = PPO1.load(model_name)

    # TODO start the mininet network

    # this model takes as state an input 30x1
    # TODO: this needs to be replaced with real values from the network later on
    state = np.ones((30,), dtype=np.float32)

    # TODO start traffic

    # run inference for some steps
    count = 0
    # while (time.time()-start) < 3:
    while count < 10:

        # The action is an increment to the current sending rate: sending_rate_t+1 = sending_rate_t + action
        action, _ = model.predict(state)
        print("RL model predicted: %s" % action)

        # Update the state to account for effects of action
        # TODO: this needs to be replaced with real values from the network later on
        state = state * 1.1
        count += 1

if __name__ == '__main__':
    main()
