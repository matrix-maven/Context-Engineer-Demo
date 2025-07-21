---
inclusion: always
---

# 🚀 Kiro Global Engineering Rules

## 🎯 Core Principles

### Code Quality First

- Write code that is readable, maintainable, and self-documenting
- Prioritize clarity over cleverness
- Follow established conventions for the language/framework being used
- Keep functions focused and under 50 lines when possible

### Security by Design

- Never hardcode secrets or sensitive data
- Validate all inputs at system boundaries
- Use principle of least privilege
- Implement proper error handling without exposing internal details

### Performance Awareness

- Write efficient code but optimize only when necessary
- Cache expensive operations appropriately
- Consider memory usage and resource constraints
- Profile before optimizing

## 🧑‍💻 Universal Code Standards

### Language-Specific Standards

#### Python

- Follow PEP 8 style guidelines with 4-space indentation
- Use descriptive variable names with snake_case
- Include docstrings for all public functions and classes
- Use type hints for function parameters and return values
- Use Pydantic models for data validation and type safety
- Prefer list comprehensions over loops when readable

#### JavaScript/TypeScript

- Use consistent indentation (2 or 4 spaces)
- Prefer const/let over var
- Use meaningful variable names with camelCase
- Include JSDoc comments for complex functions
- Use async/await over Promise chains when possible

#### General Naming Conventions

- **Variables/Functions**: Use descriptive names that explain purpose
- **Constants**: Use UPPER_SNAKE_CASE for true constants
- **Classes**: Use PascalCase
- **Files**: Use kebab-case or snake_case consistently within project
- **Directories**: Use lowercase with hyphens or underscores

## 📁 Project Structure & Organization

### Standard Directory Layout

Follow consistent project structure to improve maintainability and developer onboarding:

```
project-root/
├── README.md                 # Project overview and setup
├── requirements.txt          # Dependencies (Python)
├── package.json             # Dependencies (Node.js)
├── .env.template            # Environment variable template
├── .env                     # Local environment (gitignored)
├── main.py / app.py         # Main application entry points
├── config/                  # Configuration modules
│   ├── __init__.py
│   ├── settings.py          # Application settings
│   └── validation.py        # Config validation
├── services/                # Business logic and external integrations
│   ├── __init__.py
│   ├── ai_service.py        # Core service implementations
│   └── data_service.py
├── utils/                   # Utility functions and development tools
│   ├── __init__.py
│   ├── helpers.py           # General utility functions
│   ├── logger.py            # Logging utilities
│   ├── error_handler.py     # Error handling utilities
│   └── validate_*.py        # Validation/testing scripts
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_services.py     # Unit tests
│   └── test_integration.py  # Integration tests
├── docs/                    # Documentation
│   ├── api.md               # API documentation
│   ├── setup.md             # Setup instructions
│   └── changehistory/       # Implementation history
├── ui/                      # User interface components
│   ├── __init__.py
│   ├── components.py        # UI components
│   └── layout.py            # Layout definitions
└── .kiro/                   # Kiro IDE configuration
    ├── settings/            # IDE settings
    ├── steering/            # AI steering rules
    └── specs/               # Feature specifications
```

### Directory Purpose Guidelines

#### Root Directory

- **Keep minimal**: Only essential files (README, main app files, config files)
- **No clutter**: Move development scripts, summaries, and temporary files to appropriate subdirectories
- **Clear entry points**: Make it obvious how to run the application

#### `utils/` Directory

- **Development tools**: Validation scripts, testing utilities, development helpers
- **Reusable functions**: Common utilities used across the project
- **Path handling**: Scripts in `utils/` should use proper path resolution:
  ```python
  # Add project root to Python path
  project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  sys.path.insert(0, project_root)
  ```

#### `docs/` Directory

- **Organized documentation**: Group related docs in subdirectories
- **Change history**: Use `docs/changehistory/` for implementation summaries
- **Living documentation**: Keep docs updated with code changes
- **Clear structure**: Use consistent naming and organization

#### `config/` Directory

- **Environment-specific settings**: Separate dev/prod configurations
- **Validation logic**: Include config validation utilities
- **Type safety**: Use Pydantic or similar for configuration models

#### `services/` Directory

- **Business logic**: Core application functionality
- **External integrations**: API clients, database connections
- **Provider patterns**: Consistent interfaces for similar services

