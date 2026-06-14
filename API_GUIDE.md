# Inzaro - Weather API Integration Guide

## 🌐 Available APIs

The backend provides free weather and seismic data for all Moroccan cities using:
- **Open-Meteo API** (Free - No API Key Required)
- **USGS Earthquake API** (Free - Real-time seismic data)

## 📡 API Endpoints

### 1. **Get Weather for a Specific City**
```bash
GET /api/weather/{city}
```
**Example:**
```bash
curl http://localhost:3001/api/weather/Casablanca
```
**Response:**
```json
{
  "city": "Casablanca",
  "timestamp": "2024-04-11T15:30:00Z",
  "temperature": 22.5,
  "windSpeed": 15.3,
  "precipitation": 0,
  "humidity": 65,
  "weatherCode": 0,
  "lat": 33.5731,
  "lon": -7.5898
}
```

### 2. **Get Weather for All Cities**
```bash
GET /api/weather/all
```
Returns array of weather data for all 20 Moroccan cities.

### 3. **Get Seismic Data for a City**
```bash
GET /api/seismic/{city}
```
**Example:**
```bash
curl http://localhost:3001/api/seismic/Marrakech
```
**Response:**
```json
{
  "city": "Marrakech",
  "earthquakes": [
    {
      "magnitude": 3.2,
      "depth": 12.5,
      "latitude": 31.6295,
      "longitude": -8.0047,
      "place": "Morocco",
      "timestamp": "2024-04-05T14:30:00Z"
    }
  ],
  "count": 1
}
```

### 4. **Get Complete City Data (Weather + Seismic)**
```bash
GET /api/city-data/{city}
```
**Example:**
```bash
curl http://localhost:3001/api/city-data/Rabat
```

### 5. **Get Available Cities List**
```bash
GET /api/cities
```
Returns array of all available Moroccan cities.

## 📍 Available Moroccan Cities

1. Rabat (Capital)
2. Casablanca
3. Marrakech
4. Fes
5. Tangier
6. Agadir
7. Meknes
8. Oujda
9. Kenitra
10. Tetouan
11. Safi
12. El Jadida
13. Khouribga
14. Beni Mellal
15. Nador
16. Settat
17. Al Hoceima
18. Ouarzazate
19. Taourirt
20. Ksar El Kebir

## 🚀 Running the Application

### Start Both Backend & Frontend
```bash
npm run dev
```
This starts:
- Backend server on `http://localhost:3001`
- Frontend (Vite) on `http://localhost:3000`

### Start Only Backend
```bash
node server.js
```

### Start Only Frontend
```bash
npm run dev:vite
```

### Build for Production
```bash
npm run build
```

## 📊 Weather Data Points

Each weather response includes:
- **Temperature** (°C)
- **Wind Speed** (km/h)
- **Precipitation** (mm)
- **Humidity** (%)
- **Weather Code** (WMO Weather Code)

## 🌍 WMO Weather Codes

| Code | Description |
|------|-------------|
| 0-2 | Clear/Cloudy |
| 3 | Very Cloudy |
| 45-48 | Foggy |
| 51-55 | Drizzle |
| 61-65 | Rain |
| 71-77 | Snow |
| 80-82 | Showers |
| 85-86 | Snow Showers |
| 95-99 | Thunderstorm |

## 📴 Alert Generation

The frontend automatically generates alerts based on:
- **Heavy Rain**: > 5mm precipitation
- **Strong Wind**: > 40 km/h
- **Extreme Heat**: > 40°C
- **Extreme Cold**: < 0°C
- **Recent Earthquakes**: Magnitude ≥ 3 within last hour

## 🔄 Data Refresh

- Dashboard automatically refreshes every 5 minutes
- Weather data is live from Open-Meteo API
- Seismic data shows events from the last 30 days

## 🛠️ File Structure

```
src/
├── components/
│   ├── Dashboard.jsx          # Main dashboard with real data
│   ├── LoginPage.jsx
│   ├── LanguagePage.jsx
│   └── ...
├── services/
│   └── weatherService.js      # API client functions
├── styles/
│   └── *.css
└── App.jsx

server.js                        # Express backend
dev-server.js                   # Development server launcher
```

## 📝 Environment Variables

Create `.env` file in root directory:
```
PORT=3001
NODE_ENV=development
```

## 🐛 Troubleshooting

### Port already in use
If port 3001 or 3000 is already in use:
```bash
# Kill process on port 3001
netstat -ano | findstr :3001
taskkill /PID <PID> /F
```

### CORS Issues
The backend is configured with CORS enabled. If issues persist, check the server.js CORS configuration.

### No data displayed
1. Check if backend is running on port 3001
2. Check browser console for errors
3. Ensure internet connection (APIs are external)
4. Try manual API call: `http://localhost:3001/api/weather/Casablanca`

## 🌟 Features

✅ Real-time weather data for all Moroccan cities
✅ Seismic activity monitoring
✅ Automatic alert generation
✅ Location-based data (using city from onboarding)
✅ Live dashboard with metrics
✅ Responsive mobile design
✅ No API keys required (Free services)

## 📞 Support

For issues or questions, check:
- Console logs for error messages
- Network tab in browser DevTools
- Server logs for backend errors

---

**Powered by:**
- Open-Meteo Weather API
- USGS Earthquake Hazards Program
- Express.js Backend
- React Frontend
