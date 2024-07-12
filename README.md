# Mesop Jeopardy

Simple jeopardy game built using [Mesop](https://google.github.io/mesop/). User answers are
checked using the Gemini API.

In order to run the app, you will need a Google API Key for Gemini Pro. You can create
one using the instructions at https://ai.google.dev/gemini-api/docs/api-key.

```
git clone git@github.com:richard-to/mesop-jeopardy.git
cd mesop-jeopardy
pip install -r requirements.txt
GOOGLE_API_KEY=<your-api-key> mesop main.py
```

## Notes on the Jeopardy questions dataset

One thing to note is I haven't included the jeopardy.json file. I'm using an old dataset
of 200K questions that's about 10 years old now. You can find it with a quick Google
search.

The file needs to be added to the data folder and named jeopardy.json. The format is
like this

```
{
  "category": "HISTORY",
  "air_date": "2004-12-31",
  "question": "'For the last 8 years of his life, Galileo was...",
  "value": "$200",
  "answer": "Copernicus",
  "round": "Jeopardy!",
  "show_number": "4680"
}
```

If you do not want to use the existing Jeopardy data set, you can set the environment
variable `GENERATE_JEOPARDY_QUESTIONS=True` to generate the questions from Gemini.

## Deployment

This repository also contains configuration to deploy to GCP App Engine, GCP Cloud Run,
or using Docker.

The instructions below assume you have a `jeopardy.json` file in the data folder and
that you have a Google API Key to make Gemini API calls.

### Docker

This section shows how to run Mesop Jeopardy from a Docker image.

#### Step 0 - Install Docker

Make sure [Docker and Docker Compose are installed](https://docs.docker.com/engine/install/).

#### Step 2 - Add Google API key

In the `docker-compose.yml` set the Google API Key.

```
environment:
  - GOOGLE_API_KEY=YOUR-API-KEY-HERE
```

#### Step 3 - Run Docker image

Run this command in the repository working directory:

```
docker-compose up -d
```

#### Step 4 - View the app

The app should now be viewable at localhost:8080.

### App Engine

This section describes how to deploy Mesop Jeopardy with App Engine Flexible.

#### Step 0 - GCP setup

This section assumes that you have a properly configured Google Cloud Platform (GCP)
account (e.g. GCP project to use, Billing enabled, Google Cloud CLI installed).

See the instructions here:
https://cloud.google.com/appengine/docs/flexible/python/create-app#before-you-begin

#### Step 1 - Enable App Engine

```
gcloud app create --project=[YOUR_PROJECT_ID]
gcloud components install app-engine-python
```

#### Step 2 - Add Google API key

Set your Google API key in `app.yaml`.

```
env_variables:
  GOOGLE_API_KEY: YOUR-API-KEY
```

#### Step 3 - Deploy

Run this command in the repository working directory.

```
gcloud app deploy
```

#### Step 4 - View the app

```
gcloud app browse
```

### Cloud Run

This section describes how to deploy Mesop Jeopardy with Cloud Run.

#### Step 0 - GCP setup

This section assumes that you have a properly configured Google Cloud Platform (GCP)
account (e.g. GCP project to use, Billing enabled, Google Cloud CLI installed).

See the instructions here:
https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service#before-you-begin

#### Step 1 - Deploy

Run this command in the repository working directory.

```
gcloud run deploy mesop-jeopardy \
  --source . \
  --set-env-vars GOOGLE_API_KEY=API_KEY \
  --region us-east4
```

#### Step 2 - View app

When the deploy command is done, you should see a URL to the Cloud Run app.

## Screenshots

Here are some screenshots of the UI.

### Jeopardy board

<img width="1312" alt="Jeopardy" src="https://github.com/richard-to/mesop-jeopardy/assets/539889/bc27447d-129f-47ae-b0b1-8f5c546762ed">

### Jeopardy answer

<img width="1312" alt="Jeopardy Answer Modal" src="https://github.com/richard-to/mesop-jeopardy/assets/539889/46bbe312-8cf3-4ff7-8271-49692bd75dec">
