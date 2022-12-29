#!/bin/bash
if pgrep -x "picom" > /dev/null
then
	killall picom
else
	#picom --experimental-backends -b --config ~/.config/qtile/scripts/picom.conf
	picom -b --config ~/.config/qtile/scripts/picom.conf
fi
