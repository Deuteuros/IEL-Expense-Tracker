#!/bin/bash
echo "Building Cashew APK..."
./venv/bin/python3 ./venv/bin/flet build apk src --product "Cashew" --org "mg.iel.cashew" --project "cashew" --clear-cache
echo "Build complete."
