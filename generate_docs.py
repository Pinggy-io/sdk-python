import inspect
import importlib
from typing import List, Union


def generate_markdown_doc_from_google_style(
    module_name: str,
    output_file: str = "API_DOC.md",
    skip_classes: List[str] = None,
    skip_functions: List[str] = None,
    skip_modules: List[str] = None,
):
    skip_classes = set(skip_classes or [])
    skip_functions = set(skip_functions or [])
    skip_modules = set(skip_modules or [])

    try:
        mod = importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise RuntimeError(f"Module '{module_name}' not found")

    def is_public(name: str) -> bool:
        return not name.startswith("_")

    def format_signature(obj):
        try:
            return str(inspect.signature(obj))
        except (ValueError, TypeError):
            return ""

    def parse_google_docstring(doc: str):
        """Converts Google-style docstring into markdown format."""
        lines = doc.strip().splitlines()
        formatted = []

        in_args_section = False
        in_returns_section = False
        arg_indent = None  # baseline indent of param entries inside Args:

        for line in lines:
            # Handle Args section
            if line.startswith("Args:"):
                in_args_section = True
                arg_indent = None
                formatted.append("**Arguments**:")
                continue
            if in_args_section:
                # Blank lines inside the Args block are just spacing — pass
                # them through but don't end the section. The section ends
                # when we hit an unindented non-empty line (a new section
                # header like Returns: or free prose).
                if line.strip() == "":
                    formatted.append("")
                    continue
                if not (line.startswith(" ") or line.startswith("\t")):
                    in_args_section = False
                    # fall through to normal handling
                else:
                    # A param entry looks like `name: description` or
                    # `name (type): description`. Continuation lines may
                    # have no colon, or may have a colon embedded in prose
                    # (e.g. "Example: 80"). Distinguish them by indent: the
                    # first param line establishes a baseline, and only
                    # lines at that same indent count as new params.
                    line_indent = len(line) - len(line.lstrip())
                    head, sep, tail = line.partition(":")
                    head_clean = head.strip()
                    looks_like_param = (
                        sep
                        and head_clean
                        and " " not in head_clean.split("(")[0].strip()
                    )
                    if looks_like_param and arg_indent is None:
                        arg_indent = line_indent
                    is_new_param = (
                        looks_like_param
                        and arg_indent is not None
                        and line_indent <= arg_indent
                    )
                    if is_new_param:
                        formatted.append(f"- **{head_clean}**: {tail.strip()}")
                    else:
                        formatted.append(f"  {line.strip()}")
                    continue

            # Handle Returns section
            if line.startswith("Returns:"):
                in_returns_section = True
                formatted.append("**Returns**:")
                continue
            if in_returns_section:
                if line.strip() == "":
                    in_returns_section = False
                else:
                    return_type, return_description = line.split(":", 1)
                    return_type = return_type.strip()
                    return_description = return_description.strip()
                    formatted.append(f"- **{return_type}**: {return_description}")
                    continue

            # Handle normal docstring text
            formatted.append(line)

        return "\n".join(formatted)

    def write_doc(f, name: str, obj: Union[callable, type], kind="function"):
        doc = inspect.getdoc(obj) or "*No docstring provided.*"
        signature = format_signature(obj) if kind == "function" else ""
        f.write(f"### `{name}{signature}`\n\n")
        formatted_doc = parse_google_docstring(doc)
        f.write(f"{formatted_doc}\n\n")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Documentation for `{module_name}`\n\n")

        if module_name in skip_modules:
            f.write("This module was skipped.\n")
            return

        members = inspect.getmembers(mod, predicate=lambda x: inspect.isfunction(x) or inspect.isclass(x))
        public_members = [(name, obj) for name, obj in members if is_public(name)]

        for name, obj in public_members:
            if inspect.isfunction(obj):
                if name in skip_functions:
                    continue
                write_doc(f, name, obj)
            elif inspect.isclass(obj):
                if name in skip_classes:
                    continue
                f.write(f"## Class `{name}`\n\n")
                class_doc = inspect.getdoc(obj) or "*No class docstring.*"
                f.write(f"{class_doc}\n\n")

                # Document methods and properties
                for meth_name, meth_obj in inspect.getmembers(obj):
                    if not is_public(meth_name) or meth_name in skip_functions:
                        continue
                    if inspect.isfunction(meth_obj) or inspect.ismethod(meth_obj):
                        write_doc(f, f"{name}.{meth_name}", meth_obj)
                    elif isinstance(meth_obj, property):
                        write_doc(f, f"{name}.{meth_name}", meth_obj.fget, kind="property")

    print(f"✅ Markdown documentation written to: {output_file}")


# Legacy surface kept for backwards compatibility but excluded from public docs.
# These names are still callable so old user code does not crash, but the
# documented flow is the new one (start_tunnel / Tunnel.start / forwardings /
# add_forwarding) only.
LEGACY_NAMES = [
    # Legacy flow methods on Tunnel
    "connect",
    "request_primary_forwarding",
    "serve_tunnel",
    "start_with_c",
    # Legacy forwarding properties on Tunnel
    "tcp_forward_to",
    "udp_forward_to",
    "type",
    "udp_type",
    # Legacy callbacks on BaseTunnelHandler
    "authenticated",
    "authentication_failed",
    "primary_forwarding_succeeded",
    "primary_forwarding_failed",
]

generate_markdown_doc_from_google_style(
    module_name="pinggy",
    output_file="API_DOC.md",
    skip_classes=["Channel"],
    skip_functions=LEGACY_NAMES,
)
