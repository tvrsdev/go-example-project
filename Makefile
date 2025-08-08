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

help:
	@echo "Makefile targets:"
	@echo "  build   - Build the Go project"
	@echo "  run     - Build and run the project"
	@echo "  debug   - Run the application with
	@echo "  help    - Show this help message"