#### `tests/` Directory

- **Mirror source structure**: Organize tests to match source code layout
- **Clear naming**: Use descriptive test file names
- **Separation**: Unit tests, integration tests, and validation scripts

### File Organization Rules

#### Naming Conventions

- **Python files**: Use `snake_case.py`
- **Documentation**: Use `kebab-case.md` or descriptive names
- **Configuration**: Use clear, descriptive names (`settings.py`, `ai_config.py`)
- **Tests**: Prefix with `test_` for automatic discovery

#### File Size Guidelines

- **Keep files focused**: Single responsibility per file
- **Split large files**: Break files over 500 lines into smaller modules
- **Logical grouping**: Group related functions and classes together

#### Import Organization

- **Absolute imports**: Use absolute imports from project root
- **Clear dependencies**: Make module dependencies explicit
- **Avoid circular imports**: Structure modules to prevent circular dependencies

### Documentation Structure

#### `docs/` Organization

```
docs/
├── README.md                # Main documentation index
├── setup/                   # Setup and installation guides
│   ├── installation.md
│   └── configuration.md
├── api/                     # API documentation
│   ├── endpoints.md
│   └── examples.md
├── architecture/            # System design documentation
│   ├── overview.md
│   └── components.md
├── guides/                  # How-to guides and tutorials
│   ├── getting-started.md
│   └── best-practices.md
└── changehistory/           # Implementation history and summaries
    ├── feature-x-summary.md
    └── bug-fix-y-summary.md
```

#### Documentation Best Practices

- **Keep current**: Update docs with code changes
- **Clear examples**: Include code examples and usage patterns
- **Searchable**: Use consistent terminology and clear headings
- **Linked**: Cross-reference related documentation

## 🏗️ Architecture & Design

### Separation of Concerns

- Keep business logic separate from presentation layer
- Use dependency injection for better testability
- Follow single responsibility principle
- Implement proper abstraction layers

### Data Management

- Validate data at system boundaries
- Use structured data formats (JSON, YAML) for configuration
- Implement proper error handling for data operations
- Consider data privacy and compliance requirements

### Modularity

- Write reusable, composable functions
- Avoid tight coupling between modules
- Use interfaces/contracts to define module boundaries
- Group related functionality together

## 🔄 Kiro IDE Integration

### Specs and Planning

- Use Kiro specs for complex feature development
- Document requirements before implementation
- Break down large tasks into manageable chunks
- Review and iterate on designs before coding

### Context Awareness

- Leverage Kiro's codebase scanning capabilities
- Use file and folder context appropriately
- Reference relevant documentation and examples
- Consider existing patterns and conventions in the project

### Steering Rules

- Create project-specific steering rules when needed
- Use conditional inclusion for framework-specific guidance
- Reference external files using #[[file:path]] syntax
- Keep global rules universal and project rules specific

## 🔒 Security Guidelines

### Authentication & Authorization

- Use established authentication protocols (OAuth 2.0, OpenID Connect)
- Implement proper role-based access control
- Store secrets in environment variables or secure vaults
- Never commit credentials to version control

### Input Validation

- Validate all user inputs on both client and server
- Use allowlists over denylists when possible
- Sanitize outputs to prevent injection attacks
- Implement rate limiting for public endpoints

### Dependencies

- Regularly audit and update dependencies
- Use automated security scanning tools
- Pin dependency versions for reproducibility
- Remove unused dependencies

## 🧪 Testing Standards

### Test Coverage

- Aim for 80%+ code coverage on critical paths
- Write tests before fixing bugs (TDD approach)
- Test edge cases and error conditions
- Use meaningful test names that describe behavior

### Test Types

- **Unit Tests**: Test individual functions/methods in isolation
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete user workflows
- **Performance Tests**: Validate system performance under load

### Testing Best Practices

- Keep tests simple and focused
- Use test fixtures and factories for consistent data
- Mock external dependencies appropriately
- Run tests in CI/CD pipeline

## 📚 Documentation

### Code Documentation

- Document public APIs with clear examples
- Explain complex algorithms and business logic
- Keep comments up-to-date with code changes
- Use consistent documentation formats

### Project Documentation

- Maintain clear README with setup instructions
- Document architecture decisions and trade-offs
- Keep changelog updated with notable changes
- Include troubleshooting guides for common issues

