{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.go
    pkgs.python3
    pkgs.python3Packages.pytest
    pkgs.python3Packages.requests
  ];

  shellHook = ''
    echo "✅ Go + Python test environment ready!"
    echo "Go version: $(go version)"
    echo "Python version: $(python3 --version)"
    echo "Use: make run  # to start your Go project"
    echo "Use: pytest -q # to run E2E tests"
  '';
}
