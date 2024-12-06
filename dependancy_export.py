import subprocess
import json


def export_conda_env():
    """
    Export conda environment dependencies to requirements.txt
    excluding version numbers and conda-specific packages
    """
    # Get list of all installed packages in JSON format
    result = subprocess.run(['conda', 'list', '--json'], capture_output=True, text=True)
    packages = json.loads(result.stdout)

    # Filter out conda-specific packages and base Python
    excluded_packages = {'python', 'pip', 'setuptools', 'wheel', 'conda', 'conda-build'}

    with open('requirements.txt', 'w') as f:
        for package in packages:
            name = package['name']
            if name not in excluded_packages:
                # Write package name with its version
                if 'version' in package:
                    f.write(f"{name}=={package['version']}\n")
                else:
                    f.write(f"{name}\n")


if __name__ == "__main__":
    export_conda_env()