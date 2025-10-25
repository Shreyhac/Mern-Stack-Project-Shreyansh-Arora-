# Web to MCP - Send Website Components Directly to AI Coding Assistants

Bridge the gap between design and code. Send pixel-perfect website components directly to Cursor or Claude Code using Model Context Protocol (MCP). No more screenshots or descriptions needed.

## 🚀 **Live Product Status**

**This is a fully functional, deployed product that is currently available on the Chrome Web Store!** 

This project was originally developed by **Shreyansh Arora** as a fun side project that has been successfully monetized. The extension is actively being sold and used by developers worldwide. For demonstration and testing purposes, the Stripe payment integration and commercial features have been removed from this codebase, but you can test the full functionality using the development setup below.

**🌐 Try the Live Extension**: [Web to MCP - Chrome Web Store](https://chromewebstore.google.com/detail/web-to-mcp-import-any-web/hbnhkfkblpgjlfonnikijlofeiabolmi)

**📊 Live Stats**: 
- ⭐ **4.6/5 Rating** (7 reviews)
- 👥 **1,000+ Active Users**
- 🏪 **Available on Chrome Web Store**
- 💰 **Offers in-app purchases** (commercial version)

## 🚀 Key Features

- **Direct Component Transfer**: Send website components directly to AI coding assistants
- **MCP Integration**: Built on Model Context Protocol for seamless AI communication
- **Multi-Platform Support**: Works with Cursor IDE and Claude Code
- **Chrome Extension**: Easy-to-use browser extension for component capture
- **Real-time Processing**: Instant component analysis and transfer
- **Free Service**: Completely free to use with no pricing barriers

## 🛠️ Tech Stack

### Frontend
- **Framework**: React with Remix
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Language**: TypeScript
- **UI Components**: Custom components with modern design

### Backend
- **Framework**: Django REST API
- **Database**: SQLite (development) / MySQL (production)
- **Authentication**: Django OAuth with Google
- **Language**: Python 3.13
- **Package Manager**: uv

### Extension
- **Framework**: WXT (Web Extension Toolkit)
- **Language**: TypeScript
- **Target**: Chrome Extension Manifest V3
- **Build Tool**: Vite

### Development Tools
- **Package Managers**: npm (frontend/extension), uv (backend)
- **Version Control**: Git
- **Development Servers**: Vite dev server, Django runserver

## 👨‍💻 Developer Information

**Original Developers**: Shreyansh Arora & Colleague  
**Primary Developer**: Shreyansh Arora  
**Roll No**: 24BCS10252  
**Email**: shreyansh.24bcs10252@sst.scaler.com  
**GitHub**: [shreyhac](https://github.com/shreyhac)

**Business Context**: This project was developed as a fun side project that has been successfully monetized on the Chrome Web Store. The extension has achieved significant success with 1,000+ active users and a 4.6/5 rating. The codebase has been modified for demonstration purposes with payment features removed.



## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **Python** (v3.13 or higher)
- **uv** (Python package manager)
- **Git**
- **Chrome Browser** (for extension testing)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mernfinal
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5174/`

### 3. Backend Setup

```bash
cd backend
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```

The backend API will be available at `http://127.0.0.1:8000/`

### 4. Extension Setup

```bash
cd extension
npm install
npm run build
```

Load the extension in Chrome:
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `extension/.output/chrome-mv3` folder

## 🔧 Development Setup

### Frontend Development

```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run type-check   # Type checking
```

### Backend Development

```bash
cd backend
uv run python manage.py runserver    # Start development server
uv run python manage.py migrate      # Apply database migrations
uv run python manage.py collectstatic # Collect static files
```

### Extension Development

```bash
cd extension
npm run dev          # Start development with hot reload
npm run build        # Build for production
npm run type-check   # Type checking
```

## 🌐 API Endpoints

### Authentication
- `POST /login/google-oauth2/` - Google OAuth login
- `POST /logout/` - User logout
- `GET /user/` - Get current user info

### Extension Download
- `GET /api/extension/download/` - Download extension as ZIP file

### Health Check
- `GET /health/` - Backend health status

## 🔒 Security

- **OAuth Authentication**: Secure Google OAuth integration
- **CORS Configuration**: Properly configured for frontend-backend communication
- **Session Management**: Django session-based authentication
- **Environment Variables**: Sensitive data stored in environment variables

## 📁 Project Structure

```
mernfinal/
├── frontend/                 # React/Remix frontend
│   ├── app/
│   │   ├── components/       # Reusable components
│   │   ├── routes/          # Page routes
│   │   └── lib/             # Utilities and configurations
│   ├── public/              # Static assets
│   └── package.json
├── backend/                 # Django REST API
│   ├── core/               # Django project settings
│   ├── users/               # User management app
│   ├── extension_download/  # Extension download app
│   └── pyproject.toml
├── extension/               # Chrome extension
│   ├── entrypoints/         # Extension entry points
│   ├── components/          # Extension components
│   └── package.json
└── README.md
```

## 🚀 Deployment

### Frontend Deployment
1. Build the frontend: `npm run build`
2. Deploy the `build` folder to your hosting service
3. Configure environment variables for production

### Backend Deployment
1. Set up production database (MySQL recommended)
2. Configure environment variables
3. Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic`
5. Deploy using your preferred method (Docker, Heroku, etc.)

### Extension Deployment
1. Build the extension: `npm run build`
2. Package the `.output/chrome-mv3` folder
3. Submit to Chrome Web Store or distribute manually

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run test
```

### Backend Testing
```bash
cd backend
uv run python manage.py test
```

## 📝 Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Frontend (.env)
```
VITE_API_URL=http://127.0.0.1:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the documentation above
2. Search existing issues on GitHub
3. Create a new issue with detailed information
4. Contact: shreyansh.24bcs10252@sst.scaler.com

## 🎯 Project Status

- ✅ **Frontend**: Fully functional React/Remix application
- ✅ **Backend**: Django REST API with authentication
- ✅ **Extension**: Chrome extension with MCP integration (Live on Chrome Web Store)
- ✅ **Database**: SQLite for development, MySQL for production
- ✅ **Authentication**: Google OAuth integration
- ✅ **Extension Download**: Direct ZIP download functionality
- ✅ **Commercial Product**: Originally developed for sale, now demo version
- ✅ **Live Deployment**: Available on Chrome Web Store for purchase

## 🔄 Recent Updates

- **Commercial to Demo**: Converted from commercial product to demonstration version
- **Payment Removal**: Removed all pricing and Stripe integration for demo purposes
- **Free Service Model**: Implemented free service model for testing
- **Extension Download**: Added direct ZIP download functionality
- **Enhanced UI/UX**: Modern design with improved user experience
- **Error Handling**: Robust error handling and user feedback
- **Documentation**: Comprehensive setup and development guide
- **Business Context**: Added information about original commercial development

---

**Made with ❤️ by Shreyansh Arora (24BCS10252)**
