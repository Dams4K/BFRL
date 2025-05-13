import time

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


MAX_TIME = 3*24*60*60
MIN_TIME = 60*2 # 2minutes

def calculate_time(t: int) -> int:
    return min(max(MIN_TIME, 1.6**(24-t)), MAX_TIME)

def next_time(t: int) -> int:
    return int(time.time() + calculate_time(t))

if __name__ == "__main__":
    print(calculate_time(next_time(3.8)))
    print(calculate_time(next_time(4.2)))
    print(calculate_time(next_time(6.7)))
    print(calculate_time(next_time(12)))
    print(calculate_time(next_time(24)))