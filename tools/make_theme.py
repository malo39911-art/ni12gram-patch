#!/usr/bin/env python3
"""Builds ni12.attheme from upstream amoled_dark.attheme using the colors of the ni12 logo.
usage: make_theme.py <in amoled_dark.attheme> <out ni12.attheme>"""
import sys, colorsys

def argb(h):  # '#rrggbb' or '#aarrggbb' -> signed 32-bit int
    h = h.lstrip('#')
    if len(h) == 6: h = 'ff' + h
    v = int(h, 16)
    return v - (1 << 32) if v >= (1 << 31) else v

# ---- palette sampled from the logo ----
BG       = '#02060c'   # near-black navy (screen / chat background)
SURFACE  = '#050d18'   # lists, action bar
SURFACE2 = '#081423'   # dialogs, panels
BUBBLE_IN  = '#0c1c30'
BUBBLE_IN_SEL = '#12304d'
ACC      = '#2fb8ff'   # neon blue (ring)
ACC_LIGHT= '#7fe1ff'   # letter outline
TEAL     = '#26d7d0'   # the "2"
OUT_A    = '#1e78ff'   # outgoing bubble gradient start
OUT_B    = '#14bcd6'   # ... end
TEXT     = '#eaf7ff'
TEXT2    = '#7e9fb8'
TIME_IN  = '#6f93ae'
TIME_OUT = '#d5f3ff'
DIVIDER  = '#0e2236'

OVERRIDES = {
 'windowBackgroundWhite': SURFACE, 'windowBackgroundGray': BG,
 'actionBarDefault': SURFACE, 'actionBarActionModeDefault': SURFACE,
 'actionBarActionModeDefaultTop': SURFACE,
 'dialogBackground': SURFACE2, 'dialogBackgroundGray': BG,
 'actionBarDefaultSubmenuBackground': SURFACE2,
 'chat_messagePanelBackground': SURFACE,
 'chat_wallpaper': BG, 'chat_wallpaper_gradient_to': '#08203a',
 'chat_wallpaper_gradient_rotation': None,   # int, handled below
 'chat_inBubble': BUBBLE_IN, 'chat_inBubbleSelected': BUBBLE_IN_SEL,
 'chat_outBubble': OUT_A, 'chat_outBubbleSelected': '#1767d6',
 'chat_outBubbleGradient': OUT_B, 'chat_outBubbleGradientAnimated': None,
 'chat_messageTextIn': TEXT, 'chat_messageTextOut': '#ffffff',
 'chat_inTimeText': TIME_IN, 'chat_outTimeText': TIME_OUT,
 'chat_inReplyLine': TEAL, 'chat_outReplyLine': '#bff4ff',
 'chat_inSentClock': TIME_IN, 'chat_outSentCheck': '#d5f3ff',
 'chats_name': TEXT, 'chats_message': TEXT2, 'chats_nameMessage': TEXT,
 'chats_unreadCounter': ACC, 'chats_actionBackground': ACC,
 'chats_pinnedOverlay': '#0b2fb8ff',
 'windowBackgroundWhiteBlueText': ACC, 'windowBackgroundWhiteBlueHeader': ACC_LIGHT,
 'windowBackgroundWhiteBlueText2': ACC, 'windowBackgroundWhiteBlueText4': ACC,
 'windowBackgroundWhiteLinkText': ACC_LIGHT,
 'switchTrackChecked': ACC, 'radioBackgroundChecked': ACC,
 'divider': DIVIDER, 'dialogTextBlue': ACC, 'dialogTextLink': ACC_LIGHT,
 'chat_serviceBackground': '#9608203a',
}
INT_OVERRIDES = {'chat_wallpaper_gradient_rotation': 45, 'chat_outBubbleGradientAnimated': 0}

TARGET_HUE = 203/360.0
def remap(v):
    """blue-family colors -> logo blue hue, keeping saturation/value/alpha"""
    u = v & 0xffffffff
    a, r, g, b = (u >> 24) & 255, (u >> 16) & 255, (u >> 8) & 255, u & 255
    h, s, val = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    if s > 0.28 and 190/360 <= h <= 260/360 and val > 0.25:
        r2, g2, b2 = colorsys.hsv_to_rgb(TARGET_HUE, min(1, s*1.05), min(1, val*1.04))
        u = (a << 24) | (round(r2*255) << 16) | (round(g2*255) << 8) | round(b2*255)
        return u - (1 << 32) if u >= (1 << 31) else u
    return v

src, dst = sys.argv[1], sys.argv[2]
out, seen = [], set()
for line in open(src, encoding='utf-8-sig').read().splitlines():
    if '=' not in line or line.startswith('#'):
        out.append(line); continue
    k, v = line.split('=', 1)
    seen.add(k)
    if k in INT_OVERRIDES:
        out.append(f'{k}={INT_OVERRIDES[k]}'); continue
    if k in OVERRIDES and OVERRIDES[k] is not None:
        out.append(f'{k}={argb(OVERRIDES[k])}'); continue
    try:
        out.append(f'{k}={remap(int(v))}')
    except ValueError:
        out.append(line)
for k, c in OVERRIDES.items():
    if k not in seen and c is not None: out.append(f'{k}={argb(c)}')
for k, n in INT_OVERRIDES.items():
    if k not in seen: out.append(f'{k}={n}')
open(dst, 'w', encoding='utf-8-sig', newline='\n').write('\n'.join(out) + '\n')
print('wrote', dst, len(out), 'lines')
