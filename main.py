'''
Author: Thomas Schiller
University: University of Central Florida
Institute: Institute for Simulation and Training
'''


import time
import csv
from colorama import Fore, Back
import MilVehicleSimEnv as MilSim

env = MilSim.MilVehicleSimEnv()

#env.observation_space.sample()

episodes_scores = []
episodes = 10
for episode in range(episodes):
    state = env.reset()
    done = False
    score = 0

    while not done:
        #env.render()
        action = env.action_space.sample()
        #action = 6
        state, reward, done, info = env.step(action)


        # This is for Testing the Observation Space

        with open('observation_space.csv', 'w') as f:
            write = csv.writer(f)
            write.writerows(state)



        score += reward
        time.sleep(0.08)
        env.render()

        # print the statistics ...
        print_stats = True
        if print_stats:
            print(f"Episode: {episode + 1}")
            print(f"Done: {done}")
            print(f"Reward: {reward}")
            print(f"Score: {score}")
            for i in range(len(episodes_scores)):
                if episodes_scores[i] < -60:
                    print(Back.RED + Fore.BLACK + f'Episode {i + 1}: {episodes_scores[i]}' + Back.BLACK + Fore.WHITE)
                else:
                    print(Back.GREEN + Fore.BLACK + f'Episode {i + 1}: {episodes_scores[i]}' + Back.BLACK + Fore.WHITE)

    episodes_scores.append(score)
    #print('Episode:{} Score:{}'.format(episode, score))
