from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, ClassVar, Literal, Optional, Union

from aws_lambda_powertools.logging import Logger
from requests_oauthlib import OAuth1Session

logger = Logger(service="twitter-api-as-a-service")


@dataclass
class UserInfo:
    __slots__ = [
        "id_",
        "id_str",
        "name",
        "screen_name",
        "location",
        "profile_location",
        "description",
        "url",
        "protected",
        "followers_count",
        "friends_count",
        "listed_count",
        "created_at",
        "favourites_count",
        "verified",
        "statuses_count",
        "status",
        "profile_background_color",
        "profile_background_image_url",
        "profile_background_image_url_https",
        "profile_background_tile",
        "profile_image_url",
        "profile_image_url_https",
        "profile_banner_url",
        "profile_link_color",
        "profile_sidebar_border_color",
        "profile_sidebar_fill_color",
        "profile_text_color",
        "profile_use_background_image",
        "has_extended_profile",
        "default_profile",
        "default_profile_image",
        "profile_image_url_https_400x400",
    ]

    id_: int
    id_str: str
    name: str
    screen_name: str
    location: Optional[str]
    profile_location: Optional[str]
    description: str
    url: Optional[str]
    protected: bool
    followers_count: int
    friends_count: int
    listed_count: int
    created_at: str
    favourites_count: int
    verified: bool
    statuses_count: int
    status: dict
    profile_background_color: str
    profile_background_image_url: str
    profile_background_image_url_https: str
    profile_background_tile: bool
    profile_image_url: str
    profile_image_url_https: str
    profile_banner_url: Optional[str]
    profile_link_color: str
    profile_sidebar_border_color: str
    profile_sidebar_fill_color: str
    profile_text_color: str
    profile_use_background_image: bool
    has_extended_profile: bool
    default_profile: bool
    default_profile_image: bool
    # additional
    profile_image_url_https_400x400: str

    def __init__(self, **kwargs) -> None:
        for field in UserInfo.__slots__:
            if field == "id_":
                setattr(self, field, kwargs["id"])
            else:
                setattr(self, field, kwargs.get(field))
        self.profile_image_url_https_400x400 = self.profile_image_url_https.replace(
            "normal", "400x400"
        )


class TwitterClient:
    session: OAuth1Session
    max_fetch_count: ClassVar[int] = 200
    base_url: ClassVar[str] = "https://api.twitter.com/1.1/"

    def __init__(self) -> None:
        self.session = OAuth1Session(
            os.environ["ApiKey"],
            os.environ["ApiSecretKey"],
            os.environ["AccessToken"],
            os.environ["AccessTokenSecret"],
        )

    def get_user_info(self, screen_name: str) -> UserInfo:
        endpoint = self.base_url + "users/show.json"
        params = {"screen_name": screen_name}
        res = self.session.get(endpoint, params=params)
        res.raise_for_status()
        return UserInfo(**json.loads(res.text))


def response(
    status_code: int,
    content_type: Optional[Literal["text/plain", "application/json"]] = None,
    body: Optional[str] = None,
) -> dict[str, Any]:
    dic: dict[str, Any] = {"statusCode": status_code}
    if content_type is not None:
        dic["headers"] = {"Content-Type": f"{content_type}; charset=utf-8"}
    if body is not None:
        dic["body"] = body
    return dic


@logger.inject_lambda_context
def handler(event, context) -> dict[str, Any]:

    query_string_parameters: dict[str, str] = event["queryStringParameters"]
    if query_string_parameters.get("apikey") != os.environ["LambdaApiKey"]:
        return response(
            401, content_type="text/plain", body="apikey is invalid."
        )  # Unauthorized

    params: dict[str, Union[str, list[str]]] = {
        k: v if "," not in v else v.split(",")
        for k, v in query_string_parameters.items()
    }
    screen_name: Optional[str] = params.get("screen_name")
    fields: list[str] = params.get("fields", [])
    if screen_name is None or not fields:
        return response(
            400, content_type="text/plain", body="screen_name or fields are invalid."
        )  # Bad Request

    logger.info(params)

    client = TwitterClient()
    user_info = client.get_user_info(screen_name)
    body = {"screen_name": screen_name} | {
        key: getattr(user_info, field)
        for field in params["fields"]
        for key in ("id" if field == "id_" else field,)
        if field in UserInfo.__slots__
    }

    res = response(
        200,
        content_type="application/json",
        body=json.dumps(body, ensure_ascii=False),
    )
    logger.info(res)
    return res
