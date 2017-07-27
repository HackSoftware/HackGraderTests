# HackGraderTests
End to end tests for https://github.com/HackSoftware/HackGrader

# Requirements
* Postgresql installed and setup
* Python virtualenv installed

# Installation
* Clone this repo in a directory code/ ( alternatively, change the paths to your own directory in the script )
```
git clone git@github.com:HackSoftware/HackGraderTests.git
```
* Give permissions to script ( from root directory )
```
chmod +x utility/setup_grader.sh
```
* Run script ( from root directory )
```
bash utility/setup_grader.sh
```

#  Run tests
* Make a virtualenv for this project and install requirements
```
cd ~/code/grader_e2e/
pytest
```
