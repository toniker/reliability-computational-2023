import math
import random
from enum import Enum


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

    def simulate(self, time) -> float:
        if self.state != States.WORKING:
            return

        if time / component_study_time > self.duty_cycle:
            print('Component ended duty cycle')
            self.state = States.NOT_WORKING
            return

        lamda = 1 / self.mttf
        chance_of_failing = poisson_pdf(lamda, time)

        if random.random() > chance_of_failing:
            print('Component Failed')
            self.state = States.BROKEN


component_study_time = 100  # Hours
system_study_time = 30  # Hours
timestep = 1  # Hours


def poisson_pdf(lamda, k) -> float:
    return (lamda ** k) * (math.e ** (-1 * lamda)) / math.factorial(k)


def component_simulation():
    for time in range(0, component_study_time, timestep):
        for component in components:
            component.simulate(time)


if __name__ == "__main__":
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
