import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class System:
    def __init__(self):
        self.ttf = []
        self.ttr = []
        self.mttr = []
        self.mttf = []
        self.last_failure = np.inf
        self.last_repair = 0
        self.state = "Working"


class Component:
    def __init__(self, name, mttf, duty_cycle, mttr):
        self.name = name
        self.mttf = mttf
        self.duty_cycle = duty_cycle
        self.mttr = mttr
        self.state = "Working"
        self.ttf = []
        self.ttr = []
        self.last_failure_time = np.inf
        self.last_repair_time = 0

    def get_results(self, study_time, repair):
        total_study_time = number_of_runs * study_time * self.duty_cycle

        mttf = round(np.average(self.ttf), 2)
        reliability = round(math.exp(-component_study_time / mttf), 2)
        lamda = round(1 / mttf, 2)
        if repair:
            mttr = round(np.average(self.ttr), 2)
            mtbr = round(total_study_time / len(self.ttr), 2)
        else:
            mtbr = 0
            mttr = 0
        mtbf = round(total_study_time / len(self.ttf), 2)
        mut = round(np.sum(self.ttf) / total_study_time, 2)
        mdt = 1 - mut
        availability = mut / (mut + mdt)

        return self.name, reliability, lamda, mttf, mttr, mtbf, mtbr, mut, mdt, availability

    def get_state(self, point_in_time):
        if self.state == "Not Working":
            return self.state
        state = "Working"
        time = 0
        for i in range(len(self.ttr)):
            time += self.ttf[i]
            state = "Broken"
            if time > point_in_time:
                break
            time += self.ttr[i]
            state = "Working"
            if time > point_in_time:
                break
        return state

    def simulate_failure(self, study_time):
        if self.state != "Working":
            return

        time_until_failure = np.random.exponential(self.mttf)

        if time_until_failure + self.last_repair_time >= self.duty_cycle * study_time:
            # The component will end its duty cycle before breaking
            self.state = "Not Working"
            self.ttf = np.append(self.ttf, self.duty_cycle * study_time - self.last_repair_time)
            return

        # The component broke before reaching the end of its duty cycle
        self.state = "Broken"
        self.last_failure_time = self.last_repair_time + time_until_failure
        self.ttf = np.append(self.ttf, time_until_failure)

    def simulate_repair(self, study_time):
        time_until_repair = np.random.exponential(self.mttr)

        if self.last_failure_time + time_until_repair > study_time:
            # There is no time to fix the component
            return

        self.state = "Working"
        self.last_repair_time = self.last_failure_time + time_until_repair
        self.ttr = np.append(self.ttr, time_until_repair)


def simulate_components(repair):
    for component in components:
        component.ttf = np.empty(0)
        component.ttr = np.empty(0)

    for run in range(number_of_runs):
        for component in components:
            component.state = "Working"
            component.last_repair_time = 0
            component.last_failure_time = np.inf
            for time in range(component_study_time):
                component.simulate_failure(component_study_time)
                if repair is True and component.state == "Broken":
                    component.simulate_repair(component_study_time)

    # Collect all the data in a single dataframe
    results = []

    for component in components:
        results += [component.get_results(component_study_time, repair)]

    df = pd.DataFrame(results, columns=['Name', 'Reliability', 'λ', 'MTTF', 'MTTR', 'MTBF', 'MTBR', 'MUT', 'MDT',
                                        'Availability'])
    print(f'\n --------- Repair = {repair} ---------')
    print(df)

    # plt.figure()
    # plt.title('MTTF Histogram')
    # plt.hist(df['MTTF'], orientation='horizontal')
    # plt.xlabel('Number of components')
    # plt.ylabel("Components")
    # plt.grid()
    # plt.figure()
    # plt.show()


def simulate_system(repair):
    steps = {
        '1': [c1],
        '2': [c2, c3, c4],
        '3': [c5, c6],
        '4': [c7]
    }

    system = System()

    for component in components:
        # Reset the component arrays from previous simulations
        component.ttf = np.empty(0)
        component.ttr = np.empty(0)

    for run in range(number_of_runs):
        for component in components:
            # Reset the components to a working state at the start of every run
            component.state = "Working"
            component.last_repair_time = 0
            component.last_failure_time = np.inf

            # Simulate the components failing and repairing over the course of the study
            for time in range(system_study_time):
                component.simulate_failure(system_study_time)
                if repair is True and component.state == "Broken":
                    component.simulate_repair(system_study_time)

        # Having all the values for the component failure and repair states, get the status of the system
        # step of the way
        for time in range(system_study_time):
            steps_passing = []
            for step in steps.values():
                step_passes = False

                for component in step:
                    if component.get_state(time) == "Working":
                        step_passes = True

                steps_passing += [step_passes]
            if system.state == "Working":
                # If any step of the system fails, then the whole system fails
                if False in steps_passing:
                    system.last_failure = time
                    system.state = "Not Working"
                    system.ttf.append(time - system.last_repair)
            else:
                # The system was already in a non-working state, but it is now
                if False not in steps_passing:
                    system.last_repair = time
                    system.state = "Working"
                    system.ttf.append(time - system.last_failure)

    # system.mttf = np.average(system.ttf)
    # system.mttr = np.average(system.ttr)
    # results = [system.mttf, system.mttr]
    #
    # df = pd.DataFrame(results, columns=['MTTF', 'MTTR'])
    # print(df)


if __name__ == "__main__":
    component_study_time = 100  # Hours
    system_study_time = 30  # Hours
    number_of_runs = 100

    c1 = Component(name='C1', mttf=30, duty_cycle=0.3, mttr=12)
    c2 = Component(name='C2', mttf=24, duty_cycle=1, mttr=12)
    c3 = Component(name='C3', mttf=23, duty_cycle=1, mttr=12)
    c4 = Component(name='C4', mttf=24, duty_cycle=1, mttr=10)
    c5 = Component(name='C5', mttf=27, duty_cycle=1, mttr=10)
    c6 = Component(name='C6', mttf=28, duty_cycle=1, mttr=8)
    c7 = Component(name='C7', mttf=33, duty_cycle=0.4, mttr=12)

    components = [c1, c2, c3, c4, c5, c6, c7]

    simulate_components(repair=False)
    simulate_components(repair=True)
    simulate_system(repair=False)
    simulate_system(repair=True)
