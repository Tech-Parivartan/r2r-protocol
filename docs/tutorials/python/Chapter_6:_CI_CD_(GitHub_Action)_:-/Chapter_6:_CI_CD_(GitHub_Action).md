# Chapter 6 : CI/CD (GitHub Actions) :→

Welcome back! In the previous chapters, we've learned about the core concepts of the R2R Protocol: the standard language itself (Chapter 1: R2R Protocol), the fundamental Message structure, the meaning of Message Types, and how Payloads carry the specific data. In Chapter 5: Robot Client (Python SDK), we saw how you can use the Python SDK to write code for your robot to send and receive these messages.

Now, let's think about the R2R Protocol project itself. It provides the standard definitions and, importantly, the SDKs (like the Python one) that developers worldwide will use to build reliable robot communication. How can the project maintain the *quality* and *reliability* of this code as different contributors make changes? How can we be sure that a new change doesn't accidentally break the ability of a `RobotClient` to connect or correctly send a `STATUS` message?

This is where **CI/CD (Continuous Integration / Continuous Deployment)** comes in!

# **What is CI/CD?**

Imagine the R2R Protocol code is a product you are building with a team. Every time someone adds a new feature or fixes a bug, you need to make sure their changes haven't broken anything else in the product. Doing this manually every time would be slow and error-prone.

**CI/CD** is like having an **automated quality control and delivery team** for your code project.

- **CI stands for Continuous Integration:** Every time a developer integrates their changes (pushes code to the main repository, or creates a Pull Request), an automated system **builds** the project, **runs tests** (like the ones we saw in Chapter 5), and performs other **automated checks** (like checking code style). If any of these steps fail, the system immediately reports it, telling the developer, "Hey, your change seems to have introduced a problem!" This catches bugs and issues *early* before they cause bigger problems.
- **CD stands for Continuous Deployment / Continuous Delivery:** If the CI checks pass, the automated system can then automatically **prepare the code for release** (Deployment) or even **deploy it** to users (Delivery). For the R2R Python SDK, this means automatically packaging it and publishing it to a place like PyPI (the Python Package Index) so others can easily install it (`pip install r2r-protocol`).

The goal of CI/CD is to ensure that the project's codebase is **always in a working, releasable state** and that new changes are verified automatically and quickly.

# **Why is CI/CD Important for R2R Protocol?**

For a project like R2R Protocol, which provides fundamental building blocks (the standard) and tools (the SDKs) for robot developers:

1. **Reliability:** Robots depending on the SDK need it to be reliable. CI ensures that core functionality (like sending/receiving messages) isn't broken by new changes.
2. **Code Quality:** Automated checks like linters (which check code style and potential simple errors) ensure the code is consistent and easier for everyone to read and maintain.
3. **Faster Development:** Developers get quick feedback on their changes. They don't have to manually run all tests before submitting code, and they know right away if they've broken something.
4. **Trust:** CI/CD builds confidence in the project. Users can see that automated checks are in place (often shown with badges like in the README!) and that releases are coming from a verified process.

# **How R2R Protocol Uses GitHub Actions for CI/CD**

The R2R Protocol project uses **GitHub Actions** to implement its CI/CD pipeline. GitHub Actions is a service provided by GitHub that allows you to automate tasks directly in your GitHub repository. These automated tasks are defined in configuration files called **workflows**, written in YAML format and stored in the `.github/workflows` directory.

The R2R Protocol uses workflows for things like:

1. Running tests (Continuous Integration)
2. Checking code style (Continuous Integration)
3. Eventually, publishing the package (Continuous Deployment/Delivery - covered partially by packaging in the next chapter, but triggered by CI success).

Let's look at the core workflow files used for CI.

# **1. The Main CI Workflow (`ci.yml`)**

This workflow is the heart of the Continuous Integration process. Its main job is to make sure the code **builds and passes its tests** every time a change is pushed or a pull request is created for the `main` branch.

Look at a simplified version of the workflow definition found in `.github/workflows/ci.yml`:

```yaml
# File: .github/workflows/ci.yml
name: Python CI # A friendly name for the workflow

on: # When this workflow should run
  push: # Run on code pushes
    branches: [main] # Only if the push is to the 'main' branch
  pull_request: # Run when a pull request is created/updated
    branches: [main] # Only if the PR targets the 'main' branch

jobs: # The tasks (jobs) to perform
  build: # A job named 'build'
    runs-on: ubuntu-latest # Run this job on a virtual machine using the latest Ubuntu Linux

    steps: # The individual steps within the 'build' job
      - name: Checkout code # Step 1: Get the code from the repository
        uses: actions/checkout@v3 # Use a pre-built action to checkout the code

      - name: Set up Python 3.10 # Step 2: Configure the Python environment
        uses: actions/setup-python@v4 # Use a pre-built action to set up Python
        with:
          python-version: '3.10' # Specify which Python version to use

      - name: Install dependencies # Step 3: Install necessary libraries
        run: | # Run these commands in the virtual machine's terminal
          python -m pip install --upgrade pip # Upgrade pip installer
          pip install pytest # Install the test runner library
          cd sdk/python # Change directory to the Python SDK folder
          pip install -e . # Install the SDK itself in editable mode

      - name: Run tests # Step 4: Execute the tests
        run: pytest tests # Run the pytest command in the sdk/python/tests directory (relative to the cd command)
```

**Explanation:**

