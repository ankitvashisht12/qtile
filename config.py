# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, DropDown, ScratchPad, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer

## DEFAULTS
follow_mouse_focus = False

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "m", lazy.window.toggle_minimize()),
    # Key([mod], "o", lazy.window.layout.maximize()),


# SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    # Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "r", lazy.reload_config()),

# QTILE LAYOUT KEYS
    # Key([mod], "g", lazy.layout.normalize()),
    # Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    # Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    # Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    # Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    # Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]

# START
# -------------------------------------
# ---- Groups and Rooms ---------------
# -------------------------------------

#
# @lazy.function
# def window_to_prev_group(qtile):
#     if qtile.currentWindow is not None:
#         i = qtile.groups.index(qtile.currentGroup)
#         qtile.currentWindow.togroup(qtile.groups[i - 1].name)
#
# @lazy.function
# def window_to_next_group(qtile):
#     if qtile.currentWindow is not None:
#         i = qtile.groups.index(qtile.currentGroup)
#         qtile.currentWindow.togroup(qtile.groups[i + 1].name)
#
# def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
#     i = qtile.screens.index(qtile.current_screen)
#     if i != 0:
#         group = qtile.screens[i - 1].group.name
#         qtile.current_window.togroup(group, switch_group=switch_group)
#         if switch_screen == True:
#             qtile.cmd_to_screen(i - 1)
#
# def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
#     i = qtile.screens.index(qtile.current_screen)
#     if i + 1 != len(qtile.screens):
#         group = qtile.screens[i + 1].group.name
#         qtile.current_window.togroup(group, switch_group=switch_group)
#         if switch_screen == True:
#             qtile.cmd_to_screen(i + 1)
#
# keys.extend([
#     # MOVE WINDOW TO NEXT SCREEN
#     Key([mod,"shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
#     Key([mod,"shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
# ])
#
# groups = []
#
# # FOR QWERTY KEYBOARDS
# group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]
#
# # FOR AZERTY KEYBOARDS
# #group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]
#
# #group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
# # group_labels = ["", "", "",  "", "", "", "", "", "", "",]
#
# # vscode icon = "﬏"
# group_labels = [ "", "", "", "", "","","", "", "", ""]
# #group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]
#
# group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "max", "monadtall", "monadtall",  "monadtall",  "monadtall"]
# #group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]
#
# for i in range(len(group_names)):
#     groups.append(
#         Group(
#             name=group_names[i],
#             layout=group_layouts[i].lower(),
#             label=group_labels[i],
#         ))
#
# for i in groups:
#     keys.extend([
#
# #CHANGE WORKSPACES
#         Key([mod], i.name, lazy.group[i.name].toscreen()),
#         Key([mod], "Tab", lazy.screen.next_group()),
#         Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
#         Key(["mod1"], "Tab", lazy.screen.next_group()),
#         Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
#
# # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
#         #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
#         Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
#     ])
#
# END


# ----------------------------
# --- Workspaces and Rooms ---
# ----------------------------

# The basic idea behind Workspaces and Rooms is to control
# DIFFERENT subsets of groups with the SAME hotkeys.
# So we can have multiple 'qwerasdf' rooms in a different workspaces.
#
# Qtile Groups are used behind the scenes, but their visibility
# is set dynamically.

def get_group_name(workspace, room):
    """ Calculate Group name based on (workspace,room) combination.
    """
    return "%s%s" % (room, workspace)

# List of available workspaces.
# Each workspace has its own prefix and hotkey.
workspaces = [
    ('AV', 'F1'),
    ('WORK', 'F2'),
]

workspaceText = widget.TextBox(
    text=workspaces[0][0],
)

# List of available rooms.
# Rooms are identical between workspaces, but they can
# be changed to different ones as well. Minor changes required.
rooms = "1234567890"

# Oops, time for a little hack there.
# This is a global object with information about current workspace.
# (viable as config code, not sure about client-server though)
wsp = {
    'current': workspaces[0][0], # first workspace is active by default
}
# ... and information about active group in the each workspace.
for w, _ in workspaces:
    wsp[w] = {
        'active_group': get_group_name(w, rooms[0]) # first room is active by default
    }

