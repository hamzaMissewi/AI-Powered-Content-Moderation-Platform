# Smart Content Moderation Platform

A modern content moderation platform that uses AI to automatically moderate user-generated content (text and images) with a focus on safety and compliance.

## Features

- 🛡️ Real-time content moderation
- 🤖 AI-powered text and image analysis
- 📊 Analytics dashboard
- ⚙️ Customizable moderation rules
- 🔄 CI/CD pipeline with GitHub Actions
- ☁️ Cloud-native architecture

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- **Backend**: Python FastAPI
- **AI/ML**: Hugging Face Transformers, TensorFlow
- **Database**: PostgreSQL with Prisma ORM
- **Storage**: AWS S3
- **Auth**: NextAuth.js
- **Infrastructure**: Terraform, AWS (ECS, RDS, Lambda)
- **CI/CD**: GitHub Actions

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- Docker & Docker Compose
- AWS Account (for deployment)

### Local Development

1. Clone the repository
2. Install dependencies:

   ```bash
   # Install frontend dependencies
   npm install

   # Install Python dependencies
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables (copy `.env.example` to `.env` and update values)
4. Start the development servers:

   ```bash
   # In one terminal (frontend)
   npm run dev

   # In another terminal (backend)
   cd backend
   uvicorn main:app --reload
   ```

## Project Structure

```
smart-content-moderation/
├── .github/                # GitHub Actions workflows
├── backend/                # FastAPI backend
├── frontend/               # Next.js frontend
├── infrastructure/         # Terraform configurations
├── ml/                     # ML models and training scripts
└── docs/                   # Documentation
```

## License

MIT

smart-content-moderation/
├── .github/
│ └── workflows/
│ ├── ci-cd.yml # Main CI/CD workflow
│ └── ml-training.yml # ML model training workflow
├── backend/
│ ├── app/
│ │ ├── api/
│ │ ├── core/
│ │ ├── models/
│ │ ├── services/
│ │ └── ml/
│ ├── tests/
│ ├── alembic/
│ ├── .env.example
│ └── requirements/
│ ├── base.txt
│ ├── dev.txt
│ └── prod.txt
├── frontend/
│ ├── public/
│ └── src/
└── ml/
├── models/
├── notebooks/
└── training/
