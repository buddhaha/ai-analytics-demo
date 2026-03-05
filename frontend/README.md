# AI Analytics Frontend

React + TypeScript frontend for the AI Analytics demo.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📦 Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **TailwindCSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **Lucide React** - Icons

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.tsx    # Natural language input
│   │   ├── ChartRenderer.tsx    # Dynamic visualizations
│   │   └── ResultDisplay.tsx    # Query results display
│   ├── services/
│   │   └── api.ts               # Backend API client
│   ├── types/
│   │   └── index.ts             # TypeScript types
│   ├── App.tsx                  # Main application
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## 🔧 Configuration

Create `.env` file (optional):

```env
VITE_API_URL=http://localhost:8000
```

Default API URL is `http://localhost:8000` if not specified.

## 🎨 Features

### Chat Interface
- Natural language input with sample queries
- Auto-resizing textarea
- Keyboard shortcuts (Enter to send, Shift+Enter for new line)
- Loading states with animations

### Visualizations
- **Bar Charts** - Comparisons and rankings
- **Line Charts** - Time series and trends
- **Pie Charts** - Distributions and percentages
- **Tables** - Detailed data display

### Result Display
- Success/error indicators
- Original question display
- Generated SQL query
- AI-powered insights
- Dynamic chart rendering

## 🎯 Usage

1. Start the backend server (see main README)
2. Start the frontend dev server: `npm run dev`
3. Open http://localhost:5173
4. Ask questions in natural language!

## 📝 Example Queries

Try these questions:
- "Show me the top 10 customers by revenue"
- "What are the best selling products?"
- "Compare Q1 vs Q2 sales"
- "Which products have low ratings but high sales?"

## 🛠️ Development

### Adding New Components

```tsx
import React from 'react';

interface MyComponentProps {
  data: any;
}

const MyComponent: React.FC<MyComponentProps> = ({ data }) => {
  return <div>{/* component code */}</div>;
};

export default MyComponent;
```

### API Integration

```typescript
import { sendQuery } from './services/api';

const response = await sendQuery('Your question here');
console.log(response.results);
```

## 🐛 Troubleshooting

### Port already in use
```bash
# Use a different port
npm run dev -- --port 3000
```

### API connection errors
- Ensure backend is running on http://localhost:8000
- Check CORS settings in backend
- Verify `.env` file if using custom API URL

### Build errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📦 Building for Production

```bash
# Create optimized build
npm run build

# Preview production build locally
npm run preview
```

Build output will be in `dist/` directory.

## 🎨 Customization

### Styling
- Edit `tailwind.config.js` for theme customization
- Modify `src/index.css` for global styles
- Component styles use Tailwind utility classes

### Colors
Primary color scheme is defined in `tailwind.config.js`:
```javascript
colors: {
  primary: {
    500: '#0ea5e9',
    // ... other shades
  }
}
```

## 📄 License

MIT