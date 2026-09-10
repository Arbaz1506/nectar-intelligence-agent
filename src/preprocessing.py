import pandas as pd


def load_spotify_data(file_path: str, chunksize: int = 100_000) -> pd.DataFrame:
    """
    Load SpotifyCares-related tweets from the Twitter customer-support dataset.
    """

    spotify_chunks = []

    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        spotify_rows = chunk[
            (chunk["author_id"] == "SpotifyCares")
            |
            (
                (chunk["inbound"] == True)
                & chunk["text"].str.contains(
                    "@SpotifyCares",
                    case=False,
                    na=False
                )
            )
        ]

        spotify_chunks.append(spotify_rows)

    return pd.concat(spotify_chunks, ignore_index=True)
