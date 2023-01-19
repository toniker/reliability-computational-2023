import numpy as np


class Component:
    def __init__(self, name, mttf, duty_cycle, mttr):
        self.name = name
        self.mttf = mttf
        self.duty_cycle = duty_cycle
        self.mttr = mttr
        self.state = "Working"
        self.ttf = np.zeros(1)
        self.ttr = np.zeros(1)

    def print_results(self):
        mttf = np.average(self.ttf)
        mttr = np.average(self.ttr)
        print(f'{self.name} MTTF: {mttf:.2f}')
        # print(f'{self.name} λ: {1 / mttf:.3f}')
        print(f'{self.name} MTTR: {mttr:.1f}')

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

        last_repair_time = self.ttr[-1]
        time_until_failure = np.random.exponential(self.mttf)

        if time_until_failure + last_repair_time >= self.duty_cycle * study_time:
            # The component will end its duty cycle before breaking
            self.state = "Not Working"
            self.ttf = np.append(self.ttf, self.duty_cycle * study_time)
            return

        # The component broke before reaching the end of its duty cycle
        self.state = "Broken"
        self.ttf = np.append(self.ttf, time_until_failure)

    def simulate_repair(self, study_time):
        last_failure_time = self.ttf[-1]
        time_until_repair = np.random.exponential(self.mttr)

        if last_failure_time + time_until_repair > study_time:
            # There is no time to fix the component
            return

        self.state = "Working"
        self.ttr = np.append(self.ttr, time_until_repair)


def simulate_components(repair):
    for component in components:
        component.state = "Working"
        component.ttf = np.empty(0)
        component.ttr = np.empty(0)

    for run in range(number_of_runs):
        for component in components:
            component.state = "Working"
            for time in range(component_study_time):
                component.simulate_failure(component_study_time)
                if repair is True and component.state == "Broken":
                    component.simulate_repair(component_study_time)

    for component in components:
        component.print_results()


def simulate_system(repair):
    steps = {
        '1': [c1],
        '2': [c2, c3, c4],
        '3': [c5, c6],
        '4': [c7]
    }

    system_ttf = np.empty(0)

    for component in components:
        # Reset the component arrays from previous simulations
        component.ttf = np.empty(0)
        component.ttr = np.empty(0)

    for run in range(number_of_runs):
        for component in components:
            # Reset the components to a working state at the start of every run
            component.state = "Working"

            # Simulate the components failing and repairing over the course of the study
            for time in range(system_study_time):
                component.simulate_failure(system_study_time)
                if repair is True and component.state == "Broken":
                    component.simulate_repair(system_study_time)

        # Having all the values for the component failure and repair states, get the status of the system
        # step of the way
        steps_passing = []
        for time in range(system_study_time):
            for step in steps.values():
                step_passes = False

                for component in step:
                    if component.get_state(time) == "Working":
                        step_passes = True

                steps_passing += [step_passes]

            # If any step of the system fails, then the whole system fails
            if False in steps_passing:
                system_ttf += time


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

    simulate_components(repair=True)
