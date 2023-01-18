from enum import Enum
import random

import numpy as np
from scipy.stats import expon

class States(Enum):
    WORKING = 0
    NOT_WORKING = 1
    BROKEN = 2


class Component:
    def __init__(self, name, mttf, duty_cycle, mttr):
        self.name = name
        self.mttf = mttf
        self.duty_cycle = duty_cycle
        self.mttr = mttr
        self.state = States.WORKING
        self.failure_times = np.empty(0)
        self.expon = expon(scale=mttf)

    def simulate(self, time):
        if self.state != States.WORKING:
            return

        if time / component_study_time > self.duty_cycle:
            self.state = States.NOT_WORKING
            return

        failure_chance = 1 - np.exp(-time / self.mttf)

        random_number = np.random.uniform(0, 1)
        if random_number < failure_chance:
            self.state = States.BROKEN
            self.failure_times = np.append(self.failure_times, time)


def reset_components():
    for component in components:
        component.state = States.WORKING


def component_simulation():
    for run in range(number_of_runs):
        reset_components()

        for time in range(component_study_time):
            c1.simulate(time)
            # for component in components:
            #     component.simulate(time)

    for component in components:
        actual_mttf = np.average(component.failure_times)
        print(f'{component.name} experimental MTTF: {actual_mttf:.2f}')
        print(f'{component.name} experimental λ: {1 / actual_mttf:.2f}')


if __name__ == "__main__":
    component_study_time = 100  # Hours
    system_study_time = 30  # Hours
    timestep = 1  # Hours
    number_of_runs = 1000

    c1 = Component(name='c1', mttf=30, duty_cycle=0.3, mttr=12)
    c2 = Component(name='c2', mttf=24, duty_cycle=1, mttr=12)
    c3 = Component(name='c3', mttf=23, duty_cycle=1, mttr=12)
    c4 = Component(name='c4', mttf=24, duty_cycle=1, mttr=10)
    c5 = Component(name='c5', mttf=27, duty_cycle=1, mttr=10)
    c6 = Component(name='c6', mttf=28, duty_cycle=1, mttr=8)
    c7 = Component(name='c7', mttf=33, duty_cycle=0.4, mttr=12)

    components = [c1, c2, c3, c4, c5, c6, c7]

    steps = {
        '1': [c1],
        '2': [c2, c3, c4],
        '3': [c5, c6],
        '4': [c7]
    }

    component_simulation()

