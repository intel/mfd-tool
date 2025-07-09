# Copyright (C) 2025 Intel Corporation
# SPDX-License-Identifier: MIT
"""Tests for `mfd_base_tool` package."""

import pytest

from mfd_base_tool import ToolTemplate
from mfd_connect import Connection
from mfd_typing import OSType


class TestTool:
    class_under_test = ToolTemplate

    @pytest.fixture()
    def conn(self, mocker):
        conn = mocker.create_autospec(Connection)
        return conn

    @pytest.fixture()
    def tool_initializable_class(self, mocker, conn):
        tool_class = self.class_under_test
        if hasattr(tool_class, "__abstractmethods__"):
            # Remove abstract methods, if any so the class can be instantiated
            tool_class.__abstractmethods__ = []
        tool_class.tool_executable_name = mocker.sentinel.tool_executable_name
        tool_class._connection = conn
        return tool_class

    @pytest.fixture()
    def tool(self, tool_initializable_class, conn, mocker):
        mocker.patch("mfd_base_tool.ToolTemplate.__init__", mocker.Mock(return_value=None))
        tool = tool_initializable_class(connection=conn)
        tool._tool_exec = mocker.sentinel.tool_exec
        return tool

    def test_class_cannot_be_initialized(self, conn):
        with pytest.raises(TypeError):
            _ = self.class_under_test(connection=conn)

    def test_check_if_available_not_implemented(self, tool):
        with pytest.raises(NotImplementedError):
            tool.check_if_available()

    def test_get_version_not_implemented(self, tool):
        with pytest.raises(NotImplementedError):
            tool.get_version()

    def test__get_tool_exec_factory_not_implemented(self, tool):
        with pytest.raises(NotImplementedError):
            tool._get_tool_exec_factory()

    @pytest.mark.parametrize(
        "tool_name, path, os_type, expected_path",
        [
            ("tool.exe", "c:\\windows\\", OSType.WINDOWS, "c:\\windows\\tool.exe"),
            ("tool", r"/root/dir", OSType.POSIX, "/root/dir/tool"),
        ],
    )
    def test__get_tool_exec(self, tool, mocker, tool_name, path, os_type, expected_path):
        tool._get_tool_exec_factory = mocker.create_autospec(tool._get_tool_exec_factory, return_value=tool_name)
        tool._connection.get_os_type.return_value = os_type
        assert tool._get_tool_exec(path) == expected_path

    @pytest.mark.parametrize(
        "path, expected_path, tool_name, os_type",
        [
            ("c:\\windows", "c:\\windows\\tool.exe", "tool.exe", OSType.WINDOWS),
            (r"/root/dir", "/root/dir/tool", "tool", OSType.POSIX),
        ],
    )
    def test__get_tool_exec_unsupported_path_connection(self, tool, mocker, path, expected_path, tool_name, os_type):
        tool._get_tool_exec_factory = mocker.create_autospec(tool._get_tool_exec_factory, return_value=tool_name)
        tool._connection.path.side_effect = NotImplementedError
        tool._connection.get_os_type.return_value = os_type
        assert tool._get_tool_exec(path) == expected_path

    def test__get_tool_exec_unsupported_connection_exception(self, tool, mocker):
        tool._get_tool_exec_factory = mocker.create_autospec(tool._get_tool_exec_factory, return_value="tool")
        tool._connection.path.side_effect = NotImplementedError
        tool._connection.get_os_type.side_effect = NotImplementedError

        with pytest.raises(TypeError, match="Type of connection not supported."):
            tool._get_tool_exec("path")
