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
        self.failure_times = []

    def simulate(self, time):
        if self.state != States.WORKING:
            return

        if time / component_study_time > self.duty_cycle:
            self.state = States.NOT_WORKING
            return

        lamda = 1 / self.mttf
        chance_of_failing = 1 - poisson_pdf(lamda, 1)

        if random.random() > chance_of_failing:
            self.failure_times.append(time)
            self.state = States.BROKEN

    def repair(self):
        if self.state != States.BROKEN:
            return

        lamda = 1 / self.mttr
        chance_of_repairing = 1 - poisson_pdf(lamda, 1)

        if random.random() > chance_of_repairing:
            self.state = States.WORKING

    def reset(self):
        self.state = States.WORKING


def poisson_pdf(lamda, k) -> float:
    return (lamda ** k) * (math.e ** (-1 * lamda)) / math.factorial(k)


def component_simulation():
    for component in components:
        component.reset()

    for time in range(0, component_study_time, timestep):
        for component in components:
            component.simulate(time)


if __name__ == "__main__":
    c1 = Component(name='c1', mttf=30, duty_cycle=0.3, mttr=12)
    c2 = Component(name='c2', mttf=24, duty_cycle=1,   mttr=12)
    c3 = Component(name='c3', mttf=23, duty_cycle=1,   mttr=12)
    c4 = Component(name='c4', mttf=24, duty_cycle=1,   mttr=10)
    c5 = Component(name='c5', mttf=27, duty_cycle=1,   mttr=10)
    c6 = Component(name='c6', mttf=28, duty_cycle=1,   mttr=8)
    c7 = Component(name='c7', mttf=33, duty_cycle=0.4, mttr=12)

    components = [c1, c2, c3, c4, c5, c6, c7]

    steps = {
        '1': [c1],
        '2': [c2, c3, c4],
        '3': [c5, c6],
        '4': [c7]
    }

    for run in range(number_of_runs):
        component_simulation()

    for component in components:
        if len(component.failure_times) == 0:
            continue

        time_sum = 0
        for failure_time in component.failure_times:
            time_sum += failure_time

        print(f'{component.name} failure Time: {time_sum / len(component.failure_times):.2f}')
