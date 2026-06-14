# Anzaro - Climate Alert & Safety Platform

A modern, fast React application for weather and climate alerts providing real-time safety information to users.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ 
- npm or yarn

### Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Start development server:**
```bash
npm run dev
```

The app will open at `http://localhost:3000`

### Build for production:
```bash
npm run build
```

## 📱 Features

✅ **User Authentication** - Phone number login
✅ **Profile Setup Wizard** - 4-step onboarding with language selection, personal info, location, and accessibility settings
✅ **Welcome & Onboarding** - Video guide and feature showcase
✅ **Interactive Dashboard** - Real-time weather alerts, metrics, and quick access to emergency resources
✅ **Responsive Design** - Mobile-friendly layout
✅ **Modern UI** - Clean, professional interface with smooth animations

## 🎨 Design Features

- Clean, modern UI matching professional climate alert systems
- Responsive grid layouts
- Smooth transitions and hover effects
- Color-coded severity indicators
- Easy-to-use sidebar navigation
- Real-time data visualization cards

## 📁 Project Structure

```
src/
├── components/
│   ├── LoginPage.jsx
│   ├── LanguagePage.jsx
│   ├── PersonalInfoPage.jsx
│   ├── LocationPage.jsx
│   ├── AccessibilityPage.jsx
│   ├── WelcomePage.jsx
│   └── Dashboard.jsx
├── styles/
│   ├── global.css
│   ├── login.css
│   ├── profileSetup.css
│   └── welcome.css
├── App.jsx
└── main.jsx
```

## 🎯 Application Flow

1. **Login** - Enter phone number
2. **Language Selection** - Choose preferred language
3. **Personal Information** - Email and age
4. **Location** - City or region for alerts
5. **Accessibility** - Configure accessibility preferences
6. **Welcome** - Learn about Inzaro features
7. **Dashboard** - Main interface with alerts and metrics

## 🎨 Color Scheme

- Primary Blue: `#0066cc`
- Light Blue: `#00a8ff`
- Background: Light blue gradient
- Alerts: Orange (`#ff9800`) for warnings
- Text: Dark gray (`#1a1a1a`)

## 📦 Technologies Used

- **React 18.2** - UI Framework
- **Vite 5.0** - Build tool
- **CSS3** - Styling with flexbox and grid
- **JavaScript ES6+** - Modern JavaScript

## 🚀 Performance Optimized

- Vite for fast builds
- CSS Grid and Flexbox for responsive layouts
- Optimized component structure
- Minimal dependencies
- Fast initial load time

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 🔐 Data Management

User data is stored in component state and flows through the application via props. For production, consider integrating with a backend API.

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

---

**Inzaro** - Your Climate Safety Companion ☁️
