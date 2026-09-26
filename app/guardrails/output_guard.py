class OutputGuard:
    def check(self, response):
        if not response or not response.strip():
            return False, "No response was generated."

        response = response.strip()

        if len(response) > 12000:
            response = response[:12000]

        return True, response
