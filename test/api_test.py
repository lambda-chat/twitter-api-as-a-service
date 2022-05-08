if __name__ == "__main__":
    import os
    from pprint import pprint

    import requests
    from dotenv import load_dotenv

    load_dotenv()

    endpoint = (
        # locate appropriate URL
    )
    params = {
        "screen_name": "neko_860",
        "fields": ["name", "profile_image_url_https_400x400"],
        "apikey": os.environ["LambdaApiKey"],
    }
    res = requests.get(endpoint, params=params)
    res.raise_for_status()
    pprint(res.json())
