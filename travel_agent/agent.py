"""
Travel Agent with Custom Function Tools
Demonstrates multiple custom tools working together
"""

"""
Best practices for custom tools:
1. The funciton name should be human-readable & must describe what it does in some capacity
    search_flights - good name, understandable
    search - bad name, search what? too ambiguous
2. Use type hights for all parameters & return types
    LLM uses this to figure what type to pass as input & how to read output
3. Parameter names should be meaningful
4. Parameters should not have default values. LLMs tend to ignore default values
5. Parameters should not have complex types
    Simple, JSON-serializable types need to be used - str, int, float, bool, list, dict
    Complex & custom types (JSON non-serializable) should be avoided - datetime, custom classes, objects, file handlers
6. Doc strings are critical & must have:
    Summary of the tools
    Additional context if any (when to use it)
    Args (description of arguments)
    Returns (describe what return results to expect)
7. Try to have a dict as return type with status as a parameter so LLM can decide what to do in case of success/failure
8. Return format should be consistent
    One return shouldn't give status as success & another as OK even if they belong to different functions
9. Use strategic instructions in the agent if it has to orchestrate multiple tool uses
    Make sure it has:
        Tool usage guidelines
        Tool selection (When to use which tool)
        Workflows (step-by-step procedures)
        Error handling (what to do for each error type)
        Escalation (when & how to escalate)
"""

from google.adk.agents import LlmAgent

# Tool 1: Search flights
def search_flights(destination: str, departure_date: str)->dict:
    """
    Searches for available flights to a destination on a specific date

    Use this tool when a customer wants to know about flight options

    Args:
        destination (str): The destination city (e.g.: "Paris", "Tokyo")
        departure_date (str): Departure date in YYYY-MM-DD format

    Returns:
        dict: Flight search results
        On success: {'status': 'success', 'flights': [...], 'count': N}
        On error: {'status': 'error', 'error_message': 'explanation'}
    """

    # Simulated flight data
    available_flights = {
        'paris': [
            {
                'flight_number': "AF123",
                'price_usd': 450,
                'duration_hours': 8
            },
            {
                'flight_number': "BA456",
                'price_usd': 480,
                'duration_hours': 7
            }
        ],
        'delhi': [
            {
                'flight_number': "XY123",
                'price_usd': 250,
                'duration_hours': 8
            },
            {
                'flight_number': "YZ456",
                'price_usd': 280,
                'duration_hours': 7
            }
        ]
    }

    dest_key = destination.lower()
    if dest_key not in available_flights:
        return {
            'status': 'error',
            'error_message': f'No flights found to {destination}. Try Paris or Delhi'
        }
    
    return {
        'status': 'success',
        'destination': destination,
        'departure_date': departure_date,
        'flights': available_flights[dest_key],
        'count': len(available_flights[dest_key])
    }

# Tool 2: Search hotels
def search_hotels(city: str, check_in_date: str)->dict:
    """
    Searches for available hotels in a city for a specific check-in-date

    Use this tool when a customer needs accommodation.

    Args:
        city (str): The city name (e.g.: "Paris", "Tokyo")
        check-in-date (str): Check-in date in YYYY-MM-DD format

    Returns:
        dict: Hotel search results
            On success: {'status': 'success', 'hotels': [...], 'count': N}
            On error: {'status': 'error', 'error_message': 'explanation'}
    """
    # Simulated hotel data
    available_hotels = {
        'paris': [
            {'name': 'Hotel Eiffel', 'price_per_night_usd': 150, 'rating': 4.5},
            {'name': 'Louvre Inn', 'price_per_night_usd': 120, 'rating': 4.2}
        ],
        'tokyo': [
            {'name': 'Hotel Tokyo', 'price_per_night_usd': 50, 'rating': 4.5},
            {'name': 'Shibuya Inn', 'price_per_night_usd': 20, 'rating': 4.2}
        ]
    }

    city_key = city.lower()
    if city_key not in available_hotels:
        return {
            'status': 'error',
            'error_message': f'No hotels found in {city}. Try Paris or Tokyo'
        }
    
    return {
        'status': 'success',
        'city': city,
        'check_in_date': check_in_date,
        'hotels': available_hotels[city_key],
        'count': len(available_hotels[city_key])
    }

# Tool 3: Calculate trip budget
def calculate_trip_budget(flight_price: float, hotel_price: float, num_nights: int)->dict:
    """
    Calculates total trip budget including flights & accommodation

    Use this after finding flight & hotel prices to give the customer a total estimate

    Args:
        flight_prce (float): Round-trip flight cost in USD
        hotel_price (float): Hotel cost per night in USD
        num_nights (int): Number of nights staying

    Returns:
        dict: Budget breakdown
        Always returns: {'status': 'success', 'total_usd': X, 'breakdown': {...}}
    """
    hotel_total=hotel_price * num_nights
    total = flight_price + hotel_total

    return {
        'status': 'success',
        'total_usd': round(total, 2),
        'breakdown': {
            'flight_cost': flight_price,
            'hotel_cost_per_night': hotel_price,
            'num_nights': num_nights,
            'hotel_total': round(hotel_total, 2)
        }
    }

# Create travel agent with all 3 tools
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='travel_agent',
    description='Helps users plan trips by finding flights & hotels',
    instruction="""
    You are a helpful travel agent assistant

    Your capabilties:
    - Search for flights using search_flights (desitnation, departure_date)
    - Search for hotels using search_hotels (city, check_in_date)
    - Calculate trip budgets using calculate_trip_budget (flight_price, hotel_price, num_nights)

    When helping users:
    1. If they ask about flights, use search_flights
    2. If they ask about hotels, use search_hotels
    3. If they want a full trip estimate, use both search tools, then calculate_trip_budget
    4. Always present options clearly with prices
    5. If a tools returns an error, apologize & suggest available destinations

    Be friendly & help users plan their perfect trip!
    """,
    tools=[search_flights, search_hotels, calculate_trip_budget]
)
