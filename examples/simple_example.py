# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
from mfd_tool import ToolTemplate


class MyTool(ToolTemplate):
    tool_executable_name = "sample64e"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_tool_exec_factory(self) -> str:
        return self.tool_executable_name

    def check_if_available(self) -> None:
        if not "if statement for check":
            raise MyToolNotAvailable()

    def get_version(self) -> str:
        return "my read tool version"

    def my_tool_method(self):
        pass

my_tool = MyTool(connection=<connection>, absolute_path_to_binary_dir="/path/to/binary/dir")