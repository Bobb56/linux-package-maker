#!/bin/sh

# Script de build de Linux Package Maker

rm LPM_installer.lpk

echo --------------- COMPILING libnvdialog -----------------
# 1. Compilation de libnvdialog.a
cd nvdialog/build													&& \
cmake --build .														&& \
cd -																&& \
cp nvdialog/build/libnvdialog.a NeonLPM/neon/libs/libnvdialog.a		&& \
																	\
echo ----------------- COMPILING NeonLPM -------------------		&& \
# 2. Compilation de NeonLPM utilisant libnvdialog.a					\
cd NeonLPM/neon														&& \
make -f Makefile.linux_amd64 clean									&& \
make -f Makefile.linux_amd64 -j8									&& \
cd -																&& \
cp NeonLPM/neon/bin/neon LPM-dev/LPM/neon							&& \
																	\
echo ------------- CREATING LPM app directory --------------		&& \
cp -r LPM-dev LPM-build/											&& \
cd LPM-build														&& \
pyinstaller --onefile LPM/lpm.py									&& \
cp dist/lpm LPM/lpm													&& \
rm LPM/*.py															&& \
cd ..																&& \
																	\
echo ----------- PACKAGING Linux Package Maker -------------		&& \
# 3. Empaquetage de Linux Package Maker en s'utilisant lui-même		\
LPM-build/LPM/lpm build LPM-build/app.yaml							&& \
rm -r LPM-build														&& \
																	\
echo ---------------------- DONE ! -------------------------
