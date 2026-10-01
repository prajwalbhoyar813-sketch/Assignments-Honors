def output_decorator(operation):
    def deco(func):
        def value(a, b):
            result = func(a, b)
            print("--------------------")
            print(f" {operation}")
            print(f" input: {a}, {b}")
            print(f" output: {result}")
            print("--------------------")

            return result
        return value
    return deco
@output_decorator("Adding")
def add(a, b):
    return a + b
add(9,9)