# Cube menu for FreeCAD.
# Copyright (C) 2015, 2016 (as part of TabBar) triplus @ FreeCAD
# Copyright (C) 2017, 2018, 2019 (as part of CommandPanel) triplus @ FreeCAD
# Copyright (C) 2020 triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""Cube menu for FreeCAD - Commands."""


import os
from PySide import QtGui
from PySide import QtCore
import FreeCADGui as Gui
import CubeMenuGui as cpg
import CubeMenuCommon as cpc
import CubeMenuToolbars as cpt


p = cpc.p
menuList = []
buttonList = []
currentMenu = None
mw = Gui.getMainWindow()
mapperShow = QtCore.QSignalMapper()
mapperExpandCollapse = QtCore.QSignalMapper()
path = os.path.dirname(__file__) + "/Resources/icons/"


class CommandButton(QtGui.QToolButton):
    """Clear currentMenu on button press event."""
    def __init__(self):
        super(CommandButton, self).__init__()

    def mousePressEvent(self, event):
        """Press event."""
        global currentMenu
        currentMenu = None
        super(CommandButton, self).mousePressEvent(event)

    def changeEvent(self, event):
        """Change event."""
        if event.type() == QtCore.QEvent.EnabledChange:
            if self.icon().isNull():
                self.setIcon(QtGui.QIcon(":/icons/freecad"))

        super(CommandButton, self).changeEvent(event)


def buttonFactory():
    """Create button and apply the settings."""
    btn = CommandButton()
    btn.installEventFilter((cpef.InstallEvent(btn)))

    btnStyle = p.GetString("Style")

    if btnStyle == "Text":
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
    elif btnStyle == "IconText":
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    elif btnStyle == "TextBelow":
        btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
    else:
        pass

    if p.GetBool("EnableIconSize", 0):
        iconSize = p.GetInt("IconSize", 16)
        btn.setIconSize(QtCore.QSize(iconSize, iconSize))

    if p.GetBool("EnableButtonWidth", 0):
        btn.setFixedWidth(p.GetInt("ButtonWidth", 30))

    if p.GetBool("EnableButtonHeight", 0):
        btn.setFixedHeight(p.GetInt("ButtonHeight", 30))

    if p.GetBool("EnableFontSize", 0):
        font = btn.font()
        font.setPointSize(p.GetInt("FontSize", 8))
        btn.setFont(font)

    if p.GetString("Layout") == "Grid":
        policy = btn.sizePolicy()
        policy.setHorizontalPolicy(QtGui.QSizePolicy.Ignored)
        btn.setSizePolicy(policy)

    if p.GetBool("AutoRaise", 1):
        btn.setAutoRaise(True)

    return btn


def clearList(lst):
    """Empty list and delete the items."""
    try:
        item = lst.pop()
    except IndexError:
        item = None
    while item:
        item.deleteLater()
        try:
            item = lst.pop()
        except IndexError:
            item = None


def workbenchButtons(workbench):
    """Create workbench buttons from command names."""
    clearList(menuList)
    clearList(buttonList)
    tb = False
    group = None
    commands = []
    actions = cpc.actionList()

    # User
    if p.GetGroup("User").GetGroup(workbench).GetString("default"):
        domain = p.GetGroup("User").GetGroup(workbench).GetString("default")
    # System
    elif p.GetGroup("System").GetGroup(workbench).GetString("default"):
        domain = p.GetGroup("System").GetGroup(workbench).GetString("default")
    # Global default
    else:
        tb = True
        domain = "CPMenu.System.GlobalPanel.GlobalDefault"

    group = cpc.findGroup(domain)
    if group:
        commands = cpc.splitIndex(group, "commands")
        commands = globalDefault(commands)
        commands = expandedMenuCommands(commands)
    if tb:
        for cmd in cpt.toolbarCommands():
            commands.append(cmd)
    for cmd in commands:
        btn = buttonFactory()
        if cmd.startswith("CPCollapse"):
            domain = cmd.split("CPCollapse", 1)[1]
            data = ",".join([domain, str(0)])
            a = QtGui.QAction(btn)
            a.setData(data)
            a.setText("Collapse")
            a.setIcon(QtGui.QIcon(path + "CommandPanelCollapse.svg"))
            a.setToolTip("Collapse menu")
            btn.setDefaultAction(a)
            btn.setObjectName("Collapse")
            mapperExpandCollapse.setMapping(btn, data)
            btn.clicked.connect(mapperExpandCollapse.map)
        elif cmd == "CPSeparator":
            btn.setEnabled(False)
            btn.setAutoRaise(True)
            btn.setObjectName("CPSeparator")
        elif cmd == "CPSpacer":
            btn.setEnabled(False)
            btn.setObjectName("CPSpacer")
        elif cmd == "CPMenu":
            menu = QtGui.QMenu(mw)
            btn.setMenu(menu)
            btn.setIcon(QtGui.QIcon(":/icons/freecad"))
            # Theme support
            btn.setObjectName("qt_toolbutton_menubutton")
            btn.setPopupMode(QtGui.QToolButton
                             .ToolButtonPopupMode.MenuButtonPopup)
            btn.setToolTip("Empty menu")
        elif cmd.startswith("CPMenu"):
            menu = menuButton(cmd, btn, actions)
            btn.setMenu(menu)
            # Theme support
            btn.setObjectName("qt_toolbutton_menubutton")
            btn.setPopupMode(QtGui.QToolButton
                             .ToolButtonPopupMode.MenuButtonPopup)
        elif cmd in actions:
            btn.setDefaultAction(actions[cmd])
            if btn.icon().isNull():
                btn.setIcon(QtGui.QIcon(":/icons/freecad"))
        else:
            btn = None

        if (btn and
                btn.icon().isNull() and
                btn.objectName() not in ["CPSeparator", "CPSpacer"]):
            btn.setIcon(QtGui.QIcon(":/icons/freecad"))

        if not btn:
            pass
        elif (p.GetString("Layout") == "Grid" and
              btn.objectName() == "CPSpacer"):
            pass
        else:
            buttonList.append(btn)
    if p.GetBool("Menu", 0):
        for b in buttonList:
            if b.objectName() != "Collapse":
                b.clicked.connect(cpg.onInvoke)
    for m in menuList:
        m.triggered.connect(onMenuTriggered)

    return buttonList


