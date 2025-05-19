# Chapter 7 : Packaging (Poetry) :→

Welcome back! In our previous chapter, Chapter 6: CI/CD (GitHub Actions), we saw how automated checks like running tests and checking code style ensure the quality of the R2R Protocol Python SDK code. This is super important for a reliable tool!

But once the code is checked and verified, how do you actually get that SDK onto your robot or your development machine so you can use the Robot Client to send and receive messages? Do you have to copy and paste all the files manually?

Thankfully, no! This is where **Packaging** comes in.

# **What is Packaging?**

Imagine the R2R Protocol Python SDK is a set of tools (the `Message` class, the `RobotClient`, the `payloads`, etc.). Packaging is the process of gathering all these tools, organizing them correctly, adding some important information about them (like the version number, who made it, what other tools it needs), and bundling them into a standard, easy-to-distribute format.

Think of it like creating a standardized installer file (.exe on Windows, .dmg on Mac, or a .deb/.rpm package on Linux) for a regular computer program. This installer contains everything needed and knows how to put it in the right place on your system.

For Python, the standard way to distribute code is by creating a **Python package**. These packages are then typically uploaded to a central repository like PyPI (the Python Package Index). When you run `pip install r2r-protocol`, the `pip` tool downloads the package from PyPI and installs it on your system, making the `r2r-protocol` library available for your Python programs to `import`.

Packaging ensures:

1. **Easy Distribution:** Developers can share their code easily.
2. **Easy Installation:** Users can install the code and its dependencies with simple commands like `pip install`.
3. **Dependency Management:** The package specifies what other libraries it needs to run (its dependencies), and the installer handles getting them.
4. **Version Control:** Each package has a version number, so users can install specific versions and developers can manage updates.

# **Why Packaging is Important for R2R Protocol**

For the R2R Protocol Python SDK, packaging is crucial because it allows robot developers everywhere to easily install and use the SDK without needing to know the internal structure of the source code repository. They can simply `pip install r2r-protocol`, and they get all the necessary code (Messages, Message Types, Payloads, Robot Client) ready to use in their own projects.

# **Introducing Poetry**

The R2R Protocol project uses a tool called **Poetry** for managing its Python package. Poetry is a modern tool that helps with:

- **Dependency Management:** Defining what libraries your project needs and installing them.
- **Packaging:** Specifying how your code should be bundled.
- **Building:** Creating the distribution files (the actual packages).
- **Publishing:** Uploading the packages to PyPI or other repositories.

Poetry uses a single file, `pyproject.toml`, to manage the project's metadata, dependencies, and packaging configuration.

# **Poetry's Configuration: `pyproject.toml`**

Let's look at the `pyproject.toml` file located in the `sdk/python` directory of the R2R Protocol repository. This file tells Poetry everything it needs to know about the `r2r-protocol` Python package.

Here are the key parts relevant to packaging:

```toml
# File: sdk/python/pyproject.toml

[
tool.poetry
] # This section configures Poetry
name = "r2r_protocol" # The name of the package (what you use in 'pip install')
version = "2.0.0"  # The current version number of the package
description = "Robot-to-Robot (R2R) Communication Protocol SDK in Python" # A short description
authors = ["Tech-Parivartan <techparivartan022@gmail.com>"] # Who created it
readme = "README.md" # Where to find the README file for the package listing
license = "Apache-2.0" # The license under which the code is distributed
requires-python = ">=3.7" # Minimum Python version required to use this package

packages = [ # This tells Poetry where to find the actual code files
    { include = "r2r_protocol", from = "sdk/python" }, # Look in sdk/python for a folder named r2r_protocol
]

# Other sections like dependencies and build system are also here

```

**Explanation:**

- `[tool.poetry]`: This marks the section for Poetry's configuration.
- `name`: This is the public name of the package on PyPI. When you run `pip install r2r-protocol`, `pip` looks for a package with this name.
- `version`: This is the package's version number. It's important for tracking changes and updates. Users can request specific versions.
- `description`, `authors`, `readme`, `license`: These provide important information about the package that is displayed on PyPI and included in the package metadata.
- `requires-python`: This specifies which Python versions are compatible with this package. If a user tries to install it with an older Python version, `pip` or Poetry will show an error.
- `packages`: This crucial part tells Poetry *where* the actual Python code that makes up the library is located within the project's files. Here, it says to include the directory named `r2r_protocol` which is located inside the `sdk/python` directory. This `r2r_protocol` directory contains files like `message_format.py`, `message_types.py`, `payloads.py`, `client.py`, etc., which become the modules you `import` after installation.

# **Dependency Management with Poetry**

Poetry also manages the project's dependencies – other Python libraries that the `r2r-protocol` SDK needs to function.

```toml
# File: sdk/python/pyproject.toml (Dependencies section)

[
tool.poetry.dependencies
] # Libraries needed for the package to run
python = ">=3.7" # Specifies the Python versions

[
tool.poetry.group.dev.dependencies
] # Libraries ONLY needed for development/testing
pytest = "^8.3.5" # pytest is used for running tests (see CI/CD chapter)

```

**Explanation:**

