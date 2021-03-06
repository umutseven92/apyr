import pytest

from apyr.exceptions import FunctionException
from apyr.function_handler import FunctionHandler


class TestFunctions:
    def test_can_parse_single_line_content(self):
        content = """%random_last_name(first, second)%"""
        functions = FunctionHandler.parse_content(content)

        assert len(functions) == 1
        function = functions[0]

        assert function.full == "%random_last_name(first, second)%"
        assert function.name == "random_last_name"
        assert function.params == ["first", "second"]

    def test_can_parse_multi_line_content(self):
        content = """
        %random_last_name(first, second)%
        %random_first_name(third, fourth)%
        """
        functions = FunctionHandler.parse_content(content)

        assert len(functions) == 2

        assert functions[0].full == "%random_last_name(first, second)%"
        assert functions[0].name == "random_last_name"
        assert functions[0].params == ["first", "second"]

        assert functions[1].full == "%random_first_name(third, fourth)%"
        assert functions[1].name == "random_first_name"
        assert functions[1].params == ["third", "fourth"]

    def test_wont_parse_incorrect_functions(self):
        content = """
        %%
        %random_first_name%
        %random_first_name()%
        %random_first_%name()%
        %random_first_name(first)%
        %random_first_name%(first, second)%
        %random_first_name(first, second)%
        %random_first_name%(first,second)%
        %random_first_name(first,second)%

        { "first_name": "%random_first_name()%", "last_name": "%random_last_name(abc)%" }
        """

        functions = FunctionHandler.parse_content(content)

        assert len(functions) == 7

        assert functions[0].full == "%random_first_name()%"
        assert functions[0].name == "random_first_name"
        assert functions[0].params == []

        assert functions[1].full == "%name()%"
        assert functions[1].name == "name"
        assert functions[1].params == []

        assert functions[2].full == "%random_first_name(first)%"
        assert functions[2].name == "random_first_name"
        assert functions[2].params == ["first"]

        assert functions[3].full == "%random_first_name(first, second)%"  # Space
        assert functions[3].name == "random_first_name"
        assert functions[3].params == ["first", "second"]

        assert functions[4].full == "%random_first_name(first,second)%"  # No space
        assert functions[4].name == "random_first_name"
        assert functions[4].params == ["first", "second"]

        assert functions[5].full == "%random_first_name()%"
        assert functions[5].name == "random_first_name"
        assert functions[5].params == []

        assert functions[6].full == "%random_last_name(abc)%"
        assert functions[6].name == "random_last_name"
        assert functions[6].params == ["abc"]

    def test_can_execute_functions(self):
        content = """
        {
          "first_name": "%random_first_name(m)%",
          "last_name": "%random_last_name()%",
          "age": %random_int(0, 50)%
        }
        """

        mock_functions = {
            "random_first_name": lambda x: "Harry",
            "random_last_name": lambda: "Canyon",
            "random_int": lambda x, y: 42,
        }

        exec_content = FunctionHandler.run(content, mock_functions)

        assert (
            exec_content
            == """
        {
          "first_name": "Harry",
          "last_name": "Canyon",
          "age": 42
        }
        """
        )

    def test_will_raise_function_exception(self):
        content = """
        {
          "age": "%random_int(5, abc)%",
        }
        """

        def add_two(x, y):
            val = int(x) + int(y)
            return val

        mock_functions = {"random_int": add_two}  # Should fail

        with pytest.raises(FunctionException):
            FunctionHandler.run(content, mock_functions)
