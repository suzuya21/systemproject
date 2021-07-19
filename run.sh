#!/bin/bash
# GUI実行用シェルスクリプト
cd ~/work/systemproject/Raspberrypi/GUI
if [ $1 -eq 1 ] ; then 
  python Download.py
elif [ $1 -eq 2 ] ; then 
  python upload.py
else
  python attendance_management_gui.py
fi

