from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import httpx
import os
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from pydantic import BaseModel

# --- Pydantic models ---
class MessageRequest(BaseModel):
    message: str
    context: str = "climate_safety"  # Default context


def limit_to_18_lines(text: str) -> str:
    """Ensure chatbot response does not exceed 18 visible lines."""
    if not text:
        return ""

    lines = text.splitlines()
    if len(lines) <= 18:
        return text.strip()

    truncated = lines[:18]
    if truncated[-1].strip():
        truncated[-1] = f"{truncated[-1].rstrip()} ..."
    return "\n".join(truncated).strip()


app = FastAPI(title="INZARO Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
PORT = int(os.getenv("PORT", 3001))
BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "dist"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# --- Moroccan cities with coordinates ---
VILLES_MAROC = {
    "Rabat": {"lat": 34.0209, "lon": -6.8416},
    "Casablanca": {"lat": 33.5731, "lon": -7.5898},
    "Marrakech": {"lat": 31.6295, "lon": -8.0047},
    "Fes": {"lat": 34.0331, "lon": -5.0033},
    "Tangier": {"lat": 35.7684, "lon": -5.8038},
    "Agadir": {"lat": 30.4278, "lon": -9.5981},
    "Meknes": {"lat": 33.8869, "lon": -5.5481},
    "Oujda": {"lat": 34.6814, "lon": -1.9081},
    "Kenitra": {"lat": 34.2622, "lon": -6.5905},
    "Tetouan": {"lat": 35.5707, "lon": -5.3671},
    "Safi": {"lat": 32.2969, "lon": -8.7603},
    "El Jadida": {"lat": 33.2564, "lon": -8.5521},
    "Khouribga": {"lat": 32.8808, "lon": -6.9144},
    "Beni Mellal": {"lat": 32.3333, "lon": -6.3333},
    "Nador": {"lat": 35.1686, "lon": -2.9281},
    "Settat": {"lat": 33.0081, "lon": -7.6289},
    "Al Hoceima": {"lat": 35.2483, "lon": -3.9369},
    "Ouarzazate": {"lat": 30.9273, "lon": -6.8738},
    "Taourirt": {"lat": 34.4208, "lon": -2.7433},
    "Ksar El Kebir": {"lat": 34.8, "lon": -5.9333}
}

# --- 1. Weather API (Open-Meteo) - FREE ---
async def get_weather_data(city: str):
    """Fetch weather data from Open-Meteo API"""
    try:
        # Find city (case-insensitive)
        city_key = None
        for key in VILLES_MAROC.keys():
            if key.lower() == city.lower():
                city_key = key
                break
        
        if not city_key:
            raise ValueError(f"City not found: {city}")
        
        coords = VILLES_MAROC[city_key]
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current=temperature_2m,weather_code,wind_speed_10m,precipitation,relative_humidity_2m&timezone=auto"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()["current"]
        
        return {
            "city": city_key,
            "timestamp": datetime.now().isoformat(),
            "temperature": data["temperature_2m"],
            "windSpeed": data["wind_speed_10m"],
            "precipitation": data["precipitation"],
            "humidity": data["relative_humidity_2m"],
            "weatherCode": data["weather_code"],
            "lat": coords["lat"],
            "lon": coords["lon"]
        }
    except Exception as e:
        print(f"Weather error for {city}: {str(e)}")
        return None

# --- 2. Seismic API (USGS) - FREE ---
async def get_seismic_data(city: str):
    """Fetch seismic data from USGS API"""
    try:
        # Find city (case-insensitive)
        city_key = None
        for key in VILLES_MAROC.keys():
            if key.lower() == city.lower():
                city_key = key
                break
        
        if not city_key:
            return []
        
        coords = VILLES_MAROC[city_key]
        
        # Get earthquakes from the last 30 days
        start_date = (datetime.now() - timedelta(days=30)).date().isoformat()
        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude={coords['lat']}&longitude={coords['lon']}&maxradius=200&starttime={start_date}&mindepth=-10&maxdepth=700"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
        
        earthquakes = []
        for feature in data.get("features", []):
            coords_data = feature["geometry"]["coordinates"]
            props = feature["properties"]
            earthquakes.append({
                "magnitude": props["mag"],
                "depth": coords_data[2],
                "latitude": coords_data[1],
                "longitude": coords_data[0],
                "place": props["place"],
                "timestamp": datetime.fromtimestamp(props["time"] / 1000).isoformat(),
                "url": props["url"]
            })
        
        return earthquakes
    except Exception as e:
        print(f"Seismic error for {city}: {str(e)}")
        return []

# --- 3. API ENDPOINTS ---

@app.get("/api/cities")
async def get_cities():
    """Get list of available cities"""
    return list(VILLES_MAROC.keys())

@app.get("/api/weather/{city}")
async def get_weather(city: str):
    """Get weather data for a specific city"""
    weather = await get_weather_data(city)
    if not weather:
        raise HTTPException(status_code=404, detail=f"City not found: {city}")
    return weather

@app.get("/api/weather/all")
async def get_weather_all():
    """Get weather data for all cities"""
    tasks = [get_weather_data(city) for city in VILLES_MAROC.keys()]
    results = await asyncio.gather(*tasks)
    return [data for data in results if data is not None]

@app.get("/api/seismic/{city}")
async def get_seismic(city: str):
    """Get seismic data for a specific city"""
    earthquakes = await get_seismic_data(city)
    return {
        "city": city,
        "earthquakes": earthquakes,
        "count": len(earthquakes)
    }

@app.get("/api/city-data/{city}")
async def get_city_data(city: str):
    """Get complete data for a city (weather + seismic)"""
    weather, earthquakes = await asyncio.gather(
        get_weather_data(city),
        get_seismic_data(city)
    )
    return {
        "city": city,
        "weather": weather,
        "earthquakes": earthquakes
    }

# --- 4. AI Assistant - Groq API ---
async def get_ai_response(message: str, context: str = "climate_safety"):
    """Get AI response from Groq API"""
    try:
        print(f"[AI] Processing message: {message[:50]}...")
        # System prompt based on context
        system_prompts = {
            "climate_safety": "You are Inzaro AI, a helpful climate and disaster safety assistant based in Morocco. Provide personalized safety guidance, emergency preparedness tips, and climate risk information for Moroccan locations. Always prioritize user safety. Respond in plain text English only. Use bullet points starting with '- ' only. Do not use markdown formatting, asterisks, or dot bullets. Maximum response length: 18 lines.",
            "weather": "You are a weather expert assistant. Provide accurate weather information and recommendations for safety during different weather conditions in Morocco. Respond in plain text English only. Use bullet points starting with '- ' only. Do not use markdown formatting, asterisks, or dot bullets. Maximum response length: 18 lines.",
            "general": "You are a helpful general-purpose assistant for climate safety information in Morocco. Respond in plain text English only. Use bullet points starting with '- ' only. Do not use markdown formatting, asterisks, or dot bullets. Maximum response length: 18 lines.",
        }
        
        system_prompt = system_prompts.get(context, system_prompts["climate_safety"])

        if not GROQ_API_KEY:
            return limit_to_18_lines("AI service is not configured yet. Please set GROQ_API_KEY in server environment variables.")
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Use the current available Groq model (mixtral-8x7b-32768 was decommissioned)
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "temperature": 0.7,
            "max_tokens": 512
        }
        
        print(f"[AI] Calling Groq API...")
        async with httpx.AsyncClient() as client:
            response = await client.post(GROQ_API_URL, json=payload, headers=headers, timeout=30.0)
            print(f"[AI] Groq response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    ai_response = data["choices"][0]["message"]["content"]
                    ai_response = limit_to_18_lines(ai_response)
                    print(f"[AI] Response: {ai_response[:100]}...")
                    return ai_response
            else:
                print(f"[AI] Groq error ({response.status_code}): {response.text[:200]}")
                # Fallback response if API fails
                fallback_responses = {
                    "climate_safety": "I'm having trouble connecting to my AI backend right now. However, here are some essential safety tips during emergencies:\n\n- Listen to official alerts from weather services\n- Have an emergency kit prepared (water, first aid, light)\n- Know your evacuation routes\n- Stay informed through local news\n\nFor more personalized advice, please try again later.",
                    "weather": "I'm experiencing a temporary connection issue. General weather safety tips:\n\n- Monitor weather forecasts regularly\n- Have a weather radio or notification system\n- Prepare for extreme weather conditions\n- Update emergency plans seasonally",
                    "general": "I apologize for the technical difficulty. For climate safety in Morocco:\n\n- Register with local emergency services\n- Know the warning systems in your area\n- Establish a family emergency plan\n- Keep important documents safe"
                }
                return limit_to_18_lines(fallback_responses.get(context, "I'm temporarily unable to connect. Please try again later."))
    
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"[AI ERROR] {error_msg}")
        return limit_to_18_lines("I'm having technical difficulties right now. Please try your question again in a moment.")

