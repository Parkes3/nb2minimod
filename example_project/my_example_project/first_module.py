#| export
def say_hello(name=None):
    if name is None:
        name = 'World'
    return f'Hello {name}'

#| export