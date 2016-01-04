# python-parametrized-tests

[![Build Status](https://travis-ci.org/samupl/python-parametrized-tests.svg?branch=master)](https://travis-ci.org/samupl/python-parametrized-tests)

A very simple module that allows for parametrized test cases in python.

PyPI: https://pypi.python.org/pypi/parametrized/0.1

## Usage

In order to use the parametrized module, you have to do two simple things:

* Decorate the class with _@parametrized_test_case_ decorator,
* Decorate each parametrized method with _@parametrized_ decorator, providing arguments for that template method.

In the following example, the _param()_ method of the _ExampleParametrizedTestCase_ will be converted to three test methods, each calling the original _param_ with _value1_ and _value2_ params set to 1, 2 or 3.

This is particularly useful when you have to test a single method/function/class with different input values. Normally you either have to write separate test methods for each input value, or sacrifice test runner capabilities to distinguish between separate tests and use a for loop. With _parametrized_, you can just mark a method as parametrized and feed it with input values.

```python
import unittest
from parametrized import parametrized_test_case, parametrized


@parametrized_test_case
class ExampleParametrizedTestCase(unittest.TestCase):
  @parametrized(args=(
          (1, 1),
          (2, 2),
          (3, 3)
      )
  )
  def param(self, value1, value2):
      self.assertEqual(value1, value2)

if __name__ == '__main__':
  unittest.main()
```

This gets picked up by the test runner as 3 separate tests:

```
$ python tests.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

## TODO:

The code allows to alter how the generated test methods will be called, but that's not documented yet.
