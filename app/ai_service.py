from app.providers.factory import get_provider

from app.guardrails.input_guard import InputGuard
from app.guardrails.prompt_guard import PromptGuard
from app.guardrails.automotive_guard import AutomotiveGuard
from app.guardrails.safety_guard import SafetyGuard
from app.guardrails.output_guard import OutputGuard

from app.knowledge.service import KnowledgeService


class AIService:

    def __init__(self):

        self.provider = get_provider()

        self.input_guard = InputGuard()
        self.prompt_guard = PromptGuard()
        self.automotive_guard = AutomotiveGuard()
        self.safety_guard = SafetyGuard()
        self.output_guard = OutputGuard()

        self.knowledge = KnowledgeService()


    def ask(self, message):

        # -----------------------------
        # Input guard
        # -----------------------------

        allowed, result = self.input_guard.check(message)

        if not allowed:
            return result


        # -----------------------------
        # Automotive guard
        # -----------------------------

        if not self.automotive_guard.check(result):

            return (
                "This question is outside the "
                "Mechanic Pro automotive scope."
            )


        # -----------------------------
        # Prompt injection guard
        # -----------------------------

        allowed, prompt_result = self.prompt_guard.check(result)

        if not allowed:
            return prompt_result

        result = prompt_result


        # -----------------------------
        # Safety guard
        # -----------------------------

        safety_level = self.safety_guard.check(result)


        # -----------------------------
        # Knowledge base
        # -----------------------------

        knowledge = self.knowledge.search(result)


        # -----------------------------
        # AI provider
        # -----------------------------

        response = self.provider.chat(
            self.build_prompt(
                result,
                safety_level,
                knowledge
            )
        )


        # -----------------------------
        # Output guard
        # -----------------------------

        allowed, response = self.output_guard.check(response)

        if not allowed:
            return response


        return response


    def build_prompt(
        self,
        message,
        safety_level,
        knowledge=""
    ):

        knowledge_section = ""

        if knowledge:

            knowledge_section = f"""
Relevant Mechanic Pro knowledge base:

{knowledge}

Use the knowledge above when it is relevant to the user's question.

Do not invent vehicle-specific specifications, service intervals,
torque values, fluid specifications or repair procedures that are
not supported by the knowledge provided.

If the knowledge base does not contain the required information,
say that the information is not available in the current knowledge
base rather than pretending that it is confirmed.
"""


        if safety_level[1] == "HIGH_VOLTAGE":

            return f"""
You are Mechanic Pro, a professional automotive assistant.

The question involves a hybrid or electric vehicle high-voltage system.

Provide useful diagnostic and repair information while prioritizing safety.

Do not instruct a person to work on an energized high-voltage system.

When relevant, mention:

- High-voltage isolation procedures
- Manufacturer service procedures
- Appropriate PPE
- Required training or qualifications
- Verification that the system is safely isolated before physical work

Do not assume a vehicle is safe to work on simply because it is switched off.

{knowledge_section}

User question:

{message}
"""


        return f"""
You are Mechanic Pro, a professional automotive assistant.

Provide clear, practical automotive information.

Use the provided knowledge base when it is relevant.

Do not invent vehicle-specific specifications, service intervals,
torque values, fluid specifications or repair procedures.

If the available knowledge does not confirm something, clearly say
that the information needs to be verified against the applicable
manufacturer service information.

{knowledge_section}

User question:

{message}
"""