def get_workspace_groups(workspace):
    """ Get list of Groups that belongs to workspace.
    """
    return [ get_group_name(workspace, room) for room in rooms]

def get_room_groups(room):
    """ Get list of Groups that belongs to room.
    """
    return [ get_group_name(w, room) for w,_ in workspaces]

def to_workspace(workspace):
    """ Change current workspace to another one.
    """
    def f(qtile):
        global wsp

        # we need to save current active room(group) somewhere
        # to return to it later
        wsp[wsp['current']]['active_group'] = qtile.current_group.name

        # now we can change current workspace to the new one
        # (no actual switch there)
        wsp['current'] = workspace
        workspaceText.text = workspace
        # and navigate to the active group from the workspace
        # (actual switch)
        qtile.groups_map[
            wsp[workspace]['active_group']
        ].cmd_toscreen(toggle=False)
        # ].cmd_toscreen()

        # we also need to change subset of visible groups in the GroupBox widget
        qtile.widgets_map['groupbox'].visible_groups=get_workspace_groups(workspace)
        # qtile.widgets_map['groupbox'].visible_groups = get_workspace_groups(workspace)
        qtile.widgets_map['groupbox'].draw()
        # qtile.widgetMap['workspacebox'].visible_groups = get_room_groups(wsp[workspace]['active_group'][:1])
        # qtile.widgetMap['workspacebox'].draw()
        # You can do some other cosmetic stuff here.
        # For example, change Bar background depending on the current workspace.
        # # qtile.widgetMap['groupbox'].bar.background="ff0000"
    return f

def to_room(room):
    """ Change active room to another within the current workspace.
    """
    def f(qtile):
        global wsp
        # qtile.widgetMap['workspacebox'].visible_groups=get_room_groups(room)
        # qtile.widgetMap['workspacebox'].draw()
        qtile.groups_map[get_group_name(wsp['current'], room)].cmd_toscreen(toggle=False)
        # qtile.groups_map[get_group_name(wsp['current'], room)].cmd_toscreen()
    return f

def window_to_workspace(workspace, room=rooms[0]):
    """ Move active window to another workspace.
    """
    def f(qtile):
        global wsp
        qtile.current_window.togroup(wsp[workspace]['active_group'])
    return f

def window_to_room(room):
    """ Move active window to another room within the current workspace.
    """
    def f(qtile):
        global wsp
        qtile.current_window.togroup(get_group_name(wsp['current'], room))
    return f

group_labels = [ "", "", "", "", "", "", "","", "", ""] 
group_layouts = ["monadtall"] * 10

# Create individual Group for each (workspace,room) combination we have
groups = []
for workspace, hotkey in workspaces:
    for room in rooms:
        group_name = get_group_name(workspace, room)
        group_label = group_labels[int(room)]
        group_layout = group_layouts[int(room)]
        groups.append(Group(name=group_name, layout=group_layout, label=group_label))

# Assign individual hotkeys for each workspace we have
for workspace, hotkey in workspaces:
    keys.append(Key([mod], hotkey, lazy.function(
        to_workspace(workspace))))
    keys.append(Key([mod, "shift"], hotkey, lazy.function(
        window_to_workspace(workspace))))

# Assign shared hotkeys for each room we have.
# Decision about actual group to open is made dynamically.
for room in rooms:
    keys.append(Key([mod], room, lazy.function(
        to_room(room))))
    keys.append(Key([mod, "shift"], room, lazy.function(
        window_to_room(room))))

# -------------------------------------
# ---- ScratchPad ---------------------
# -------------------------------------

# # Define ScratchPad
groups.append(ScratchPad("scratchpad", [
    DropDown("term", "alacritty --class=scratch", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
]))
#
# # ScratchPad keybindings
keys.extend([
    Key([mod], "n", lazy.group['scratchpad'].dropdown_toggle('term'))
])

# ------------------------
# --- Layout -------------
# ------------------------

def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#5e81ac",
            "border_normal": "#4c566a"
            }

layout_theme = init_layout_theme()


