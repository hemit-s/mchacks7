## Inspiration
One of our team members has volunteered at a distress centre for several years, and has experienced the large volumes of calls these centres received firsthand. This was the inspiration for LifeLine. We wanted a way for those who need immediate support to be able to receive it immediately, without needing to wait for a volunteer.

## What it does
Currently, LifeLine follows specific protocols that distress centre volunteers are trained to follow. Specific questions are asked by the bot to determine if the user is in serious distress and needs immediate assistance from the authority. It asks follow up questions based on the responses to the questions to determine their state of mind and provides assistive advice.

We are also using IBM Watson's Natural Language Processing system to determine the levels of specific emotions in the user's responses (sadness, fear, anger, disgust). In addition to the base functionality, we also ask demographic based questions (the users identity is never stored and all information is anonymous). Both the outputs from IBM Watson's emotion level measures and the responses to the demographic questions, we are also estimating a risk factor associated with certain factors based on a trained machine learning model.

## How we built it
We used Voiceflow to implement the voice and text based chat functionality, and record the responses to export to a Google Sheet. From there, a Python script is used to import the data, process the responses using IBM Watson, and estimate the risk factor using a scikit-learn based machine learning model.

## Challenges we ran into
We originally tried to use DialogFlow (which interfaces directly with the Google Assistant and Google Cloud API), but it proved to be much too complex for the prototype we were trying to implement.

After choosing Voiceflow, we weren't able to interface well with FireBase or MongoDB, so we ended up going with the pre-existing functionality in Voiceflow to export responses to a Google Sheets spreadsheet.

## What's next for LifeLine
Further extending the functionality of the voice assistant to be able to process more complex responses and provide responses more tailored to the specific user. Using the output from the python script, and especially through IBM Watson, we wanted to send this data back to our Voiceflow app so that it can use the emotion levels detected by IBM Watson to tailor the conversation and respond accordingly to the individual in need.

We were hoping to collect the outputs from our python script and potentially pass them on to a volunteer at working at a distress centre or hotline with specific information about the caller that LifeLine had gathered. This would save the volunteer time and allow them to assist the individual in need more quickly. The risk factor we predict would useful to the volunteer as well in assessing the overall situation of the individual on the other end of the phone.
