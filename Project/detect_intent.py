from google.cloud import dialogflow
import os

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_service_key2.json"

# Define your project ID
# project_id = "probable-summer-395414"
# session_id = '11111'
# text=["yeah, sorry"]

def detect_intent_texts(texts):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    project_id = "probable-summer-395414"
    session_id = '11111'
    language_code ='en-US'
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    response_obj = {
        'intent':'',
        'location':'',
        'direction':[],
        'degree':''
    }

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )

        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
        if response.query_result.parameters:
            print("Detected Entities:")
            for entity_name, entity_value in response.query_result.parameters.items():
                print("{}: {}".format(entity_name, entity_value))
                response_obj[entity_name] = entity_value
        
        response_obj["intent"]= response.query_result.intent.display_name

        print("\n")

    # return(response.query_result.intent.display_name)
    # print("Response Object:", response_obj)
    return(response_obj)
