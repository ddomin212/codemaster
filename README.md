## Streamlit app for helping you write better code
This app combines multiple features
1. Visualize the dependencies of your codebase, along with metrics
2. Get detailed information, such as the number of functions, classes, or the maximum indentation level
3. Get a pylint score for your code, along with the errors and warnings.
4. Get a rating on your code from a chatbot, mutiple chatbots are available. We use [Poe.com's](https://poe.com/) API to get the chatbot responses.
All in a friendly web interface.
---
## How to run
You can find your `POE_API_KEY` [as follows](https://github.com/snowby666/poe-api-wrapper#how-to-get-your-token), the daily limit is about 10 requests, so it's more for prototype purposes.

### Local
1. Clone the repo
2. Add the `POE_API_KEY` to the `.env` file
3. Install the requirements
4. Run the app `streamlit run Codemaster_alt.py`

### Docker
1. Clone the repo
2. Add `ENV POE_API_KEY your_api_key` to the `Dockerfile`
3. Build the docker image `docker build -t codemaster .`
4. Run the docker image `docker run -p 8501:8501 codemaster`

---

### TODO: 
    Chatbot interface for back-forth conversation with codemaster
    Optimize chatbots -> use one conversation for all messages, maybe softer token limit.
    Actual website