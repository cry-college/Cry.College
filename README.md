# Real World Cryptography for Engineers and Practitioners
This repository contains code for the beta version of the [Cry.College](https://cry.college) lecture.
As part of the lecture, students have to implement the missing chunks.

## Setup
The reference version is Python 3.10. The code is only tested for this version, but should work for any reasonably recent Python version (> 3.5).
Only one package is required as an external dependency. That is `pytest` which is required to run the (you guessed it) tests.

Please install pytest only via the Python package manager `pip`. In an own virtual environment this can be achieved with:

```bash
# Build the env
python -m venv crycollege_env
# Activate the env for the current shell
source crycollege_env/bin/activate
# Install pytest
pip install pytest
```

Remember that you have to activate the env (aka `source crycollege_env/bin/activate`) everytime you open a new shell.

## Code and Tasks
In order to run implementations and tasks, add the working directory to the PYTHONPATH:

```bash
# CD into the root directory of this repository
cd Cry.College
# Add dir to Python's search path
export PYTHONPATH=$(pwd)
``` 

## Test Code
After you have written code, you can test it locally using `pytest`.
To test a file, just run:

```bash
pytest CryCollege/week3/weierstrass_curve.py 
```

# License
To keep people from publishing solutions, we had to choose a restrictive license.
You can do what you want with the software on your own machine.
But if you publish solutions or a modified version, we will sue you.
No joke, we'll sue the crap out of you.

## License text
You may use the Software without charge.
You may distribute exact copies of the Software to anyone.

YOU MAY NOT PUBLISH MODIFIED, ADAPTED, TRANSLATED, OR
DERIVATIVE WORKS BASED UPON THE SOFTWARE OR ANY PART THEREOF.
