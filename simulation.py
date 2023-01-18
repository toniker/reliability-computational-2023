from enum import Enum

import numpy as np


class States(Enum):
    WORKING = 0
    NOT_WORKING = 1
    BROKEN = 2


class System:
    def __init__(self):
        self.mttf = np.empty(0)


class Component:
    def __init__(self, name, mttf, duty_cycle, mttr):
        self.name = name
        self.mttf = mttf
        self.duty_cycle = duty_cycle
        self.mttr = mttr
        self.state = States.WORKING
        self.failure_times = np.empty(0)

    def restore(self):
        self.state = States.WORKING

    def reset(self):
        self.state = States.WORKING
        self.failure_times = np.empty()

    def simulate(self, time):
        if self.state != States.WORKING:
            return

        if time / component_study_time > self.duty_cycle:
            self.failure_times = np.append(self.failure_times, time)
            self.state = States.NOT_WORKING
            return

        lamda = 1 / self.mttf
        failure_chance = lamda * np.exp(-time * lamda)
        random_number = np.random.uniform(0, 1)

        if random_number < failure_chance:
            self.state = States.BROKEN
            self.failure_times = np.append(self.failure_times, time)


def component_simulation():
    for component in components:
        component.reset()

    for run in range(number_of_runs):
        for component in components:
            component.restore()

        for time in range(component_study_time):
            for component in components:
                component.simulate(time)

    for component in components:
        actual_mttf = np.average(component.failure_times)
        print(f'{component.name} experimental MTTF: {actual_mttf:.2f}')
        print(f'{component.name} experimental λ: {1 / actual_mttf:.2f}')


def system_simulation():
    for component in components:
        component.reset()

    system = System()

    steps = {
        '1': [c1],
        '2': [c2, c3, c4],
        '3': [c5, c6],
        '4': [c7]
    }

    for run in range(number_of_runs):
        for component in components:
            component.restore()

        for time in range(system_study_time):
            steps_passing = []

            for step in steps.values():
                for component in step:
                    component.simulate(time)
                    if component.state is States.WORKING:
                        steps_passing += [True]
                    else:
                        steps_passing += [False]

            if False in steps_passing:
                system.mttf = np.append(system.mttf, time)

    print(f"System MTTF {np.average(system.mttf):.3f}")


if __name__ == "__main__":
    component_study_time = 100  # Hours
    system_study_time = 30  # Hours
    number_of_runs = 1000

    c1 = Component(name='C1', mttf=30, duty_cycle=0.3, mttr=12)
    c2 = Component(name='C2', mttf=24, duty_cycle=1,   mttr=12)
    c3 = Component(name='C3', mttf=23, duty_cycle=1,   mttr=12)
    c4 = Component(name='C4', mttf=24, duty_cycle=1,   mttr=10)
    c5 = Component(name='C5', mttf=27, duty_cycle=1,   mttr=10)
    c6 = Component(name='C6', mttf=28, duty_cycle=1,   mttr=8)
    c7 = Component(name='C7', mttf=33, duty_cycle=0.4, mttr=12)

    components = [c1, c2, c3, c4, c5, c6, c7]
    component_simulation()
    system_simulation()
