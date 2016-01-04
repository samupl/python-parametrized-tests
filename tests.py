import unittest

import parametrized


class IsParametrizedTestCase(unittest.TestCase):
    def setUp(self):
        def stub_method(_):
            pass
        self.stub_method = stub_method

    def test_is_parametrized_true(self):
        """

        """
        self.stub_method.parametrized = True
        self.assertTrue(parametrized.is_parametrized(self.stub_method))

    def test_is_parametrized_false(self):
        self.stub_method.parametrized = False
        self.assertFalse(parametrized.is_parametrized(self.stub_method))

    def test_is_parametrized_none(self):
        self.stub_method.parametrized = None
        self.assertFalse(parametrized.is_parametrized(self.stub_method))

    def test_is_parametrized_no_attribute(self):
        self.assertFalse(parametrized.is_parametrized(self.stub_method))


class GenerateMethodNameTestCase(unittest.TestCase):
    def test_simple_callable(self):
        def example():
            pass

        example.parametrized_name = '{method_name}_{iter}'
        example.parametrized_fmt_func = lambda params: {}

        self.assertEqual(
            first=parametrized.generate_method_name(example, 1, []),
            second='test_example_1'
        )

    def test_callable_with_fmt_callback(self):
        def example():
            pass

        example.parametrized_name = '{method_name}_{iter}_{test_fmt}'
        example.parametrized_fmt_func = lambda params: {'test_fmt': 'XXX'}

        self.assertEqual(
            first=parametrized.generate_method_name(example, 1, []),
            second='test_example_1_XXX'
        )


class ParametrizedDecoratorTestCase(unittest.TestCase):
    def test_method_generation(self):
        @parametrized.parametrized_test_case
        class ExampleTestCase:
            @parametrized.parametrized(args=[1, 2, 3])
            def example(self, value):
                pass

        etc = ExampleTestCase()
        self.assertTrue(hasattr(etc, 'test_example_0'))
        self.assertTrue(hasattr(etc, 'test_example_1'))
        self.assertTrue(hasattr(etc, 'test_example_2'))


@parametrized.parametrized_test_case
class ParametrizedDecoratorActuallTestCase(unittest.TestCase):
    @parametrized.parametrized(args=[
        (1, 1),
        (2, 2),
        (3, 3),
        ('abc', 'abc'),
        (1.0, 1.0),
        (0xfe, 0xfe),
        (object, object),
        (str, str),
        ([], []),
        ({}, {}),
        (None, None)
    ])
    def equal(self, value1, value2):
        self.assertEqual(value1, value2)

    @parametrized.parametrized(args=[
        (1, 2),
        (2, 3),
        (3, 4),
        ('abc', 'abc2'),
        (1.0, 1.1),
        (0xfe, 0xfa),
        (str, int),
        ([1], [2]),
        ({1}, {2}),
    ])
    def not_equal(self, value1, value2):
        self.assertNotEqual(value1, value2)

if __name__ == '__main__':
    unittest.main()
