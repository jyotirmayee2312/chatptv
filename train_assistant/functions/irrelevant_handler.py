# train_assistant/functions/irrelevant_handler.py

def respond_to_irrelevant_query() -> str:
    """
    Returns a fixed response for irrelevant queries.
    """
    return (
        "I specialize in Melbourne train services only. "
        "Please ask about train schedules or disruptions."
    )
