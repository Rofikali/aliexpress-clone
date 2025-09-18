import time


def my_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        end_time = time.time()
        args = (start_time, end_time)
        print("Something is happening before the function is called.")
        fun_return = func(*args, **kwargs)
        print(
            f"this function calling --- > {func.__name__} <----, end time {end_time} - start time {start_time} = {end_time - start_time} "
        )
        return fun_return

    return wrapper


@my_decorator
def cal_time(srt_time, end_time):
    print("time is this ")


cal_time()
