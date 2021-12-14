
def calc_time(time):
    sum_time = int(time[0])*86400 + int(time[1])*3600 + int(time[2])*60 + int(time[3])
    return sum_time


class SWITCH:
    def __init__(self, power) -> None:
        self.name = 'SWITCH'
        self.power = power
        self.start_time = None
        self.end_time= None
        self.energy = 0
    def calculate_energy(self):
        if len(self.start_time) == len(self.end_time):
            for _,time in enumerate(self.start_time):
                start = calc_time(time.split(':'))
                end = calc_time(self.end_time[_].split(':'))
                self.energy += (end - start)*self.power
        else:
            cp_start_time = self.start_time.copy()
            cp_end_time = self.end_time.copy()
            for _,time in enumerate(cp_end_time):
                end = calc_time(time.split(':'))
                start = calc_time(self.start_time[_].split(':'))
                self.energy += (end - start)*self.power
                cp_end_time.remove(time)
                cp_start_time.remove(self.start_time[_])
            start = calc_time(cp_start_time[0].split(':'))
            end = calc_time('31:23:59:59'.split(':'))
            self.energy += (end - start)*self.power
        return self.energy

class SENSOR:
    def __init__(self, power, sensetive) -> None:
        self.name = 'SENSOR'
        self.power = power
        self.end_time = sensetive
        self.start_time = None
        self.energy = 0
    def calculate_energy(self):
        start = []
        for time in self.start_time:
            start.append(calc_time(time.split(':')))
        start = sorted(start)
        for i in range(len(start)):
            if i+1 < len(start):
                if start[i+1] - start[i] <= self.end_time:
                    end = start[i+1] + self.end_time
                else:
                    end = start[i]+self.end_time
                # self.energy += (end - start[i])*self.power
            else:
                end = start[i]+self.end_time
            self.energy += (end - start[i])*self.power
        return self.energy


with open('input.txt') as f:
    lines = f.readlines()
lines = [line.replace('\n','') for line in lines]
num_lamp = int(lines[0])

detect_lamp = lines[1:num_lamp+1]
lamps = {}
for _,lamp in enumerate(detect_lamp):
    type_lamp = lamp.split(' ')
    if len(type_lamp)>2:
        lamps[_+1]=SENSOR(int(type_lamp[1]), int(type_lamp[2]))
    else:
        lamps[_+1]=SWITCH(int(type_lamp[1]))
num_algo = int(lines[num_lamp+1])

detect_algo = lines[num_lamp+2:num_lamp+num_algo+1]
algos = {int(algo.split(' ')[0]): int(algo.split(' ')[1]) for algo in detect_algo}

detect_Consumption = lines[num_lamp+3+num_algo:]
count_cons = {}
for consumption in detect_Consumption:
    consumption = consumption.split(' ')
    class_num = int(consumption[0])
    if class_num not in count_cons:
        count_cons[class_num] ={}
        count_cons[class_num]['start_time'] = [':'.join(consumption[1:])]
        count_cons[class_num]['end_time'] =[]
    else:
        if len(count_cons[class_num]['start_time']) > len(count_cons[class_num]['end_time']):
            count_cons[class_num]['end_time'].append(':'.join(consumption[1:]))
        else:
            count_cons[class_num]['start_time'].append(':'.join(consumption[1:]))

sum_energy = 0
for val in count_cons:
    lamp_class = lamps[val]
    if lamp_class.name == 'SWITCH':
        lamp_class.start_time = count_cons[val]['start_time']
        lamp_class.end_time = count_cons[val]['end_time']
        sum_energy += lamp_class.calculate_energy()
    elif lamp_class.name == 'SENSOR':
        lamp_class.start_time = [*count_cons[val]['start_time'],*count_cons[val]['end_time']]
        sum_energy += lamp_class.calculate_energy()
min_E = None
print(sum_energy,algos)
for energy in algos:
    if sum_energy <= energy:
        print(sum_energy*algos[energy])
        break
        
