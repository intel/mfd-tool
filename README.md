> [!IMPORTANT]  
> This project is under development. All source code and features on the main branch are for the purpose of testing or evaluation and not production ready.

# MFD Base Tool
Module for abstraction of tool (wrappers).

ToolTemplate has got 3 main methods:

* `_get_tool_exec_factory(self) -> str` - responsible to return correct tool execute name according to e.g. OS. Should use `tool_executable_name` structure as store for names.
* `check_if_available(self) -> None` - responsible for checking, if tool is available and executable in system. Should raise exception if not
* `get_version(self) -> str` - responsible for getting version of tool.

All methods and `tool_executable_name` variable in class must be implemented in developed tool.
Arguments in public methods must be forced as named arguments:
`__init__(self, *, arg1, arg2)` etc.

## Usage
Example implementation using ToolTemplate:

```python
from mfd_base_tool import ToolTemplate


class MyTool(ToolTemplate):
    tool_executable_name = "my tool name"
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
```
## OS supported:
* LNX
* WINDOWS
* ESXI
* FREEBSD
* EFI shell support

## Issue reporting

If you encounter any bugs or have suggestions for improvements, you're welcome to contribute directly or open an issue [here](https://github.com/intel/mfd-base-tool/issues).