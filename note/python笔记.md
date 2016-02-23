# Python

## metaclass dynamic generate class

example:
```python
def a_function():
    pass

class MetaClass():
    __metaclass__ = a_function

    pass
```