- **`name: Python CI`**: This gives the workflow a clear name you'll see on GitHub.
- **`on:`**: This tells GitHub *when* to run this workflow. Here, it runs on `push` events to the `main` branch and on `pull_request` events targeting the `main` branch. This means every code change gets automatically checked!
- **`jobs:`**: A workflow can have one or more jobs. This workflow has one job called `build`.
- **`runs-on: ubuntu-latest`**: This specifies that the job should run on a fresh virtual machine hosted by GitHub, configured with the latest Ubuntu Linux.
- **`steps:`**: These are the individual commands or actions the job executes sequentially.
    - `Checkout code`: This standard step gets a copy of your repository's code onto the virtual machine.
    - `Set up Python`: This action configures the specified Python version (3.10 in this case) on the virtual machine so you can run Python commands.
    - `Install dependencies`: These commands use `pip` to install the required Python packages. `pytest` is needed to run the tests, and `pip install -e .` inside `sdk/python` installs the `r2r-protocol` package itself, making its modules available.
    - `Run tests`: This command executes the tests located in the `tests` directory of the Python SDK. If any test fails, this step fails, and the entire job fails.

If all steps in this `build` job complete successfully, the check for that commit or pull request passes, giving confidence that the code is working. If any step fails (e.g., `pip install` has an error because of a dependency issue, or `pytest` finds a bug), the job fails, and the developer is notified.

# **2. The Python Linter Workflow (`python-linter.yml`)**

Beyond just working, code should also be readable and follow consistent style guidelines. Linting is an automated check that helps enforce these standards and catch common, simple programming errors. The R2R Protocol uses `flake8` for linting Python code.

Here's a simplified look at the linter workflow from `.github/workflows/python-linter.yml`:

```yaml
# File: .github/workflows/python-linter.yml
name: Python Linter # Name for the linter workflow

on:
  push:
    branches: [main] # Run on pushes to main
    paths: # ONLY run if files in these paths change
      - 'sdk/python/**.py'
      - '.github/workflows/python-linter.yml'
  pull_request:
    branches: [main] # Run on PRs targeting main
    paths: # ONLY run if files in these paths change
      - 'sdk/python/**.py'
      - '.github/workflows/python-linter.yml'

jobs:
  lint-python-code: # A job named 'lint-python-code'
    runs-on: ubuntu-latest # Run on a fresh Ubuntu VM

    steps:
      - name: Check out repository code # Step 1: Get the code
        uses: actions/checkout@v4

      - name: Set up Python # Step 2: Configure Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11' # Using a specific Python version for consistency

      - name: Install linter # Step 3: Install the linting tool
        run: |
          python -m pip install --upgrade pip
          pip install flake8 # Install the flake8 linter

      - name: Run Flake8 # Step 4: Execute the linter check
        run: |
          # Run flake8 on the 'sdk/python' directory
          # The flags tell flake8 what to check and how to report
          flake8 sdk/python --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 sdk/python --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

**Explanation:**

- **`name: Python Linter`**: Workflow name.
- **`on: ... paths:`**: This is a useful optimization. This workflow *only* runs if files within the `sdk/python` directory (specifically `.py` files) or the workflow file itself change. This saves computing resources compared to running it on every single commit in the repository if only non-Python files are changed.
- **`jobs: lint-python-code`**: The job name.
- **`runs-on: ubuntu-latest`**: Runs on a fresh VM.
- **`steps:`**:
    - `Checkout code`: Gets the code.
    - `Set up Python`: Configures Python.
    - `Install linter`: Installs the `flake8` tool.
    - `Run Flake8`: Executes the `flake8` command on the `sdk/python` directory. The various flags configure flake8's behavior (what errors/warnings to look for, line length limits, etc.). If `flake8` finds violations based on these rules, this step fails.

This linter workflow acts as an automated code reviewer, ensuring that contributions adhere to the project's coding style, making the codebase cleaner and more consistent.

# **How it Works Under the Hood (Conceptual Flow)**

Let's visualize what happens when a developer pushes a change to GitHub:


![1_Chapter_6_CI_CD_(GitHub_Action)](./1_Chapter_6_CI_CD_(GitHub_Action).png)

This flow shows how GitHub Actions automates the process. It listens for events (like pushes), finds the relevant workflow files, sets up temporary environments (virtual machines), runs the defined steps, and reports the outcome back to the repository. This provides immediate feedback on the health of the code after every change.

You can see the results of these workflows directly on the R2R Protocol GitHub page, often linked as badges in the `README.md` file:

```python

# Snippet from README.md
[![Build Status](https://github.com/Tech-Parivartan/r2r-protocol/actions/workflows/ci.yml/badge.svg)](https://github.com/Tech-Parivartan/r2r-protocol/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/r2r-protocol.svg)](https://pypi.org/project/r2r-protocol/)
...
``` 

The "Build Status" badge directly reflects the outcome of the `ci.yml` workflow – green means the latest changes passed all tests!

# **Conclusion**

CI/CD, powered by tools like GitHub Actions, is essential for maintaining the quality and reliability of collaborative software projects like the R2R Protocol SDK. Continuous Integration automatically builds, tests, and checks code style whenever changes are made, catching errors early. This ensures that the Python SDK you use in your robots (as explored in Chapter 5: Robot Client (Python SDK)) is robust and dependable. Continuous Deployment/Delivery, which often follows successful CI, automates the release process, making new versions of the SDK easily available.

We've now seen how the protocol is defined, how messages are structured, and how the Python SDK lets you use it. We've also peeked behind the scenes at how the project ensures the quality of that very SDK.

Next, we'll look at another aspect of managing the SDK: packaging. How is the Python SDK prepared so you can simply install it with `pip install r2r-protocol`?

Ready to learn about how the R2R Protocol Python SDK is packaged for distribution? Let's move on to Chapter 7: Packaging (Poetry)!


