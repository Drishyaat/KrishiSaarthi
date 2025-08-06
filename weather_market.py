import random

def get_mock_weather(location: str):
    weather_conditions = [
        "Sunny, low chance of rain",
        "Overcast with light rain",
        "High humidity, chance of fungal disease",
        "Dry and windy, risk of pest spread",
        "Cool night temperatures, slower crop growth"
    ]
    advice = [
        "Irrigate as usual, monitor for water stress.",
        "Reduce overhead irrigation to prevent blight.",
        "Apply preventive fungicides this week.",
        "Monitor insect traps regularly, consider natural pest control.",
        "Fence young plants against cold damage."
    ]
    idx = random.randint(0, len(weather_conditions)-1)
    return weather_conditions[idx], advice[idx]

def get_market_tip():
    tips = [
        "Market prices expected to rise this week for tomatoes.",
        "Price dip expected in cereals, consider storage.",
        "Demand for organic vegetables increasing locally.",
        "Export demand stable, focus on quality improvements.",
        "Avoid selling during festival season due to low demand."
    ]
    return random.choice(tips)
