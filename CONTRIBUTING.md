## Contribute to kneed

Thank you for checking out the `kneed` repository and for your interest in contributing to the project. Please read
 below to see where `kneed` could use help.
I have tried to follow the `Kneedle` algorithm as best as I could interpret from reading [the manuscript](https://raghavan.usc.edu/papers/kneedle-simplex11.pdf), 
but the source code is far from perfect and could benefit from improvements.

- Submit a bug report or feature request on [GitHub Issues](https://github.com/arvkevi/kneed/issues).
- Contribute a Jupyter notebook to [notebooks](https://github.com/arvkevi/kneed/tree/master/notebooks).
- Documenting applications where `kneed` could be useful.
- Code refactors -- the code was refactored in `0.4.0` to be more human-readable. However I think the code could still be greatly improved
by breaking the `KneeLocator` class into a collection of methods. This would make the algorithm easier to unittest.

## Getting Started on GitHub

A typical workflow for a contributor (modified from [Yellowbrick](https://github.com/DistrictDataLabs/yellowbrick/):

1. **Discover** a bug or a feature by using the package.
2. **Discuss** the bug or feature by [adding an issue](https://github.com/arvkev/kneed/issues).
3. **Fork** the repository into your own GitHub account.
4. Create a **Pull Request** to [suggest modifications](https://github.com/arvkevi/kneed/pulls) regarding your task.
5. **Code** the feature, add a test, add your contribution.  **Make sure the tests pass**
6. **Review** the code with the repository owner.
7. **Merge** the contribution.

### Forking the Repository

The first step is to fork the repository into your own account. This will create a copy of the codebase that you can edit and write to. Do so by clicking the **"fork"** button in the upper right corner of the kneed GitHub page.

Once forked, use the following steps to get your development environment set up on your computer:

1. Clone the repository.

    After clicking the fork button, you should be redirected to the GitHub page of the repository in your user account. You can then clone a copy of the code to your local machine.

    ```
    $ git clone https://github.com/[YOURUSERNAME]/kneed
    $ cd kneed
    ```

    Optionally, you can also [add the upstream remote](https://help.github.com/articles/configuring-a-remote-for-a-fork/) to synchronize with changes made by other contributors:

    ```
    $ git remote add upstream https://github.com/arvkevi/kneed
    ```

2. Create a virtual environment.

    You can use [virtualenv](https://virtualenv.pypa.io/en/stable/) (and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/), [pyenv](https://github.com/pyenv/pyenv-virtualenv) or [conda envs](https://conda.io/docs/using/envs.html) in order to manage their Python version and dependencies. Using the virtual environment tool of your choice, create one for kneed. 
    Here's how with virtualenv:

    ```
    $ virtualenv venv
    ```

3. Install dependencies.

    Kneed's main dependencies are in the `requirements.txt` document at the root of the repository, however you will later also need to install testing dependencies.
    Install them all with `pip`:

    ```
    $ pip install -e .[testing]
    ```

At this point you're ready to get started writing code!

### Testing

Please make sure your changes pass all tests. The entire test suite can be run as follows:

```
$ pytest
```

or

```
$ pytest tests/test_sample.py
```
