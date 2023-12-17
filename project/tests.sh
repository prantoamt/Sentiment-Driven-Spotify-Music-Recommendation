#!/bin/bash
pytest project/tests/tests_system.py -rA --disable-pytest-warnings
pytest project/tests/tests_transform.py -rA --disable-pytest-warnings


# To run the tests you need kaggle credentials to pull data from kaggle.
# To do so: 
#   1. please copy the kaggle credentials from the link (https://docs.google.com/document/d/1nTbYoqtzhuq4R3yBovNVnRnj6mMbF53qxltKSBYNfPE/edit?usp=sharing)
#   2. create kaggle.json in root directory and paste the kaggle credentials from step 1.
#   3. run chmod +x ./project/tests.sh
#   4. run ./project/tests.sh

# etl-pipeline-runner python package has been used to build the pipeline.
# The unit test cases of the pipeline components are written here: https://github.com/prantoamt/etl-pipeline-runner/tree/main/tests