def globalDefault(commands):
    """Add commands from global default menu."""
    temp = []
    for cmd in commands:
        if cmd == "CPGlobalDefault":
            domain = "CPMenu.System.GlobalPanel.GlobalDefault"
            group = cpc.findGroup(domain)
            if group:
                for cmdGlobal in cpc.splitIndex(group, "commands"):
                    temp.append(cmdGlobal)
        else:
            temp.append(cmd)

    return temp


def menuButton(domain, btn, actions):
    """Create menu for menu button."""
    menu = QtGui.QMenu(mw)
    menuList.append(menu)
    menu.setObjectName(domain)
    g = cpc.findGroup(domain)
    if g:
        commands = cpc.splitIndex(g, "commands")
        for cmd in commands:
            if cmd.startswith("CPMenu") or cmd.startswith("CPSpacer"):
                pass
            elif cmd == "CPSeparator":
                menu.addSeparator()
            elif cmd in actions:
                menu.addAction(actions[cmd])
            else:
                pass
        # Set default action
        try:
            btn.setDefaultAction(menu.actions()[0])
            menu.setDefaultAction(menu.actions()[0])
        except IndexError:
            pass

        default = g.GetString("Default")
        for a in menu.actions():
            name = a.objectName()
            if name and name == default:
                btn.setDefaultAction(a)
                menu.setDefaultAction(a)

        # Add expand action
        data = ",".join([domain, str(1)])
        e = QtGui.QAction(menu)
        e.setText("Expand")
        e.setIcon(QtGui.QIcon(path + "CommandPanelExpand.svg"))
        e.setToolTip("Expand menu")
        e.setData(data)

        menu.addSeparator()
        menu.addAction(e)

        mapperExpandCollapse.setMapping(e, data)
        e.triggered.connect(mapperExpandCollapse.map)

        mapperShow.setMapping(menu, domain)
        menu.aboutToShow.connect(mapperShow.map)

    if btn.icon().isNull():
        btn.setIcon(QtGui.QIcon(":/icons/freecad"))

    return menu


def expandedMenuCommands(commands):
    """Add command names for expanded menu."""
    names = []
    for cmd in commands:
        if cmd.startswith("CPMenu"):
            g = cpc.findGroup(cmd)
            if g:
                expand = g.GetBool("Expand", False)
            else:
                expand = False
            if expand:
                commandsEx = cpc.splitIndex(g, "commands")
                for cmdEx in commandsEx:
                    if cmdEx.startswith("CPMenu"):
                        pass
                    elif cmdEx == "CPSeparator":
                        pass
                    else:
                        names.append(cmdEx)
                # Move spacer after collapse button
                try:
                    last = names.pop()
                except IndexError:
                    last = None
                if last == "CPSpacer":
                    names.append("CPCollapse" + cmd)
                    names.append(last)
                elif last:
                    names.append(last)
                    names.append("CPCollapse" + cmd)
                else:
                    names.append("CPCollapse" + cmd)
            else:
                names.append(cmd)
        else:
            names.append(cmd)

    return names


def onMenuShow(domain):
    """Set currentMenu domain on menu aboutToShow"""
    global currentMenu
    currentMenu = domain


def onMenuTriggered(a):
    """Set default menu action on menu triggered."""
    if cpg.scroll.hasFocus():
        domain = currentMenu
        group = cpc.findGroup(domain)
        for menu in menuList:
            if menu.objectName() == domain:
                menu.setDefaultAction(a)
                for btn in buttonList:
                    if btn.menu() == menu:
                        btn.setDefaultAction(a)
                        if btn.icon().isNull():
                            btn.setIcon(QtGui.QIcon(":/icons/freecad"))
                name = a.objectName()
                if group and name:
                    group.SetString("Default", name)


def onMenuExpandCollapse(s):
    """Set expand or collapse menu parameter."""
    try:
        data = s.split(",")
    except AttributeError:
        data = []
    try:
        domain = data[0]
        expand = data[1]
    except IndexError:
        domain = None
        expand = None
    if domain:
        g = cpc.findGroup(domain)
    if g and expand == "1":
        g.SetBool("Expand", 1)
    elif g:
        g.SetBool("Expand", 0)
    else:
        pass

    cpg.onWorkbench()


mapperShow.mapped[str].connect(onMenuShow)
mapperExpandCollapse.mapped[str].connect(onMenuExpandCollapse)