@app.post("/api/chat")
async def chat(request: MessageRequest):
    """Chat endpoint using Groq API"""
    try:
        print(f"[CHAT] Received request: {request.message[:50]}...")
        print(f"[CHAT] Context: {request.context}")
        
        if not request.message or not request.message.strip():
            print("[CHAT] Message is empty")
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        print("[CHAT] Calling get_ai_response...")
        response = await get_ai_response(request.message, request.context)
        print(f"[CHAT] Response received: {response[:100]}...")
        
        return {
            "message": request.message,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"[CHAT ERROR] {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

# --- 5. Serve static files (React build) AFTER API routes ---
if DIST_DIR.exists():
    app.mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="static")
else:
    print(f"WARNING: dist directory not found at {DIST_DIR}")

# --- 6. Serve index.html for SPA routing (LAST) ---
# @app.get("/{full_path:path}")
# async def serve_spa(full_path: str):
#     """Serve index.html for SPA routing"""
#     index_file = DIST_DIR / "index.html"
#     if index_file.exists():
#         return FileResponse(index_file)
#     raise HTTPException(status_code=404, detail="Not found")

# --- Server startup ---
if __name__ == "__main__":
    import uvicorn
    
    print("\n☁️ INZARO Server running on http://localhost:3001")
    print("📊 Available APIs:")
    print("  - GET /api/cities")
    print("  - GET /api/weather/{city}")
    print("  - GET /api/weather/all")
    print("  - GET /api/seismic/{city}")
    print("  - GET /api/city-data/{city}")
    print("  - POST /api/chat (AI Assistant)")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)
