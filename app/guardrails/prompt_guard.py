class PromptGuard:
    def check(self, message):
        blocked_patterns = [
            "ignore previous instructions",
            "ignore all previous instructions",
            "ignore your instructions",
            "forget your instructions",
            "disregard previous instructions",
            "disregard all previous instructions",
            "show me your system prompt",
            "show your system prompt",
            "reveal your instructions",
            "reveal the system prompt",
            "bypass your rules",
            "bypass the rules",
            "jailbreak"
        ]

        message_lower = message.lower()

        for pattern in blocked_patterns:
            if pattern in message_lower:
                return False, "This request cannot be processed."

        return True, message
