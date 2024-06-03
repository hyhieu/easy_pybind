"""Entry point to generate PyBind11 bindings.

python3 main.py --module-name example
"""

import argparse
from pathlib import Path

from . import file_contents as fc


def _parse_args() -> argparse.Namespace:
    class _CustomHelpFormatter(argparse.HelpFormatter):
        def _format_action_invocation(self, action):
            if action.option_strings == ["--with-gitignore"]:
                return "--[no-]with-gitignore"
            if action.option_strings == ["--with-pytest"]:
                return "--[no-]with-pytest"
            if action.option_strings == ["--with-pymain"]:
                return "--[no-]with-pymain"
            if action.option_strings == ["--cuda"]:
                return "--[no-]cuda"
            return super()._format_action_invocation(action)

    parser = argparse.ArgumentParser(
        prog="easy_pybind", formatter_class=_CustomHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", title="command")
    create_parser = subparsers.add_parser("create", help="Create a pybind project.")

    create_parser.add_argument(
        "--module-name",
        type=str,
        required=True,
        help=("Name of the module to generate bindings for. For instance, if the name "
              "is `cpp_example`, then a folder called `cpp_example` will be created. "
              "Later, when the module is built, you can `import cpp_example` from "
              "to use the module."),
    )

    create_parser.add_argument(
        "--module-path",
        type=Path,
        default=Path("."),
        required=False,
        help="Where the module should be. Default to the current directory.",
    )

    # --with-gitignore
    group = create_parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--with-gitignore",
        dest="with_gitignore",
        action="store_true",
        help=("If given, will add a `.gitignore` file to the module directory to "
              "avoid committing build outputs into GIT."),
    )
    group.add_argument(
        "--no-with-gitignore",
        dest="with_gitignore",
        action="store_false",
        help=argparse.SUPPRESS)
    create_parser.set_defaults(with_gitignore=True)

    # --with-pytest
    group = create_parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--with-pytest",
        dest="with_pytest",
        action="store_true",
        help=("If given, will generate a pytest to smoke test the module.")
    )
    group.add_argument(
        "--no-with-pytest",
        dest="with_pytest",
        action="store_false",
        help=argparse.SUPPRESS)
    create_parser.set_defaults(with_pytest=False)

    # --with-pymain
    group = create_parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--with-pymain",
        dest="with_pymain",
        action="store_true",
        help=("If given, will generate a main.py to import and run the module.")
    )
    group.add_argument(
        "--no-with-pymain",
        dest="with_pymain",
        action="store_false",
        help=argparse.SUPPRESS)
    create_parser.set_defaults(with_pymain=False)

    # --cuda
    group = create_parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--cuda",
        dest="cuda",
        action="store_true",
        help=("If given, will generate a CUDA project instead of a CC project.")
    )
    group.add_argument(
        "--no-cuda",
        dest="cuda",
        action="store_false",
        help=argparse.SUPPRESS)
    create_parser.set_defaults(cuda=False)

    args = parser.parse_args()
    return args


def create(args: argparse.Namespace):
    module_name = args.module_name
    module_path = args.module_path / module_name

    print(f"Generating PyBind11 bindings for project {module_name}...", flush=True)
    module_path.mkdir(parents=True, exist_ok=True)

    (module_path / "build.sh").write_text(fc.build_sh(module_name, use_cuda=args.cuda))
    (module_path / "build.sh").chmod(0o755)

    (module_path / "clean.sh").write_text(fc.clean_sh(module_name))
    (module_path / "clean.sh").chmod(0o755)

    src = module_path / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / f"{module_name}.cc").write_text(fc.project_cc(module_name))
    (src / f"{module_name}_impl.h").write_text(fc.impl_h(module_name))

    if args.cuda:
        (src / f"{module_name}_impl.cu").write_text(fc.impl_cc(module_name))
    else:
        (src / f"{module_name}_impl.cc").write_text(fc.impl_cc(module_name))

    if args.with_gitignore:
        (module_path / ".gitignore").write_text(fc.GITIGNORE)

    if args.with_pytest:
        (module_path / f"{module_name}_test.py").write_text(fc.test_py(module_name))

    if args.with_pymain:
        (module_path / "main.py").write_text(fc.main_py(module_name))


def main():
    args = _parse_args()
    if args.command == "create":
        create(args)
    else:
        raise ValueError(f"Unkonwn command {args.command}.")


if __name__ == "__main__":
    main()
