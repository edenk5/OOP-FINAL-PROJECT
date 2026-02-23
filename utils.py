from datetime import datetime

# A decorator is basically a function that "wraps" another function
def audit_logger(func):
    
    # This inner function is the "wrapper" that will run instead of the original function.
    # *args, **kwargs means "accept any parameters the original function needs".
    def wrapper(*args, **kwargs):
        
        # 1. The action we add (printing the log BEFORE the function runs)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🔒 [AUDIT LOG - {current_time}] Action '{func.__name__}' is starting...")
        
        # 2. Running the original function itself (with its parameters)
        result = func(*args, **kwargs)
        
        # 3. Returning the result of the original function
        return result

    # The decorator returns the wrapper function so Python can use it
    return wrapper