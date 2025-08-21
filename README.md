[![Releases](https://img.shields.io/github/v/release/tvrsdev/go-example-project?label=Releases&color=2b9348)](https://github.com/tvrsdev/go-example-project/releases)

# Go Example Project — Clean HTTP API, Tests, Nix & Docker

[![Go](https://img.shields.io/badge/language-Go-00ADD8?logo=go&logoColor=white)](https://golang.org)
[![Docker](https://img.shields.io/badge/container-Docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com)
[![Nix](https://img.shields.io/badge/build-Nix-7F3FBF?logo=nixos&logoColor=white)](https://nixos.org)
[![Topics](https://img.shields.io/badge/topics-docker%20%7C%20go%20%7C%20http%20api%20%7C%20tests-blue)]()

![go-gopher](https://blog.golang.org/go-brand/Go-Logo/PNG/Go-Logo_Aqua.png)

A simple, well-structured Go example project. It shows a clean REST HTTP API, test suites for unit, integration, and end-to-end (E2E) testing, and repeatable builds with Nix and Docker. Use this repo to learn patterns, copy configs, or bootstrap a small API service.

Table of contents
- Features
- Tech stack
- Quick start
- Docker
- Nix
- Testing
  - Unit tests
  - Integration tests
  - E2E tests
- API reference
- Project layout
- Development workflow
- CI tips
- Releases
- Contributing
- License

Features
- Small HTTP REST API with clear handlers and middleware.
- Layered architecture: handlers, services, repositories.
- Unit tests for logic and handlers.
- Integration tests that run against a real database or container.
- E2E tests that validate the full stack via HTTP.
- Dockerfile and docker-compose for local dev.
- Nix flake and dev shell for reproducible builds.
- Simple logging and configuration with environment variables.
- Example TDD workflow and test helpers.

Tech stack
- Go 1.20+ (module-aware)
- net/http, chi for routing
- sqlx or database/sql for DB access
- SQLite or PostgreSQL for integration tests
- Docker for containerized runs
- Nix for reproducible dev shells and builds
- Testcontainers (or testcontainers-go) for integration tests
- curl or HTTP client for E2E checks

Quick start — local (fast)
1. Clone the repo:
   git clone https://github.com/tvrsdev/go-example-project
2. Change directory:
   cd go-example-project
3. Run with go:
   go run ./cmd/server
4. Open API:
   GET http://localhost:8080/health
5. Use the API client or curl:
   curl http://localhost:8080/v1/items

This starts the API with a built-in in-memory store. It runs fast and fits local development.

Docker — run in a container
Build the container:
  docker build -t go-example-project:local .

Run the container:
  docker run --rm -p 8080:8080 -e ENV=local go-example-project:local

docker-compose for full stack (DB + app):
  docker-compose up --build

The Dockerfiles include multi-stage builds. The final image contains only the static binary. Use small base images for speed and security.

Nix — reproducible dev and build
- Enter the dev shell:
  nix develop
- Build the binary:
  nix build .#packages.x86_64-linux.go-example-project
- Run tests inside the shell:
  nix develop --command go test ./...

The repo includes a flake with pinned inputs. The dev shell provides Go, Docker CLI, and test helpers. Use Nix to reproduce CI runs locally.

Testing — structured and repeatable
We split tests into three levels:
- Unit tests: fast, run in memory, mock dependencies.
- Integration tests: start a DB or dependent service, test real DB interactions.
- E2E tests: start the full stack and drive it via HTTP.

Unit tests
- Fast feedback.
- Use table-driven tests.
- Mock repositories and external calls.
- Run:
  go test ./... -run Test.* -v

Integration tests
- Use testcontainers-go or docker-compose.
- Start PostgreSQL or SQLite in a container.
- Migrate the DB in test setup.
- Run:
  go test ./internal/integration -v

E2E tests
- Start the full stack with docker-compose or Nix.
- Run the actual binary and hit HTTP endpoints.
- Use a lightweight HTTP client for checks.
- Example run:
  docker-compose -f docker-compose.e2e.yml up --build --abort-on-container-exit
  go test ./test/e2e -v

Testing tips
- Seed test data programmatically at setup.
- Use unique DB names per test run when possible.
- Keep E2E tests focused; do not duplicate every unit test at E2E level.

HTTP API reference
Base URL: http://localhost:8080
- GET /health
  - Returns 200 with service status.
- GET /v1/items
  - Returns list of items.
- POST /v1/items
  - Create an item. JSON body: { "name": "string", "price": 100 }
- GET /v1/items/{id}
  - Returns a single item.
- PUT /v1/items/{id}
  - Update an item.
- DELETE /v1/items/{id}
  - Delete an item.

All endpoints return JSON. Handlers use context for request scope. Use a simple middleware stack for logging, tracing, and request IDs.

Project layout
- cmd/server
  - main.go — starts the server.
- internal/app
  - handlers, services, repository interfaces.
- pkg/db
  - DB helpers and migrations.
- configs
  - config.yml.example
- test
  - e2e, helpers
- docker
  - Dockerfile, docker-compose files
- nix
  - flake.nix and dev shell
- scripts
  - dev scripts for convenience

This layout keeps public API small and keeps most code unexported. It matches common Go patterns.

Development workflow
- Use feature branches.
- Run unit tests on every change.
- Run integration tests before merging into main.
- Keep E2E tests in CI gates or scheduled jobs.
- Use pre-commit hooks for formatting and vet checks.
- Use go mod tidy and go vet on CI.

CI tips
- Parallelize unit and integration jobs.
- Use a cache for Go modules.
- Run Nix builds in a separate job when you rely on flakes.
- Build the Docker image in CI and push to registry on release.

Releases
Download and run a release:
- Visit releases: https://github.com/tvrsdev/go-example-project/releases
- Download the release file you need from the Releases page. You need to download the release file and execute it. Example steps:
  1. Download asset (e.g., go-example-project_linux_amd64.tar.gz).
  2. Extract:
     tar xzf go-example-project_linux_amd64.tar.gz
  3. Make binary executable:
     chmod +x go-example-project
  4. Run:
     ./go-example-project serve --config config.yml

The Releases page lists binaries for each platform and checksum files. Use the matching asset for your OS and architecture. If the link does not work, check the Releases section on GitHub for available assets.

Badges and links
- Releases: [![Download Release](https://img.shields.io/github/downloads/tvrsdev/go-example-project/total?label=downloads&color=informational)](https://github.com/tvrsdev/go-example-project/releases)
- Latest release: [![Latest Release](https://img.shields.io/github/v/release/tvrsdev/go-example-project)](https://github.com/tvrsdev/go-example-project/releases)

Contributing
- Fork and open a pull request.
- Follow the style guide in CONTRIBUTING.md.
- Write tests for new features.
- Use small, focused commits.
- Keep public APIs backward compatible when possible.

Tips for maintainers
- Keep the Dockerfile minimal and multi-stage.
- Keep tests deterministic and isolated.
- Use feature flags for experimental behavior.
- Keep the flake lock updated monthly.

Common commands
- Build:
  go build ./cmd/server
- Test all:
  go test ./... -v
- Lint:
  golangci-lint run
- Format:
  gofmt -w .

Images and assets
- Go logo: https://blog.golang.org/go-brand/Go-Logo/PNG/Go-Logo_Aqua.png
- Docker logo: https://www.docker.com/sites/default/files/d8/2019-07/Moby-logo.png
- Nix logo: https://nixos.org/logo.png

License
This project uses the MIT License. See LICENSE for details.