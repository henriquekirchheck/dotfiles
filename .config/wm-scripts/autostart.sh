#!/usr/bin/env bash

picom --experimental-backends &
dbus-launch --exit-with-session &
nitrogen --restore &
dunst &
discord --start-minimized &
