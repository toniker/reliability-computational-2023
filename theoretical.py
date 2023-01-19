import math

import pandas as pd

component_study_time = 100  # Hours
system_study_time = 30  # Hours


class Component:
    def __init__(self, name, mttf, duty_cycle, mttr):
        self.name = name
        self.mttf = mttf
        self.duty_cycle = duty_cycle
        self.mttr = mttr


c1 = Component(name='C1', mttf=30, duty_cycle=0.3, mttr=12)
c2 = Component(name='C2', mttf=24, duty_cycle=1, mttr=12)
c3 = Component(name='C3', mttf=23, duty_cycle=1, mttr=12)
c4 = Component(name='C4', mttf=24, duty_cycle=1, mttr=10)
c5 = Component(name='C5', mttf=27, duty_cycle=1, mttr=10)
c6 = Component(name='C6', mttf=28, duty_cycle=1, mttr=8)
c7 = Component(name='C7', mttf=33, duty_cycle=0.4, mttr=12)

components = [c1, c2, c3, c4, c5, c6, c7]


def calculate_components():
    results = []

    for component in components:
        lamda = round(1 / component.mttf, 2)
        r = round(math.exp(-component_study_time / component.mttf), 2)
        results += [[component.name, lamda, r, component.mttf]]

    df = pd.DataFrame(results, columns=['name', 'Reliability', 'λ', 'MTTF'])
    print(df)


def calculate_system():
    steps = {
        '1': [c1],
        '2': [c2, c3, c4],
        '3': [c5, c6],
        '4': [c7]
    }

    system_mttf = 0

    for step in steps.values():
        step_mttf = 0
        if len(step) == 1:
            for component in step:
                step_mttf = component.mttf
        else:
            sum_mttf = 0
            for component in step:
                sum_mttf += 1 / component.mttf
                step_mttf += component.mttf
            step_mttf -= 1 / sum_mttf

        system_mttf += 1 / step_mttf

    system_mttf = round(1 / system_mttf, 2)

    print(f'\nSystem MTTF: {system_mttf}')


calculate_components()
calculate_system()
