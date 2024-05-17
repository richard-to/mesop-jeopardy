# Mesop Jeopardy

Simple jeopardy game built using [Mesop](https://google.github.io/mesop/). User answers are 
checked using the Gemini API.

In order to run the app, you will need a Google API Key for Gemini Pro. You can create
one using the instructions at https://ai.google.dev/gemini-api/docs/api-key.

```
git clone git@github.com:richard-to/mesop-jeopardy.git
cd mesop-jeopardy
pip install -r requirements.txt
GOOGLE_API_KEY=<your-api-key> mesop app.py
```

## Notes on the Jeopardy questions dataset

One thing to note is I haven't included the jeopardy.json file. I'm using an old dataset
of 200K questions that's about 10 years old now. You can find it with a quick Google
search.

The file needs to be added to the data folder and named jeopardy.json. The format is
like this. So you can also ask Gemini/ChatGPT/etc to generate some questions in this
format as well.

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

## Screenshots

Here are some screenshots of the UI.

### Jeopardy board

<img width="1312" alt="Jeopardy" src="https://github.com/richard-to/mesop-jeopardy/assets/539889/bc27447d-129f-47ae-b0b1-8f5c546762ed">

### Jeopardy answer

<img width="1312" alt="Jeopardy Answer Modal" src="https://github.com/richard-to/mesop-jeopardy/assets/539889/46bbe312-8cf3-4ff7-8271-49692bd75dec">

