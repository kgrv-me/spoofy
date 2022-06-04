# This file defines how PyOxidizer application building and packaging is
# performed. See PyOxidizer's documentation at
# https://pyoxidizer.readthedocs.io/en/stable/ for details of this
# configuration file format.

def make_exe():
    dist = default_python_distribution()

    policy = dist.make_python_packaging_policy()
    policy.bytecode_optimize_level_zero = False
    policy.bytecode_optimize_level_one = False
    policy.bytecode_optimize_level_two = True
    policy.include_non_distribution_sources = False

    python_config = dist.make_python_interpreter_config()
    python_config.optimization_level = 2
    python_config.run_module = "spoofy"

    exe = dist.to_python_executable(
        name="SPOOFY",
        packaging_policy=policy,
        config=python_config
    )
    exe.windows_subsystem = "console"
    exe.add_python_resources(exe.read_package_root(
       path=CWD,
       packages=["spoofy"]
    ))
    exe.add_python_resources(exe.read_package_root(
       path="venv/lib/python3.10/site-packages",
       packages=["manuf", "scapy"]
    ))

    return exe

def make_install(exe):
    # Create an object that represents our installed application file layout.
    files = FileManifest()

    # Add the generated executable to our install layout in the root directory.
    files.add_python_resource(".", exe)

    return files

# Tell PyOxidizer about the build targets defined above.
register_target("exe", make_exe)
register_target("Spoofy", make_install, depends=["exe"], default=True)

# Resolve whatever targets the invoker of this configuration file is requesting
# be resolved.
resolve_targets()
