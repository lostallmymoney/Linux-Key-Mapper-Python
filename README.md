# Linux-Key-Mapper-Python
A python version of a key mapper for linux (can add any device)

Currently configured with Razer Naga 2014.
To reconfigure to your device find it's ID in Xinput and switch it at line 5.
Also change the path of the device file stream (/dev/input/by-id/....)

run

'sh start.sh'

to start the tool.
## CONFIGURATION goes like that : `
  -default
  -3=run1=record
  -3=run2=stopRecord
  -4=cfg1=other
  -5=run0=startAndStopRecord
  -7=key0=XF86AudioLowerVolume
  -9=key0=XF86AudioRaiseVolume
  -10=key0=XF86AudioPrev
  -11=run1=xdotool key XF86AudioPlay
  -12=key0=XF86AudioNext
  -end
  -other
  -3=key0=q
  -4=cfg1=default
  -7=key0=XF86AudioLowerVolume
  -9=key0=XF86AudioRaiseVolume
  -10=key0=XF86AudioPrev
  -11=run1=xdotool key XF86AudioPlay
  -12=key0=XF86AudioNext
  -end
`
run1 runs on press
run2 runs on release
run0 runs on both

key0 press a key with xdotool and releases it on releases
