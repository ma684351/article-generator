{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    uv
  ];

  shellHook = ''
    if [ ! -d ".venv" ]; then
      uv venv
    fi
    source .venv/bin/activate
    uv pip install -e .
  '';
}
