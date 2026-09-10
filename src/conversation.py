import pandas as pd


def get_conversation(tweet_id: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Reconstruct the conversation leading up to a given tweet.

    Follows the in_response_to_tweet_id chain backwards and
    returns messages in chronological order.
    """

    tweet_map = df.set_index("tweet_id").to_dict("index")

    conversation = []
    current_id = int(tweet_id)

    while current_id in tweet_map:
        tweet = tweet_map[current_id].copy()
        tweet["tweet_id"] = current_id

        conversation.append(tweet)

        parent_id = tweet.get("in_response_to_tweet_id")

        if pd.isna(parent_id) or parent_id is None:
            break

        current_id = int(float(parent_id))

    conversation.reverse()

    return pd.DataFrame(conversation)
