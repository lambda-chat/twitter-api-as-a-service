# Twitter Api as a Service

Twitter API Wrapper.

## Preparing

Prepare your Twitter app. Then make `.env` file like the following:

```ts
type Environment = {
    ApiKey: string;
    ApiSecretKey: string;
    AccessToken: string;
    AccessTokenSecret: string;
    LambdaApiKey: string;
}
```

## Deploy

```sh
./deploy.sh
```

## Destroy

```sy
cdk destroy
```

## Usage (by Python)

```py
import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = (
    # locate appropriate URL (see AWS Lambda console)
)
params = {
    "screen_name": "awscloud_jp",
    "fields": ["name", "profile_image_url_https_400x400"],
    "apikey": os.environ["LambdaApiKey"],  # in .env
}
res = requests.get(endpoint, params=params)
res.raise_for_status()
pprint(res.json())

""" output
{"name": "AWS/アマゾン ウェブ サービス/クラウド"
 "profile_image_url_https_400x400", f"{icon url here}",
 "screen_name", "awscloud_jp"}
"""
```