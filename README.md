# Real World Cryptography for Engineers and Practitioners
This repository contains code for the beta version of the [Cry.College](https://cry.college) lecture.
As part of the lecture, students have to implement the missing chunks.

## Setup
The reference version is Python 3.10. The code is only tested for this version, but should work for any reasonably recent Python version (> 3.5).
Only one package is required as an external dependency. That is `pytest` which is required to run the (you guessed it) tests. To install pytest just run ``pip install pytest`` on your terminal.

## testing 

If you are using Linux then you can use the bash script in the [scripts](./scripts) folder to test your written code. It automates the process of running tests for the repository. The script will prompt you to enter a week number between 1-8 and displays the available classes for that week. You can then choose a week and a class by entering a corresponding number. To run the test you just go to the scripts directory and run `./run_tests.sh`. 
 
To run the script on Windows, navigate to the scripts directory in your terminal and run `.\run_tests.cmd`. The script will prompt you to enter a week number between 1 and 8. After entering a valid week number, the script will display the available classes for that week. You can then choose a class by entering its name.

In case you don't want to set an environment variable, you can configure [vscode to set the variable](https://code.visualstudio.com/docs/python/environments#_use-of-the-pythonpath-variable).

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
