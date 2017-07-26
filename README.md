# HackGraderTests
End to end tests for https://github.com/HackSoftware/HackGrader

# Installation
* Clone this repo in a directory code/ ( alternatively, change the paths to your own directory in the script )
```
git clone git@github.com:HackSoftware/HackGraderTests.git
```
* Give permissions to script
```
chmod +x utility/setup_grader.sh
```
* Run script
```
bash setup_grader.sh
```
* Run tests
```
cd ~/code/grader_e2e/
pytest
```
