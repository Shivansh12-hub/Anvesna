from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from misingval import modelPred, health_risk
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
llm = ChatGroq(model="llama-3.1-8b-instant", api_key=GROQ_API_KEY)



pregnancy_prompt = PromptTemplate(
    template="""
You are a Pregnancy Health Expert. You are NOT explaining medical basics. 
You are ONLY analyzing the woman's health data and risk profile, and providing **actionable, professional, data-driven insights**.

Patient Data:

{sample_data}

Predicted Risk Status (from clinical model):

{risk_status}

Instructions:

1. Provide a **summary of key metrics** using only available input data. For missing fields, leave as null. Include:
   - age
   - bmi (pre_pregnancy_bmi)
   - blood_pressure (systolic/diastolic)
   - hemoglobin_level
   - gestational_age_weeks
   - number_of_prenatal_visits
2. Add an overall risk probability as `"riskinpercent"` (0-100) based on risk_status and patient data.
3. Identify **potential health risks** based on the data and risk status.
4. For each risk, provide a **short recommendation** (few words) to mitigate it.
5. **Output ONLY in JSON format** as follows:

{{
  "summary": {{
      "age": <int or null>,
      "bmi": <float or null>,
      "blood_pressure": "<systolic>/<diastolic> or null",
      "hemoglobin": <float or null>,
      "gestational_age_weeks": <int or null>,
      "prenatal_visits": <int or null>,
      "riskinpercent": <float 0-100>
  }},
  "risks": [
      {{"risk": "<risk name>", "recommendation": "<short recommendation>"}},
      {{"risk": "<risk name>", "recommendation": "<short recommendation>"}}
  ]
}}

- Keep the risk and recommendation lists concise, few words per item.
- Make the summary impactful, so it is **visually impressive** at a glance.
- Do not include any extra explanation, only return the JSON.

User Question/Request:
{question}

Answer:
""",
    input_variables=["sample_data", "risk_status", "question"]
)



def pregnancyHealthChat(sample_data, risk_status, question):
    prompt_text = pregnancy_prompt.format(
        sample_data=sample_data,
        risk_status=risk_status,
        question=question
    )
    messages = [HumanMessage(content=prompt_text)]
    response = llm.invoke(messages)
    return response.content


if __name__ == "__main__":
    sample_data = {
        "age": 28,
        "pre_pregnancy_bmi": None,
        "gestational_age_weeks": 20,
        "blood_pressure_systolic": 118,
        "blood_pressure_diastolic": 76,
        "hemoglobin_level": 12.8,
        "number_of_prenatal_visits": 5,
        "has_diabetes": 0,
        "has_hypertension": 0,
        "smoking_status": 0,
        "alcohol_consumption": 0
    }

    sample_data = modelPred(sample_data)  
    sample_risk = [25, 130, 80, 15.0, 98.0, 86]
    risk_status = health_risk(sample_risk=sample_risk)

    print("Welcome to the Pregnancy Health Chatbot!")

    while True:
        user_question = input("\nEnter your question about the patient's health (or 'exit' to quit): ")
        if user_question.lower() == "exit":
            break
        answer = pregnancyHealthChat(sample_data, risk_status, user_question)
        print("\nPregnancy Health Report:\n", answer)
