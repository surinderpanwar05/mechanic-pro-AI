class SafetyGuard:
    def check(self, message):
        high_voltage_terms = [
            "high voltage",
            "high-voltage",
            "hv battery",
            "hybrid battery",
            "ev battery",
            "traction battery",
            "battery pack",
            "inverter",
            "dc-dc converter",
            "on-board charger",
            "high voltage cable",
            "orange cable"
        ]

        message_lower = message.lower()

        for term in high_voltage_terms:
            if term in message_lower:
                return True, "HIGH_VOLTAGE"

        return True, "NORMAL"