layouts = [
    #layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadTall(**layout_theme),
    layout.MonadThreeCol(**layout_theme),
    #layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadWide(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Tile(**layout_theme),
    layout.Spiral(**layout_theme),
    layout.Max(**layout_theme),
    layout.Zoomy(**layout_theme)
]

# COLORS FOR THE BAR
#Theme name : ArcoLinux Default
def init_colors():
    return [["#2F343F", "#2F343F"], # color 0
            ["#2F343F", "#2F343F"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#fba922", "#fba922"], # color 3
            ["#3384d0", "#3384d0"], # color 4
            #["#f3f4f5", "#f3f4f5"], # color 5
            ["ffffff", "#ffffff"], # color 5
            ["#cd1f3f", "#cd1f3f"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#6790eb", "#6790eb"], # color 8
            ["#a9a9a9", "#a9a9a9"]] # color 9


colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Cascadia Code",
                fontsize = 13,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               Spacer(
                   length=8,
               ),
               workspaceText,
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.GroupBox(font="FontAwesome",
                        fontsize = 16,
                        margin_y = 1,
                        margin_x = 0,
                        padding_y = 6,
                        padding_x = 5,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[5],
                        inactive = colors[9],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = colors[8],
                        foreground = colors[2],
                        background = colors[1],
                        visible_groups = get_workspace_groups(wsp['current'])
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.CurrentLayout(
                        foreground = colors[3],
                        background = colors[1]
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.WindowName(
                        foreground = colors[7],
                        background = colors[1],
                        ),
               # widget.Net(
               #          font="Noto Sans",
               #          fontsize=12,
               #          interface="enp0s31f6",
               #          foreground=colors[2],
               #          background=colors[1],
               #          padding = 0,
               #          ),
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # widget.NetGraph(
               #          font="Noto Sans",
               #          fontsize=12,
               #          bandwidth="down",
               #          interface="auto",
               #          fill_color = colors[8],
               #          foreground=colors[2],
               #          background=colors[1],
               #          graph_color = colors[8],
               #          border_color = colors[2],
               #          padding = 0,
               #          border_width = 1,
               #          line_width = 1,
               #          ),
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # # do not activate in Virtualbox - will break qtile
               # widget.ThermalSensor(
               #          foreground = colors[5],
               #          foreground_alert = colors[6],
               #          background = colors[1],
               #          metric = True,
               #          padding = 3,
               #          threshold = 80
               #          ),
               # # battery option 1  ArcoLinux Horizontal icons do not forget to import arcobattery at the top
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # arcobattery.BatteryIcon(
               #          padding=0,
               #          scale=0.7,
               #          y_poss=2,
               #          theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
               #          update_interval = 5,
               #          background = colors[1]
               #          ),
               # # battery option 2  from Qtile
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.TextBox(
                        font="FontAwesome",
                        text="",
                        foreground=colors[2],
                        background=colors[1],
                        padding = 4,
                        fontsize=16
                        ),
               widget.Battery(
                        update_interval = 10,
                        foreground = colors[5],
                        background = colors[1],
                        low_percentage= 0.2,
                        discharge_char="",
                        charge_char="",
	                    ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.TextBox(
                        font="FontAwesome",
                        text="  ",
                        foreground=colors[7],
                        background=colors[1],
                        padding = 0,
                        fontsize=16
                        ),
               widget.Memory(
                        update_interval = 1,
                        measure_mem="G",
                        foreground = colors[5],
                        background = colors[1],
                       ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.TextBox(
                        font="FontAwesome",
                        text="  ",
                        foreground=colors[4],
                        background=colors[1],
                        padding = 0,
                        fontsize=16
                        ),
               widget.Clock(
                        foreground = colors[5],
                        background = colors[1],
                        format="%d-%m-%Y %I:%M %p"
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.Systray(
                        background=colors[1],
                        icon_size=20,
                        padding = 5
                        ),
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.8)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=0.8))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #####################################################################################
#     ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
#     #####################################################################################
#     d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d[group_names[1]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d[group_names[2]] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d[group_names[3]] = ["Gimp", "gimp" ]
#     d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d[group_names[5]] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d[group_names[6]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d[group_names[7]] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d[group_names[8]] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d[group_names[9]] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ######################################################################################
#
#     wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)
#
# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME



main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