- `[tool.poetry.dependencies]`: This lists the libraries required by the `r2r-protocol` SDK when it's installed and used by someone. In this case, the only dependency listed is the Python version itself (which is handled by the `requires-python` field above), meaning the SDK is designed to be relatively self-contained and doesn't rely on many external libraries for its core function.
- `[tool.poetry.group.dev.dependencies]`: These are libraries needed only by developers working *on* the R2R Protocol SDK project itself, for things like running tests (`pytest`), checking code style, building documentation, etc. These dependencies are *not* installed when a user simply installs the `r2r-protocol` package to use it in their robot application. This separation is important for keeping user installations lean.

Poetry keeps track of exact dependency versions in a `poetry.lock` file, ensuring builds are repeatable.

# **Building the Package**

Once the `pyproject.toml` is configured, Poetry can **build** the package distribution files. This is the step that creates the bundles ready for distribution.

A developer working on the project (or more commonly, the CI/CD pipeline) would run a command like this from the `sdk/python` directory:

```bash
poetry build
```

This command instructs Poetry to read the `pyproject.toml` file and create the standard distribution formats. The main formats are:

- **sdist (Source Distribution):** A `.tar.gz` file containing the source code and metadata.
- **Wheel:** A `.whl` file (pronounced "wheel"). This is a pre-built format that doesn't require compilation steps during installation, making `pip install` faster. It's the preferred format for many packages.

After running `poetry build`, you would find these files in a new `dist/` directory inside `sdk/python`, looking something like this:

```bash
sdk/python/
├── dist/
│   ├── r2r_protocol-2.0.0.tar.gz  # Source distribution
│   └── r2r_protocol-2.0.0-py3-none-any.whl # Wheel distribution
├── r2r_protocol/ # The actual SDK code directory
│   ├── __init__.py
│   ├── client.py
│   ├── message_format.py
│   ├── message_types.py
│   ├── payloads.py
│   └── ...
├── tests/ # Test files
│   └── ...
├── pyproject.toml # Poetry configuration
├── poetry.lock    # Poetry dependency lock file
└── README.md
```


These files in the `dist/` directory are the actual packages ready to be shared.

# **Publishing the Package**

After building, the wheel and sdist files can be **published**. The most common place for Python packages is PyPI (pypi.org).

Publishing makes the package available for anyone to install using `pip`. The command to publish using Poetry is:

```bash
poetry publish
```

This command uploads the packages from the `dist/` directory to PyPI (you need an account and API key configured).

**Connecting to CI/CD:** In many projects, including potentially the R2R Protocol in the future (or in a slightly more complex setup), the CI/CD pipeline (Chapter 6: CI/CD (GitHub Actions)) will automate this build and publish process. After the tests pass on the `main` branch for a new version tag, the CI workflow might trigger the `poetry build` and then `poetry publish` commands automatically. This ensures that every verified version is made available quickly and correctly.

# **How Packaging Works Under the Hood (Simplified Flow)**

Here's a simple sequence of how Poetry helps get the SDK from the project code to a user's computer:


![1_Chapter_7_Packaging_(Poetry)](./1_Chapter_7_Packaging_(Poetry).png)

This flow shows how Poetry acts as the intermediary, using the configuration file to bundle the code and make it available via PyPI, which is then used by the standard `pip` installer.

You can even see Poetry being used in the provided `Dockerfile` snippet for the SDK:

```dockerfile
# Snippet from Dockerfile
COPY sdk/python/pyproject.toml sdk/python/poetry.lock* ./
RUN pip install poetry && \ # Install Poetry first
    poetry config virtualenvs.create false && \ # Configure Poetry
    poetry install --no-dev --no-interaction --no-ansi # Use Poetry to install dependencies

COPY sdk/python/r2r_protocol ./r2r_protocol # Copy the actual code
```

This snippet from the `Dockerfile` (which is used to build a Docker image for the SDK) shows that even during the build process of a Docker image, Poetry is used to install the project's dependencies *before* the SDK's own code is copied into the right place. The `--no-dev` flag is used here specifically to tell Poetry *not* to install the development dependencies (like `pytest`), only the core dependencies needed to run the code, which is standard practice for deployment environments.

# **Conclusion**

Packaging, handled by tools like Poetry, is how the R2R Protocol Python SDK is transformed from source code files in a repository into a standardized, easily installable bundle. Poetry uses the `pyproject.toml` file to define the package's identity, metadata, included code, and dependencies. Running `poetry build` creates the distribution files (`.whl`, `.tar.gz`), and `poetry publish` uploads them to PyPI, making the SDK accessible via `pip install r2r-protocol`. This process, often automated by CI/CD, is vital for distributing and maintaining the SDK for the broader robot development community.

With this chapter, we've completed our initial exploration of the R2R Protocol, from the high-level concept to the fundamental message structure, message types, payloads, the Python SDK for practical use, the CI/CD process ensuring code quality, and finally, how the SDK is packaged for easy distribution.

You now have a foundational understanding of how the R2R Protocol works and how its Python SDK is built and managed. This knowledge will be invaluable as you delve deeper into robot communication and contribute to or use the R2R Protocol in your own projects.

This concludes our introductory tutorial series on the R2R Protocol. We hope this has been a helpful starting point for your journey into the world of robot communication!


