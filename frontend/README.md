# Web Development MCP - Frontend

This is the frontend for the Web Development MCP (Meta-Configuration-Platform), built with React, TypeScript, and modern web technologies.

## Features

- **Modern React** - Built with React 18 and TypeScript for type safety
- **UI Components** - Reusable, accessible components built with Radix UI and styled with Tailwind CSS
- **Theming** - Light/dark mode support with system preference detection
- **Routing** - Client-side routing with React Router
- **State Management** - React Query for server state management
- **Testing** - Comprehensive test suite with Jest and React Testing Library
- **Build Tooling** - Optimized production builds with Vite

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with CSS variables for theming
- **UI Primitives**: Radix UI
- **State Management**: React Query
- **Routing**: React Router v6
- **Build Tool**: Vite
- **Testing**: Jest, React Testing Library, and user-event
- **Linting/Formatting**: ESLint, Prettier
- **Icons**: Lucide React

## Project Structure

```
frontend/
├── public/                  # Static assets
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ui/              # Shadcn/ui based components
│   │   └── common/          # Application-specific components
│   ├── features/            # Feature-based modules
│   │   ├── dashboard/       # Dashboard page and components
│   │   ├── projects/        # Projects management
│   │   ├── templates/       # Project templates
│   │   └── settings/        # User settings
│   ├── lib/                 # Utility functions and helpers
│   ├── providers/           # Context providers
│   ├── router/              # Application routes
│   ├── stores/              # State management
│   ├── types/               # TypeScript type definitions
│   ├── App.tsx              # Main application component
│   └── main.tsx             # Application entry point
├── .eslintrc.cjs            # ESLint configuration
├── .prettierrc              # Prettier configuration
├── index.html               # HTML entry point
├── package.json             # Project dependencies and scripts
├── postcss.config.js        # PostCSS configuration
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
└── vite.config.ts           # Vite configuration
```

## Getting Started

### Prerequisites

- Node.js 16+ and npm 8+

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```

### Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run preview` - Preview the production build locally
- `npm run test` - Run tests
- `npm run test:watch` - Run tests in watch mode
- `npm run test:coverage` - Generate test coverage report
- `npm run lint` - Lint the codebase
- `npm run format` - Format the codebase with Prettier
- `npm run typecheck` - Check for TypeScript errors

## Development

### Environment Variables

Create a `.env` file in the root of the frontend directory with the following variables:

```env
VITE_API_BASE_URL=http://localhost:3000/api
# Add other environment variables as needed
```

### Component Development

We follow a component-driven development approach using Storybook. To start the Storybook server:

```bash
npm run storybook
```

### Testing

Run the test suite:

```bash
npm test
```

Run tests with coverage:

```bash
npm run test:coverage
```

## Styling

We use Tailwind CSS for styling with a set of custom design tokens defined in `src/styles/theme.css`. The theme can be customized by modifying the `tailwind.config.js` file.

### Theming

The application supports light and dark themes. The theme can be toggled using the theme toggle in the application header.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Shadcn/ui](https://ui.shadcn.com/) for the component design system
- [Radix UI](https://www.radix-ui.com/) for accessible UI primitives
- [Tailwind CSS](https://tailwindcss.com/) for utility-first CSS
