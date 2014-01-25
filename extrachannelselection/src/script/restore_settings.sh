#!/bin/sh
echo ""
echo ""
echo "Restoring settings"
echo ""
echo ""
echo "GUI will restart now!"
echo ""
echo ""
init 4
rm -rf /etc/enigma2/settings
cp /tmp/settings /etc/enigma2/settings
rm -rf /tmp/settings
init 3
exit 0
