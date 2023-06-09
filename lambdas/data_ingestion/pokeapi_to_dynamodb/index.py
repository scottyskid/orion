import json
import os

import awswrangler as wr
import boto3
import pandas as pd
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.typing import LambdaContext

tracer = Tracer()
logger = Logger()
s3_recource = boto3.resource("s3")


def get_category_items(category: str) -> pd.DataFrame:
    categories_obj = s3_recource.Object(
        os.environ["DATA_BUCKET"],
        f"{os.environ['DATA_KEY_BASE']}/api/v2/{category}/index.json",
    )
    response = categories_obj.get()
    categories: dict[str, object] = json.loads(response["Body"].read())

    item_df: pd.DataFrame = pd.DataFrame(categories["results"])
    item_df["category"] = category
    item_df["id"] = item_df["url"].str.split("/").str[-2]
    set_s3_uri = (
        lambda x: f"s3://{os.environ['DATA_BUCKET']}/{os.environ['DATA_KEY_BASE']}/{x}"
    )
    item_df["s3_uri"] = item_df["url"].apply(set_s3_uri)

    return item_df


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def lambda_handler(event: object, context: LambdaContext) -> None:
    categories_obj = s3_recource.Object(
        os.environ["DATA_BUCKET"],
        f"{os.environ['DATA_KEY_BASE']}/api/v2/index.json",
    )
    response = categories_obj.get()
    categories: dict[str, object] = json.loads(response["Body"].read())

    categories_df: pd.DataFrame = pd.DataFrame(
        data=categories.items(), columns=["category", "url"]
    )
    wr.dynamodb.put_df(df=categories_df, table_name=os.environ["TABLE_NAME_CATEGORY"])

    frames: list[pd.DataFrame] = []
    for category in categories.keys():
        logger.info(f"getting category data for {category=}")
        item_df = get_category_items(category=category)
        frames.append(item_df)

    items_df: pd.DataFrame = pd.concat(frames)
    wr.dynamodb.put_df(
        df=items_df,
        table_name=os.environ["TABLE_NAME_ITEMS"],
    )
