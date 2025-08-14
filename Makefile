APP_NAME := pick
SRC := cmd/main.go
OUTPUT := $(APP_NAME)

all: build

build: $(SRC)
	@echo "Building the project..."
	go build -o $(OUTPUT) $(SRC)

run: 
	@echo "Running the application..."
	CONFIG_PATH=./config/config.toml go run $(SRC)

debug:
	@echo "Running the application with -race"
	go run -race $(SRC)

test:
	@echo "Running tests with race detector and coverage report..."
	go test ./internal/... -race -coverprofile=coverage.out -covermode=atomic
	@echo "Generating HTML coverage report..."
	go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report saved to coverage.html"

help:
	@echo "Makefile targets:"
	@echo "  build   - Build the Go project"
	@echo "  run     - Build and run the project"
	@echo "  debug   - Run the application with
	@echo "  test    - Run tests with race detector and generate coverage report"
	@echo "  help    - Show this help message"