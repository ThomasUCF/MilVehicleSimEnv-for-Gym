'''
Author: Thomas Schiller, M&S Student
University: University of Central Florida
Institute: Institute for Simulation and Training
'''


import time
import csv
from colorama import Fore, Back
import MilVehicleSimEnv as MilSim

show_obspace = True

env = MilSim.MilVehicleSimEnv()

#env.observation_space.sample()

episodes_scores = []
episodes = 10
for episode in range(episodes):
    state = env.reset()
    done = False
    score = 0

    counter = 0

    while not done:
        #env.render()
        action = env.action_space.sample()

        '''
        if counter < 12:
            action = 3
        else: action = 9
        counter += 1
        '''

        state, reward, done, info = env.step(action)


        # Print the observation space
        if show_obspace:
            with open('observation_space/observation_space.csv', 'w') as f:
                write = csv.writer(f, delimiter=';')
                write.writerows(state)



        score += reward
        time.sleep(0.2)  # slowing down the rendering
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
