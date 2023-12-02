#!/bin/bash
pytest project/tests/tests_system.py


# To run the tests you need kaggle credentials to pull data from kaggle.
# To do so: 
#   1. please download the kaggle.json file from the link (https://docs.google.com/document/d/1nTbYoqtzhuq4R3yBovNVnRnj6mMbF53qxltKSBYNfPE/edit?usp=sharing)
#   2. put kaggle.json in root directory.
#   3. run chmod +x ./project/tests.sh
#   4. run ./project/tests.sh

# I have used etl-pipeline-runner python package to build the pipeline. The unit
# test cases of the pipeline components are written here: https://github.com/prantoamt/etl-pipeline-runner/tree/main/tests