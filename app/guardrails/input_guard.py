class InputGuard:
    def check(self, message):
        if not message or not message.strip():
            return False, "Please enter a question."

        message = message.strip()

        if len(message) > 2000:
            return False, "Question is too long."

        return True, message
