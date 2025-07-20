# railway.nix
{ pkgs }:
pkgs.mkShell {
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
  ];
}
