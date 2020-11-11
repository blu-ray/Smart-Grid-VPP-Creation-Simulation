import AgentCreator
from matplotlib import pyplot as plt
import numpy as np

def save_simulation(filename, explanations):
    history = AgentCreator.simulate()
    with open(f'Simulations\\{filename}', 'w') as sim_file:
        sim_file.write(explanations)
        sim_file.write('\n')
        for key in history.keys():
            sim_file.write(key)
            sim_file.write('\t')
            for item in history[key]:
                sim_file.write(str(item))
                sim_file.write(' ')
            sim_file.write('\n')

def load_simulation(filename):
    with open(f'Simulations\\{filename}', 'r') as sim_file:
        history = {}
        sim_file.readline() # explanations
        line = sim_file.readline()
        while(line):
            line_list = line.split()
            key = line_list[0]
            history[key] = []
            for i in range(1, len(line_list)):
                history[key].append(float(line_list[i]))
            line = sim_file.readline()
    return history

def show_report(history, history2, history3, history4):
    print(len(history['spday']))
    print(history3['nov'][-10:])

    # this part is for simple hourly figure
    # fig, ax = plt.subplots(figsize = (8, 4))
    # line1 = ax.plot(history['sp'])
    # plt.setp(line1, label = 'income')
    # ax.set_title('Income Amount')
    # plt.ylabel('Average Income per Agent')
    # plt.xlabel('Hour')
    # # ax.plot(history['sp'])
    # plt.ylim(500000, 1000000)
    # ax.legend()
    # plt.show()

    #this part is four daily vpp - fixed price - singletons
    # fig, ax = plt.subplots(figsize = (8, 4))
    # line1 = ax.plot(history['spday'])
    # line2 = ax.plot(history2['spday'])
    # line3 = ax.plot(history3['spday'])
    # plt.setp(line1, label='singletons')
    # plt.setp(line2, label='with VPP', color='orange')
    # plt.setp(line3, label='fixed price', color='green')
    # ax.set_title('Income Amount')
    # plt.ylabel('Average Income per Agent')
    # plt.xlabel('Day')
    # # ax.plot(history['sp'])
    # #plt.ylim(500000, 900000)
    # ax.legend()
    # plt.show()

    #this part is for average number of agents in vpps
    # fig, ax = plt.subplots(figsize = (8, 4))
    # line1 = ax.plot(history['nov'])
    # line2 = ax.plot(history2['nov'])
    # line3 = ax.plot(history3['nov'])
    # plt.setp(line1, label='100%')
    # plt.setp(line2, label='75%', color='orange')
    # plt.setp(line3, label='50%', color='green')
    # ax.set_title('Holons Size Average')
    # plt.ylabel('Average Number of Agents in each VPP')
    # plt.xlabel('Hour')
    # # ax.plot(history['sp'])
    # #plt.ylim(500000, 900000)
    # ax.legend()
    # plt.show()


    fig, ax = plt.subplots(figsize = (8, 4))
    line1 = ax.plot(history['errorday'])
    line2 = ax.plot(history2['errorday'])
    line3 = ax.plot(history3['errorday'])
    line4 = ax.plot(history4['errorday'])
    plt.setp(line1, label='VPP CRPS')
    plt.setp(line2, label='VPP MSE', color='orange')
    plt.setp(line3, label='VPP none', color='green')
    plt.setp(line4, label='singletons none', color='red')

    ax.set_title('Error Rate')
    plt.ylabel('Error')
    plt.xlabel('Day')
    # ax.plot(history['sp'])
    #plt.ylim(500000, 900000)
    ax.legend()
    plt.show()

    # fig, ax = plt.subplots(figsize = (8, 4))
    # line1 = ax.plot((np.array(history['spday']) + np.array(history2['spday']))/2)
    # line2 = ax.plot(history3['spday'])
    # plt.setp(line2, color = 'darkorange')
    # plt.show()
    # plt.plot(self.history['nov'])
    # plt.show()


    # fig, ax = plt.subplots(figsize = (8, 4))
    # line1 = ax.plot((np.array(history['errorday']) + np.array(history2['errorday']))/2)
    # line2 = ax.plot(history3['errorday'])
    # plt.setp(line2, color = 'darkorange')
    # plt.show()

#save_simulation('1.txt', 'crps')
#save_simulation('2.txt', 'crps')
#save_simulation('3_novpp.txt', 'crps')

# history = load_simulation('1.txt')
# history2 = load_simulation('2.txt')
# history3 = load_simulation('3_novpp.txt')

#save_simulation('final_1_1.txt', 'sigleton with crps')
#save_simulation('final_1_2.txt', 'vpp with crps')
#save_simulation('final_1_3.txt', 'fixed price crps')

# history = load_simulation('final_1_1.txt')
# history2 = load_simulation('final_1_2.txt')
# history3 = load_simulation('final_1_3.txt')

#save_simulation('final_2_1.txt', 'vpp 100')
#save_simulation('final_2_2.txt', 'vpp 75')
#save_simulation('final_2_3.txt', 'vpp 50')

# history = load_simulation('final_2_1.txt')
# history2 = load_simulation('final_2_2.txt')
# history3 = load_simulation('final_2_3.txt')

#save_simulation('final_3_1.txt', 'vpp crps')
#save_simulation('final_3_2.txt', 'vpp mse')
#save_simulation('final_3_3.txt', 'vpp none')
#save_simulation('final_3_4.txt', 'singletons none')

history = load_simulation('final_3_1.txt')
history2 = load_simulation('final_3_2.txt')
history3 = load_simulation('final_3_3.txt')
history4= load_simulation('final_3_4.txt')

show_report(history, history2, history3, history4)