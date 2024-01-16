> *Within this repository, you will discover a data engineering and data science project, along with exercises leveraging open data sources as an integral component of the MADE ([Methods of Advanced Data Engineering](https://oss.cs.fau.de/teaching/specific/saki/)) course. The course was conducted by the FAU Chair for Open-Source Software (OSS) during the Winter '24 semester. This repository has been forked from the [jvalue-made-template](https://github.com/jvalue/made-template) repository.*

# Sentiment-Driven Spotify Music Recommendation: Leveraging Social Media Posts and User Playlists for Personalized Music Experience 🎵😊

Welcome to the Sentiment-Driven Music Recommender GitHub repository!

### Overview
This project aims to redefine personalized music experiences by seamlessly integrating social media sentiment analysis into the realm of music curation. The approach involves training a Logistic Regression model on Twitter posts to extract sentiment, achieving a commendable 76% test accuracy. Building upon this foundation, the system identifies users' sentiments and combines them with their existing music playlists to offer truly personalized and emotionally resonant music recommendations.

### Project Goals
In the dynamic landscape of personalized music, the goals include:

- Sentiment Analysis Model: Train a Logistic Regression model to discern sentiment from social media posts, capturing the emotional nuances that influence music choices.

- User Playlist Integration: Leverage sentiment scores alongside existing playlist data to gain a holistic understanding of a user's musical inclinations. This project uses a dummy playlist instead of real user playlist.

- Recommendation Engine: Develop a sophisticated recommendation engine that dynamically adapts to users' changing emotions and preferences, ensuring personalized and responsive music suggestions.

Project report [here](/project/report.pdf), slides and video presentation can be found in this repository as well. Feel free to navigate through the report to gain a comprehensive understanding of the project's objectives, methods, results, and potential implications.

To run the project on local machine, ensure that you have the necessary libraries installed. Follow the steps outlined in the [Running the Project Locally](#running-the-project-locally) section for the installation process.

## Key project files and their functions:

- `project/pipeline.sh`: It will run an automated ETL pipeline for the project.
- `project/tests.sh` : It will run the test cases the project.
- `project/main.py` : It will run the project and ask for input.
- `project/logistic_regression_model.joblib` : Trained logistic regression model.
- `project/vectorizer.joblib` : Fitted vectorizer for the model.

## Running the Project Locally

1. Clone the repository:

```
git clone git@github.com:prantoamt/made-template.git
```

2. Create virtual environment:

```
python3 -m venv venv
```

3. Activate the virtual environment:

```
source .venv/bin/activate
``` 

4. Install requirements:

```
pip install -r requirements.txt
```

5. Run the project:

```
python ./project/main.py
```

## etl-pipeline-runner
An ETL (Extract Transform Load) pipeline has been employed a to gather the required data for this project. Throughout the project, a collaborative effort has been made to initiate an [open-source Python package](https://github.com/prantoamt/etl-pipeline-runner) for executing ETL pipelines. Take a moment to review our contributions and share your feedback. Your input is highly appreciated.

### Exercises
Throughout the semester, we were engaged in exercises that required the utilization of both Python and [Jayvee](https://github.com/jvalue/jayvee). Automated feedback for these exercises is facilitated through a GitHub action defined in .github/workflows/exercise-feedback.yml.

Here are the exercise files:
- [exercise1.py](/exercises/exercise1.py)
- [exercise2.jv](/exercises/exercise2.jv)

The exercise feedback is triggered each time we make changes to files in the exercise/ directory and push those changes to the GitHub repository. To view the feedback, access the latest GitHub Action run, and navigate to the exercise-feedback job and Exercise Feedback step.

Feel free to explore, contribute, and enjoy a personalized music journey with our Sentiment-Driven Music Recommender! 🎶