#!/usr/bin/env bash

# Startup qTile

# setxkbmap br &
picom --experimental-backend &
dbus-launch --exit-with-session &
nitrogen --restore &
nm-applet &
dunst &
emacs --daemon &
thunar --deamon &
discord --start-minimized &
volumeicon &
