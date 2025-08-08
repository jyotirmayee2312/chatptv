# train_assistant/functions/irrelevant_handler.py

def respond_to_irrelevant_query() -> str:
    """Handle queries unrelated to Melbourne train services"""
    print("Inside irrelevant function")
    return (
        "I specialize in Victoria train services only. "
        "Please ask about train schedules or disruptions."
    )