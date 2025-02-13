# Cleanbill

Cleanbill is an AI-powered healthcare bill analysis platform that helps patients understand their medical bills, identify potential savings, and take control of their healthcare costs.

## Features

- **Intelligent Bill Analysis**: Automatically scans and analyzes medical bills for errors, overcharges, and savings opportunities
- **Coverage Verification**: Checks insurance coverage and pre-authorization requirements
- **Cost Comparison**: Analyzes costs for similar services in your region
- **Savings Identification**: Finds potential savings through billing rate adjustments, network discounts, and duplicate charge detection
- **Clear Summaries**: Provides easy-to-understand breakdowns of medical bills and potential savings

## Tech Stack

- **Frontend**: SvelteKit, TailwindCSS
- **UI/UX**: Modern, responsive design with accessibility features
- **Animations**: Smooth transitions and loading states
- **Theme Support**: Light/dark mode theming

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/yourusername/cleanbill.git
cd cleanbill
```

2. Install dependencies:

```bash
pnpm install
```

3. Start the development server:

```bash
pnpm dev
```

4. Open your browser and navigate to `http://localhost:5173`

## Deployment

The marketing website is automatically deployed to Vercel. Here's how it's set up:

1. The `/apps/marketing` directory is configured as a separate Vercel project
2. Deployment is triggered on pushes to the `main` branch
3. Build settings in Vercel:
   ```
   Framework Preset: SvelteKit
   Root Directory: apps/marketing
   Build Command: pnpm build
   Output Directory: .svelte-kit
   Install Command: pnpm install
   ```

## Project Structure

```
apps/
├── marketing/           # Marketing website
│   ├── src/
│   │   ├── lib/        # Shared components and utilities
│   │   │   ├── components/
│   │   │   └── stores/
│   │   └── routes/     # Page routes
│   └── static/         # Static assets
└── web/                # Main application (coming soon)
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please email support@cleanbill.ai or open an issue in this repository.

## Roadmap

- [ ] User authentication and profiles
- [ ] Bill upload and OCR processing
- [ ] Integration with insurance providers
- [ ] Mobile app development
- [ ] Provider network analysis
- [ ] Payment plan recommendations

## About

Cleanbill was created to make healthcare billing transparent and manageable for everyone. Our mission is to help patients save money and understand their healthcare costs better.
