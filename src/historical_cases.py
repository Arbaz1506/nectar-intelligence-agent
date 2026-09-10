import pandas as pd


def build_spotify_cases(
    file_path: str,
    chunksize: int = 100_000,
) -> pd.DataFrame:

    required_columns = [
        "tweet_id",
        "author_id",
        "inbound",
        "created_at",
        "text",
        "in_response_to_tweet_id",
    ]

    support_replies = []

    for chunk in pd.read_csv(
        file_path,
        usecols=required_columns,
        chunksize=chunksize,
    ):
        spotify = chunk[
            chunk["author_id"] == "SpotifyCares"
        ].copy()

        spotify = spotify[
            spotify["in_response_to_tweet_id"].notna()
        ]

        if not spotify.empty:
            support_replies.append(
                spotify[
                    [
                        "tweet_id",
                        "created_at",
                        "text",
                        "in_response_to_tweet_id",
                    ]
                ]
            )

    support_df = pd.concat(
        support_replies,
        ignore_index=True,
    )

    parent_ids = set(
        support_df["in_response_to_tweet_id"]
        .astype(float)
        .astype(int)
        .tolist()
    )

    customer_rows = []

    for chunk in pd.read_csv(
        file_path,
        usecols=required_columns,
        chunksize=chunksize,
    ):
        chunk_ids = pd.to_numeric(
            chunk["tweet_id"],
            errors="coerce",
        )

        matched = chunk[
            chunk_ids.isin(parent_ids)
        ].copy()

        if not matched.empty:
            customer_rows.append(matched)

    customers_df = pd.concat(
        customer_rows,
        ignore_index=True,
    )

    customers_df["tweet_id"] = pd.to_numeric(
        customers_df["tweet_id"],
        errors="coerce",
    ).astype("Int64")

    support_df["in_response_to_tweet_id"] = pd.to_numeric(
        support_df["in_response_to_tweet_id"],
        errors="coerce",
    ).astype("Int64")

    cases = customers_df.merge(
        support_df,
        left_on="tweet_id",
        right_on="in_response_to_tweet_id",
        suffixes=("_customer", "_support"),
    )

    cases = cases[
        [
            "tweet_id_customer",
            "text_customer",
            "created_at_customer",
            "tweet_id_support",
            "text_support",
            "created_at_support",
        ]
    ].copy()

    cases.columns = [
        "customer_tweet_id",
        "customer_message",
        "customer_created_at",
        "support_tweet_id",
        "historical_reply",
        "support_created_at",
    ]

    return cases
