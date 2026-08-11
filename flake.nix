{
  description = "Antigravity SDK Note Article Generator";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python311
            uv
          ];

          shellHook = ''
            if [ ! -d ".venv" ]; then
              echo "[-] Virtual environment not found. Creating with uv..."
              uv venv
            fi
            source .venv/bin/activate
            echo "[-] Installing Python dependencies..."
            uv pip install -e .
            echo "[+] Environment initialized successfully!"
          '';
        };
      }
    );
}