### API Documentation

- Use OpenAPI/Swagger for REST APIs
- Include request/response examples
- Document error codes and handling
- Provide SDK examples when available

## 🔄 Version Control

### Commit Standards

- Use conventional commit format: `type(scope): description`
- Write clear, descriptive commit messages
- Make atomic commits that represent single changes
- Reference issues/tickets in commit messages

### Branching Strategy

- Use feature branches for new development
- Keep main/master branch stable and deployable
- Use descriptive branch names
- Delete merged branches to keep repository clean

### Code Review

- Review all code before merging to main
- Focus on logic, security, and maintainability
- Provide constructive feedback
- Test changes locally when possible

## 📦 Dependency Management

### General Principles

- Keep dependencies minimal and well-justified
- Prefer established, well-maintained packages
- Document why each dependency is needed
- Regular security audits and updates

### Language-Specific

- **Python**: Use requirements.txt or pyproject.toml with pinned versions
- **Node.js**: Use package-lock.json for reproducible builds
- **Go**: Use go.mod for dependency management
- **Rust**: Use Cargo.toml with semantic versioning

## ⚡ Performance Guidelines

### General Optimization

- Measure before optimizing
- Focus on algorithmic improvements first
- Cache expensive computations appropriately
- Use efficient data structures for the use case

### Web Performance

- Optimize images and static assets
- Implement proper caching strategies
- Minimize bundle sizes
- Use lazy loading for non-critical resources

### Database Performance

- Use appropriate indexes
- Optimize query patterns
- Implement connection pooling
- Monitor query performance

## 🚨 Error Handling & Logging

### Error Handling

- Use structured error handling patterns
- Provide meaningful error messages to users
- Log errors with sufficient context for debugging
- Implement graceful degradation when possible

### Logging

- Use structured logging (JSON format preferred)
- Include correlation IDs for request tracing
- Log at appropriate levels (DEBUG, INFO, WARN, ERROR)
- Avoid logging sensitive information

### Monitoring

- Implement health checks for services
- Monitor key performance metrics
- Set up alerting for critical failures
- Use distributed tracing for complex systems

## 🌐 API Design

### REST APIs

- Use nouns in URLs, not verbs
- Implement proper HTTP status codes
- Version APIs appropriately
- Use consistent response formats

### GraphQL APIs

- Design schema with clear field names
- Implement proper pagination
- Use DataLoader pattern to avoid N+1 queries
- Document schema with descriptions

### General API Principles

- Design APIs for your consumers
- Implement proper authentication and authorization
- Use rate limiting to prevent abuse
- Provide comprehensive documentation

## ♿ Accessibility

### Web Accessibility

- Follow WCAG 2.1 AA guidelines
- Use semantic HTML elements
- Ensure keyboard navigation works
- Provide alternative text for images

### Testing

- Use automated accessibility testing tools
- Perform manual keyboard testing
- Test with screen readers when possible
- Include accessibility in code review process

## 🔁 Code Reuse & DRY Principles

### Avoid Duplication

- Extract common functionality into shared utilities
- Use configuration files for environment-specific values
- Create reusable components and modules
- Implement proper abstraction layers

### Refactoring Guidelines

- Refactor when files exceed 500 lines
- Extract functions when logic becomes complex
- Use design patterns appropriately
- Maintain backward compatibility when possible

## 🤖 AI-Assisted Development

### Working with AI Tools

- Use AI for code generation and suggestions
- Review and understand AI-generated code
- Test AI-generated code thoroughly
- Maintain coding standards even with AI assistance

### Prompt Engineering

- Be specific about requirements and constraints
- Provide context about existing codebase
- Ask for explanations of complex solutions
- Iterate on prompts for better results

## 🚀 Deployment & DevOps

### CI/CD Pipeline

- Automate testing and deployment
- Use infrastructure as code
- Implement proper staging environments
- Monitor deployment success and rollback if needed

### Environment Management

- Use environment variables for configuration
- Keep development and production environments similar
- Document deployment procedures
- Implement proper backup and recovery strategies

---

_These rules are designed to be universal and applicable across different projects and technologies. Adapt them to your specific project needs while maintaining the core principles._

_Last Updated: 2025-01-16_
_Version: 2.0.0_
