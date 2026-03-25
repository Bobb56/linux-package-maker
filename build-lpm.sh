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
cp NeonLPM/neon/bin/neon LPM-build/LPM/neon							&& \
																	\
echo ----------- PACKAGING Linux Package Maker -------------		&& \
# 3. Empaquetage de Linux Package Maker en s'utilisant lui-même		\
LPM-build/LPM/LPM.sh build LPM-build/app.yaml						&& \
																	\
echo ---------------------- DONE ! -------------------------
