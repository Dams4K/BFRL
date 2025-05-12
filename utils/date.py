# copied from https://stackoverflow.com/questions/4048651/function-to-convert-seconds-into-minutes-hours-and-days

intervals = (
    ('days', 60*60*24),
    ('hours', 60*60),
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])