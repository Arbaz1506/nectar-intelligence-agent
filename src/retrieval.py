import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class HistoricalRetriever:
    def __init__(self, cases_path: str):
        self.cases = pd.read_csv(cases_path)

        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=2,
        )

        self.matrix = self.vectorizer.fit_transform(
            self.cases["customer_message"].fillna("")
        )

    def search(
        self,
        query: str,
        top_k: int = 5,
        min_similarity: float = 0.2,
    ) -> pd.DataFrame:

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.matrix,
        ).flatten()

        valid_indices = [
            i for i, score in enumerate(scores)
            if score >= min_similarity
        ]

        if not valid_indices:
            return pd.DataFrame(
                columns=[
                    *self.cases.columns,
                    "similarity",
                ]
            )

        top_indices = sorted(
            valid_indices,
            key=lambda i: scores[i],
            reverse=True,
        )[:top_k]

        results = self.cases.iloc[top_indices].copy()
        results["similarity"] = scores[top_indices]

        return results.reset_index(drop=True)

    def has_evidence(
        self,
        query: str,
        min_similarity: float = 0.6,
    ) -> bool:

        results = self.search(
            query,
            top_k=1,
            min_similarity=min_similarity,
        )

        return not results.empty
