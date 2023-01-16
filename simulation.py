from enum import Enum


class States(Enum):
    WORKING = 0
    NOT_WORKING = 1
    BROKEN = 2


components = {
    'c1': {"MTTF": 30, "DutyCycle": 0.3, "MTTR": 12, "State": States.WORKING},
    'c2': {"MTTF": 24, "DutyCycle": 1, "MTTR": 12, "State": States.WORKING},
    'c3': {"MTTF": 23, "DutyCycle": 1, "MTTR": 12, "State": States.WORKING},
    'c4': {"MTTF": 24, "DutyCycle": 1, "MTTR": 10, "State": States.WORKING},
    'c5': {"MTTF": 27, "DutyCycle": 1, "MTTR": 10, "State": States.WORKING},
    'c6': {"MTTF": 28, "DutyCycle": 1, "MTTR": 8, "State": States.WORKING},
    'c7': {"MTTF": 33, "DutyCycle": 0.4, "MTTR": 12, "State": States.WORKING},
}

component_study_time = 100  # Hours
system_study_time = 30  # Hours
timestep = 1 # Hours

steps = {
    '1': [components['c1']],
    '2': [components['c2'], components['c3'], components['c4']],
    '3': [components['c5'], components['c6']],
    '4': [components['c7']]
}


def component_simulation():
    for time in range(0, component_study_time, timestep):
        for component in components.values():
            if component['State'] != States.WORKING:
                continue

            if time / component_study_time > component['DutyCycle']:
                component['State'] = States.NOT_WORKING
                print(component)


if __name__ == "__main__":
    component_simulation()
