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
    c1 = Component('c1', 30, 0.3, 12)
    c2 = Component('c2', 24, 1, 12)
    c3 = Component('c3', 23, 1, 12)
    c4 = Component('c4', 24, 1, 10)
    c5 = Component('c5', 27, 1, 10)
    c6 = Component('c6', 28, 1, 8)
    c7 = Component('c7', 33, 0.4, 12)

    components = [c1, c2, c3, c4, c5, c6, c7]

    steps = {
        '1': [c1],
        '2': [c2, c3, c4],
        '3': [c5, c6],
        '4': [c7]
    }

    component_simulation()
