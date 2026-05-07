from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200}]
)

class ContentSearchAPIView(APIView):

    def get(self, request):

        query = request.GET.get("q", "")

        response = client.search(
            index="ramagallery_contents",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "TITLE^5",
                            "DESCRIPTION",
                            "TAGS^3"
                        ],
                        "fuzziness": "AUTO"
                    }
                }
            }
        )

        return Response(response["hits"]["hits"])