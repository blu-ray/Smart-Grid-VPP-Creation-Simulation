import xml.etree.ElementTree as ET
import os
from Agent import Agent
from Grid import Grid

def simulate():
    xml_files = os.listdir('Data\\')
    corrupts = ['WHITBYCGS', 'STONE MILLS SF', 'DPNTMTLND', 'HARMON', 'KIPLING', 'LITTLELONG', 'SILVERFALLS']
    gens_dict = {}
    sim_grid = Grid()
    for file in xml_files:
        addr = os.path.join('Data', file)
        #print(addr)

        tree = ET.parse(addr)
        root = tree.getroot()
        generators = root[1][1]
        for generator in generators:

            name = generator[0].text
            # Generator Name
            #print(generator[0].tag, generator[0].text)

            if name in corrupts:
                continue    #corrupted generator

            if name not in gens_dict:
                agen = Agent(name, generator[1].text)
                gens_dict[name] = agen
                sim_grid.add_vpp(agen)
            # Generator Fuel Type
            #print(generator[1].tag, generator[1].text)
            '''
            if len(generator[2][0]) < 2:
                # N/A generator
                #pass
                continue
            '''
            outputs = generator[2]

            outs = []
            # print("outputs")
            for sample in outputs:
                # Hour
                # print(sample[0].text)

                if len(sample) > 1:
                    # EnergyMW
                    # print(sample[1].text)

                    outs.append(sample[1].text)
                    gens_dict[name].add_out(sample[1].text)

                else:
                    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
                    print(generator[1].text, generator[0].text)


            capabilities = generator[3]
            forec = []
            # print("capabilities")
            for sample in capabilities:
                # Hour
                # print(sample[0].text)

                # EnergyMW
                # print(sample[1].text)

                forec.append(sample[1].text)
                gens_dict[name].add_forec(sample[1].text)

            capacities = generator[4]
            caps = []
            # print("capacities")
            for sample in capacities:
                # Hour
                # print(sample[0].text)

                # EnergyMW
                # print(sample[1].text)

                caps.append(sample[1].text)
                gens_dict[name].add_capac(sample[1].text)

            '''
            for i in range(24):
                if forec[i] != caps[i]:
                    print("!!!FFFFFFF!!!!")
                    break
            '''
        # print(len(root[1][1]))

    # print(len(gens_dict))
    # gen = gens_dict['ADELAIDE']
    # gen2 = gens_dict['AMARANTH']
    # gen3 = gens_dict['ARMOW']
    # print(gen.output(34))
    # print(gen2.output(34))
    # print(gen3.output(34))
    # gen2.merge_holon(gen3)
    # gen.merge_holon(gen2)
    # print(gen.output_sum(34))
    #
    #
    # grid = Grid()
    # grid.add_vpp(gen)
    # grid.pay_for_time(34)
    # print(gen.incomes[0] + gen2.incomes[0] + gen3.incomes[0])
    #
    # gen.remove_child(gen2)
    # gen.remove_child(gen3)
    # grid.add_vpp(gen2)
    # grid.add_vpp(gen3)
    # grid.pay_for_time(34)
    # print(gen.incomes[1] + gen2.incomes[1] + gen3.incomes[1])
    # ss = 0
    # for time in range(744):
    #     for vpp in sim_grid.vpps:
    #         ss += abs(vpp.output(time) - vpp.forecast(time))
    #         if time < 24:
    #             #print(vpp.name, time, vpp.output(time), vpp.forecast(time))
    #             pass
    #     if (time + 1) % 24 == 0:
    #         print(ss)
    #         ss = 0

    return sim_grid.run()