# Contributing

Thank you for your interest in contributing to `kneed`! There are many ways to help:

- Submit a bug report or feature request on [GitHub Issues](https://github.com/arvkevi/kneed/issues)
- Contribute a Jupyter notebook to [notebooks](https://github.com/arvkevi/kneed/tree/main/notebooks)
- Document applications where `kneed` could be useful
- Code improvements and bug fixes

## Getting Started

A typical workflow for a contributor:

1. **Discover** a bug or a feature by using the package.
2. **Discuss** the bug or feature by [adding an issue](https://github.com/arvkevi/kneed/issues).
3. **Fork** the repository into your own GitHub account.
4. Create a **Pull Request** to [suggest modifications](https://github.com/arvkevi/kneed/pulls).
5. **Code** the feature, add a test, add your contribution. **Make sure the tests pass.**
6. **Review** the code with the repository owner.
7. **Merge** the contribution.

### Forking the Repository

The first step is to fork the repository into your own account. Click the **"Fork"** button in the upper right corner of the [kneed GitHub page](https://github.com/arvkevi/kneed).

Once forked, set up your development environment:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/[YOURUSERNAME]/kneed
    cd kneed
    ```

    Optionally, add the upstream remote:

    ```bash
    git remote add upstream https://github.com/arvkevi/kneed
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -e .[testing]
    ```

At this point you're ready to get started writing code!

### Testing

Please make sure your changes pass all tests:

```bash
pytest
```

or:

```bash
pytest tests/test_sample.py
```
