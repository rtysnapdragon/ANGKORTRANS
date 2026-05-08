def build_context(documents):

    context = ""

    for doc in documents:

        context += f"""

        TITLE:
        {doc.title}

        CONTENT:
        {doc.content}

        """

    return context