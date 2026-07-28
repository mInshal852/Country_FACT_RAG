class QueryDecomposer:

    def __init__(self, llm):
        self.llm = llm

    def decompose(self, query: str):

        system_prompt = """
You are a query decomposition assistant.

Your tasks are:

1. Correct spelling and grammar errors.
2. Rewrite the query to improve clarity while preserving its original meaning.
3. If the query contains multiple independent questions or topics, split them into separate search queries.
4. If the query contains only one question or topic, return it as a single rewritten query.
5. Do not change the user's intent or add assumptions.

Return only the final search queries, one per line.
Do not include explanations, numbering, or additional text.
"""

        user_prompt = query

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        sub_queries = [
            q.strip("-•1234567890. ").strip() for q in response.split("\n") if q.strip()
        ]

        # this code:

        # sub_queries = [
        #     q.strip("-•1234567890. ").strip() for q in response.split("\n") if q.strip()
        # ]

        # is equivalent to

        # sub_queries = []

        # for q in response.split("\n"):
        #     if q.strip():
        #     cleaned_query = q.strip("-•1234567890. ").strip()
        #     sub_queries.append(cleaned_query)

        return sub_queries
