import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet # Import SlotSet

# Define the path to the knowledge base file
KNOWLEDGE_BASE_FILE = "DiseaseData.json"

class ActionTellSymptoms(Action):
    """Provides the symptoms for a given disease and remembers the disease."""

    def name(self) -> Text:
        return "action_tell_symptoms"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 1. Try to get disease from the user's message
        disease = next(tracker.get_latest_entity_values("disease"), None)
        
        # 2. If no disease in message, try to get it from memory (slot)
        if not disease:
            disease = tracker.get_slot("disease")

        # 3. If still no disease, ask the user
        if not disease:
            dispatcher.utter_message(text="I'm sorry, I didn't catch the disease name. Could you please specify which one?")
            return []

        # Load the knowledge base
        try:
            with open(KNOWLEDGE_BASE_FILE, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text="I'm sorry, I can't seem to access my knowledge base right now.")
            return [SlotSet("disease", None)] # Clear the slot if DB is missing

        # Find the disease and its symptoms
        disease_info = None
        for d in data["diseases"]:
            if d["name"].lower() == disease.lower():
                disease_info = d
                break

        if disease_info and "symptoms" in disease_info:
            symptoms_list = "\n- ".join(disease_info["symptoms"])
            response = f"The common symptoms of {disease.capitalize()} are:\n- {symptoms_list}"
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text=f"I'm sorry, I don't have information about the symptoms of {disease}.")
            # Clear the slot if the disease is not found
            return [SlotSet("disease", None)]

        # 4. Save the disease in memory for the next turn
        return [SlotSet("disease", disease)]

class ActionTellPrevention(Action):
    """Provides prevention methods for a given disease and remembers the disease."""

    def name(self) -> Text:
        return "action_tell_prevention"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # 1. Try to get disease from the user's message
        disease = next(tracker.get_latest_entity_values("disease"), None)

        # 2. If no disease in message, try to get it from memory (slot)
        if not disease:
            disease = tracker.get_slot("disease")
            
        # 3. If still no disease, ask the user
        if not disease:
            dispatcher.utter_message(text="Could you please specify which disease you're asking about?")
            return []

        try:
            with open(KNOWLEDGE_BASE_FILE, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, I'm unable to access my health database at the moment.")
            return [SlotSet("disease", None)]

        disease_info = None
        for d in data["diseases"]:
            if d["name"].lower() == disease.lower():
                disease_info = d
                break

        if disease_info and "prevention" in disease_info:
            prevention_list = "\n- ".join(disease_info["prevention"])
            response = f"To prevent {disease.capitalize()}, you should:\n- {prevention_list}"
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text=f"I'm sorry, I don't have prevention information for {disease}.")
            return [SlotSet("disease", None)]
        
        # 4. Save the disease in memory for the next turn
        return [SlotSet("disease", disease)]

class ActionTellVaccineInfo(Action):
    """Provides the schedule for a given vaccine."""

    def name(self) -> Text:
        return "action_tell_vaccine_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        vaccine = next(tracker.get_latest_entity_values("vaccine"), None)

        if not vaccine:
            dispatcher.utter_message(text="Which vaccine are you interested in?")
            return []

        try:
            with open(KNOWLEDGE_BASE_FILE, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text="Sorry, my vaccination schedule data is currently unavailable.")
            return []

        vaccine_info = None
        for v in data["vaccinations"]:
            if v["name"].lower() == vaccine.lower():
                vaccine_info = v
                break

        if vaccine_info:
            response = (
                f"The {vaccine.upper()} vaccine protects against {vaccine_info['protects_against']}. "
                f"The recommended schedule is: {vaccine_info['schedule']}."
            )
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text=f"I don't have information on the {vaccine} vaccine.")

        return []

