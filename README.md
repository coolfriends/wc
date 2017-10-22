# wc
A simple Flask REST API to obtain a word count and most common used word.

## Setup
* Tested with Python 3.6
* Tested with Node 8.7.0
* Tested with npm 5.4.2

### Install Python requirements
Make sure to set up a Python 3.6 virtual environment before moving forward.
```bash
pip install -r requirements.txt
```

### Install serverless
This project is managed with serverless framework. While you could serve this
without it, serverless framework makes deploying to AWS a breeze.
```bash
npm install -g serverless
npm install
```

### AWS Credentials
You need to have aws credentials set up with an account with significant IAM
privelages to deploy.

http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
https://serverless.com/framework/docs/providers/aws/guide/iam/

### Environment variables
The `WC_SECRET_KEY` environment variable is the only method of authentication.
Keep it safe.
```bash
export WC_SECRET_KEY=your-secure-key
```


## Tests
### Run the tests
```bash
python -m unittest
```

## Start
Deploy to AWS
```bash
sls deploy
```

Make a note of the endpoint address, which should look like this:
"https://somethings.execute-api.us-west-2.amazonaws.com/dev/"

Test it out using the Python requests library
```python
import os
import requests
import json

secret_key = os.environ['WC_SECRET_KEY']
# Replace this url with your url, with the route wc appended as shown
url = "https://somerestapiiguess.execute-api.us-west-2.amazonaws.com/dev/wc"
response = requests.post(url, data={
    'text': 'Your lovely block of text.',
    'wc_secret_key': secret_key
})
print(response.text)
```





