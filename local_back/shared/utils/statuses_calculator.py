import os


def main_status(last_value, normal_value, warning_value):
    if last_value < normal_value:
        status = 'normal'
    elif last_value < warning_value:
        status = 'warning'
    else:
        status = 'critical'

    return status


def main_status_reverse(last_value, normal_value, warning_value):
    if last_value > normal_value:
        status = 'normal'
    elif last_value > warning_value:
        status = 'warning'
    else:
        status = 'critical'

    return status


def status_per_core(last_value, normal_value, warning_value):
    num_cores = os.cpu_count()
    if last_value < normal_value * num_cores:
        status = 'normal'
    elif last_value < warning_value * num_cores:
        status = 'warning'
    else:
        status = 'critical'

    return status
