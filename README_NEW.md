# XO Anime 🎌

A full-stack web application for discovering and streaming anime, manga, novels, and latest anime news. Built with Django backend and Node.js API with TypeScript.

## 📋 Features

- **Anime**: Browse, search, and watch anime powered by Gogoanime
- **Manga**: Discover and read manga powered by Mangasee123
- **Novels**: Access light novels powered by Read Light Novels
- **News**: Stay updated with latest anime news from Anime News Network
- **User Management**: Authentication and session management with django-allauth
- **Responsive Design**: Tailwind CSS for mobile-friendly interface

## 🏗️ Project Structure

### Backend (Django - Python)

```
apps/
├── anime/          # Anime content management
├── manga/          # Manga content management
├── novels/         # Light novel content management
├── news/           # News aggregation
├── core/           # Core functionality (models, middleware)
└── utils/          # Helper functions and custom template filters

xoanime/
├── settings/       # Django settings (base, dev, config)
├── urls.py         # URL routing
├── wsgi.py         # Production server
└── asgi.py         # Async server

templates/          # HTML templates organized by app
staticfiles/        # CSS, JavaScript, images
```

### Frontend (TypeScript/Node.js - Fastify API)

```
api/
└── src/
    ├── main.ts        # Fastify server setup
    └── routes/        # API endpoints
        ├── anime/
        ├── manga/
        ├── news/
        └── novels/
```

## 🛠️ Tech Stack

### Backend

- **Framework**: Django 5.0.1
- **Language**: Python 3.12+
- **Authentication**: django-allauth
- **HTTP Client**: requests
- **Development**: django-extensions, black, flake8

### API

- **Framework**: Fastify 4.26.0
- **Language**: TypeScript
- **Data Source**: @consumet/extensions
- **CORS**: @fastify/cors
- **Development**: nodemon, prettier

### Frontend

- **Styling**: Tailwind CSS
- **Assets**: Static CSS, JavaScript, images

## 📦 Prerequisites

- Python 3.12 or higher
- Node.js 12.5.0 or higher
- Yarn 1.17.3 or higher (for API)
- Poetry (for Python dependency management)

## 🚀 Installation & Setup

### Backend Setup

1. **Install Python dependencies**:

   ```bash
   poetry install
   ```

2. **Create environment configuration** (if needed):

   ```bash
   # Set up environment variables in a .env file
   ```

3. **Run migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Collect static files**:

   ```bash
   python manage.py collectstatic
   ```

5. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```
   The server will be available at `http://localhost:8000`

### API Setup

1. **Navigate to the API directory**:

   ```bash
   cd api
   ```

2. **Install Node dependencies**:

   ```bash
   yarn install
   ```

3. **Create environment variables**:

   ```bash
   # Create a .env file in the api/ directory
   PORT=5000
   ```

4. **Build TypeScript**:

   ```bash
   yarn build
   ```

5. **Start the API server**:

   ```bash
   # Development mode with hot reload
   yarn dev

   # Production mode
   yarn start
   ```

   The API will be available at `http://localhost:5000`

## 📝 Available Scripts

### Backend (Django)

```bash
python manage.py runserver      # Start development server
python manage.py migrate        # Apply database migrations
python manage.py makemigrations # Create new migrations
python manage.py shell          # Interactive Python shell
flake8                          # Lint Python code
black .                         # Format Python code
```

### API (Node.js)

```bash
yarn dev     # Start development server with hot reload
yarn build   # Compile TypeScript to JavaScript
yarn start   # Run production build
yarn lint    # Format code with prettier
```

## 🔌 API Routes

The API provides the following endpoints (all GET requests):

| Route       | Source             | Description                |
| ----------- | ------------------ | -------------------------- |
| `/anime/*`  | Gogoanime          | Anime content and metadata |
| `/manga/*`  | Mangasee123        | Manga content and chapters |
| `/novels/*` | Read Light Novels  | Light novel content        |
| `/news/*`   | Anime News Network | Latest anime news          |

**Base URL**: `http://localhost:5000`

Example:

```
GET http://localhost:5000/anime/recent
GET http://localhost:5000/manga/search?query=naruto
GET http://localhost:5000/news/recent
```

## 🗂️ Django Apps

### Anime (`apps/anime/`)

Handles anime content, including recent episodes, popular shows, genres, search, and streaming.

### Manga (`apps/manga/`)

Manages manga content with search, reading functionality, and bookmarks.

### Novels (`apps/novels/`)

Light novel management with reading, search, and tracking.

### News (`apps/news/`)

Aggregates anime news and updates from various sources.

### Core (`apps/core/`)

Core utilities including:

- Database models
- Custom middleware (XOSessionMiddleware)
- Admin interface configuration

### Utils (`apps/utils/`)

Helper functions and custom template tags:

- `helpers/fetch.py` - Data fetching utilities
- `templatetags/filters.py` - Custom Django template filters

## 🎨 Frontend

### Templates

HTML templates are organized by app in the `templates/` directory:

- `base/` - Base layout and reusable components (navbar, sidebar, news feed)
- `anime/` - Anime-specific templates
- `manga/` - Manga-specific templates
- `novels/` - Novel-specific templates
- `news/` - News article templates

### Static Files

Located in `staticfiles/`:

- `styles/` - Tailwind CSS and custom styles
- `scripts/` - JavaScript for interactivity (app.js, player.js)
- `images/` - Image assets

## ⚙️ Configuration

### Django Settings

Settings are split across multiple files in `xoanime/settings/`:

- `base.py` - Base configuration
- `dev.py` - Development settings
- `config.py` - Additional configuration

### Environment Variables

Create a `.env` file in both the root and `api/` directories:

**Root `.env`**:

```env
DEBUG=True
SECRET_KEY=your-secret-key
```

**api/.env**:

```env
PORT=5000
```

## 📚 Development

### Code Quality

Run linting and formatting:

```bash
# Python
flake8
black .

# TypeScript
yarn lint
```

### Database Migrations

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the ISC License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Akash Damle**

- Email: akash.damle@outlook.com
- GitHub: [@code-kasha](https://github.com/code-kasha)

## 🙏 Acknowledgments

- **Anime Data**: Powered by [Gogoanime](https://anitaku.to)
- **Manga Data**: Powered by [Mangasee123](https://mangasee123.com)
- **News Data**: Powered by [Anime News Network](https://animenewsnetwork.com)
- **Novels Data**: Powered by [Read Light Novels](https://animedaily.net/)
- **Data Scraping**: [@consumet/extensions](https://github.com/consumet/consumet.ts)

## ⚠️ Disclaimer

This project is for educational purposes only. Ensure you have the right to access and use content from the integrated sources. Always respect copyright and terms of service.

---

**Note**: This is a personal project. For production use, ensure proper authorization and licensing from content providers.
