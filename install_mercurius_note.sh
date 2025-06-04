#!/bin/bash
# Installazione automatica Mercurius HUD su Android/Termux

echo "📦 Installazione Mercurius HUD per Note10+"

pkg update -y && pkg install -y git python

pip install --upgrade pip
pip install kivy requests speechrecognition pyttsx3

echo "🔄 Clonazione repository mobile..."
if [ ! -d "$HOME/mercurius_infinite_mobile" ]; then
    git clone https://github.com/giack891811/mercurius_infinite_mobile "$HOME/mercurius_infinite_mobile"
fi

mkdir -p /sdcard/MERCURIUS_APP/
cp -r "$HOME/mercurius_infinite_mobile" /sdcard/MERCURIUS_APP/

cat <<'EOS' > $PREFIX/bin/mercurius_hud
python $HOME/mercurius_infinite_mobile/main.py
EOS
chmod +x $PREFIX/bin/mercurius_hud

termux-create-shortcut -n "Mercurius HUD" -c "mercurius_hud" >/dev/null 2>&1 || true

echo "✅ Mercurius Jarvis Ready su Note10+"

