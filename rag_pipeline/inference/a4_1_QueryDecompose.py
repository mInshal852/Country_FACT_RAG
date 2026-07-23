class QueryDecomposer:

    def __init__(self, llm):
        self.llm = llm

    def decompose(self, query: str):

        system_prompt = """
You are a query decomposition assistant.

If the user query contains multiple independent questions,
split them into separate search queries.

If the query contains only one question,
return it unchanged.

Return only one query per line.
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
