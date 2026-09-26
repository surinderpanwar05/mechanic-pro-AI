from pathlib import Path


class KnowledgeService:

    def __init__(self):
        self.documents_path = Path(
            "/var/www/mechanic-ai/app/knowledge/documents"
        )

    def search(self, question: str) -> str:

        if not self.documents_path.exists():
            return ""

        question_words = set(
            question.lower().split()
        )

        results = []

        for file in self.documents_path.glob("*.md"):

            try:
                content = file.read_text(
                    encoding="utf-8"
                )
            except Exception:
                continue

            content_words = set(
                content.lower().split()
            )

            matches = question_words.intersection(
                content_words
            )

            if matches:
                results.append(content)

        if not results:
            return ""

        return "\n\n".join(results)
