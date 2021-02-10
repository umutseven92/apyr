import re
from typing import List, Tuple, Dict

from apyr.exceptions import FunctionException
from apyr.models import ContentFunction


class FunctionHandler:
    @staticmethod
    def parse_content(content: str) -> List[ContentFunction]:
        regex = re.compile(
            r"(?P<full>%(?P<name>[^%]+?)\((?P<params>.*?)\)%)", flags=re.M
        )
        match: List[Tuple[str, str, str]] = regex.findall(content)

        functions: List[ContentFunction] = []

        for capture in match:
            full, name, params = capture
            param_mapped = list(
                map(lambda x: x.strip(), params.split(","))
            )  # Remove whitespace from params
            param_list = list(
                filter(lambda x: x != "", param_mapped)
            )  # Filter out empty params
            functions.append(ContentFunction(full=full, name=name, params=param_list))

        return functions

    @staticmethod
    def execute_functions(
        content_functions: List[ContentFunction], functions: Dict, content: str
    ) -> str:
        for content_function in content_functions:
            fun = functions.get(content_function.name)

            if fun is None:
                print(f"Function {content_function.name} not found. Skipping..")
                continue

            try:
                result = fun(*content_function.params)
            except Exception as ex:
                raise FunctionException(content_function.full, str(ex)) from ex

            content = content.replace(content_function.full, str(result))

        return content

    @staticmethod
    def run(content: str, functions: Dict) -> str:
        content_functions = FunctionHandler.parse_content(content)
        return FunctionHandler.execute_functions(content_functions, functions, content)
