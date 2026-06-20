import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_notes(subject, topic):

    prompt = f"""
                You are a senior MAKAUT B.Tech professor, university paper setter, and exam-oriented notes writer.
                Generate high-quality university notes for engineering students.

                SUBJECT:
                {subject}

                TOPIC:
                {topic}

                STRICT RULES:
                * Follow the exact structure.
                * Do not add any extra sections.
                * Use simple and easy to understand English.
                * Use exam-oriented language.
                * Use short paragraphs.
                * Each bullet should be maximum 1-2 lines.
                * Highlight important keywords using **bold**.
                * Write content suitable for Semester exam preparation.
                * Ensure all sections contain meaningful content.
                * If a diagram is possible, provide a simple ASCII diagram.
                * If a diagram is not possible, write "Diagram not applicable".

                OUTPUT FORMAT:
                # {topic}

                ## Definition
                Write a concise university-exam definition.
                Include one simple example.

                ## Diagram
                Provide a clean ASCII/text diagram.

                ## Key Points
                * Point 1
                * Point 2

                ## Advantages
                * Advantage 1
                * Advantage 2
                * Advantage 3
                * Advantage 4

                ## Disadvantages
                * Disadvantage 1
                * Disadvantage 2
                * Disadvantage 3
                * Disadvantage 4

                ## Applications
                * Application 1
                * Application 2
                * Application 3
                * Application 4

                ## 5 MARKS Questions
                1. Question 1

                answer:  to question 1

                2. Question 2

                answer:  to question 2

                
                ## 15 MARKS Questions
                1. Question 1

                answer:  to question 1

                2. Question 2
                
                answer:  to question 2

                Generate complete notes now.
            """
                 
    response = model.generate_content(prompt)
    return response.text