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


from PySide import QtGui
from PySide import QtCore
import FreeCADGui as Gui
import CubeMenuCommon as cpc


p = cpc.p
menuActions = []
mw = Gui.getMainWindow()
mapperShow = QtCore.QSignalMapper()


def populateMenu(domain=None):
    """Populate top or submenu."""
    if domain:
        populateSub(domain)
    else:
        populateTop()


def populateTop():
    """Populate all top menus."""
    # Global menu mode
    if p.GetBool("Global", 0):
        workbench = "GlobalPanel"
    else:
        workbench = Gui.activeWorkbench().__class__.__name__

    for menu in mw.findChildren(QtGui.QMenu, "NaviCube_Menu"):
        commands = []
        # User
        if p.GetGroup("User").GetGroup(workbench).GetString("default"):
            domain = (p.GetGroup("User")
                      .GetGroup(workbench)
                      .GetString("default"))
        # System
        elif p.GetGroup("System").GetGroup(workbench).GetString("default"):
            domain = (p.GetGroup("System")
                      .GetGroup(workbench)
                      .GetString("default"))
        # Global default
        else:
            domain = "CPMenu.System.GlobalPanel.GlobalDefault"

        group = cpc.findGroup(domain)

        if group:
            commands = cpc.splitIndex(group, "commands")
            commands = globalDefault(commands)

        addActions(menu, commands)


def populateSub(domain):
    """Populate submenu."""
    action = menuAction(domain)

    if action:
        commands = []
        menu = action.menu()
        group = cpc.findGroup(domain)
        if group:
            commands = cpc.splitIndex(group, "commands")
            commands = globalDefault(commands)

        addActions(menu, commands)


def menuAction(domain):
    """Create action with submenu."""
    action = None
    group = cpc.findGroup(domain)

    if group:
        for act in menuActions:
            if act.menu().objectName() == domain:
                action = act
        if not action:
            action = QtGui.QAction(mw)
            menu = QtGui.QMenu()
            menu.setObjectName(domain)
            action.setMenu(menu)
            menuActions.append(action)
            mapperShow.setMapping(menu, domain)
            menu.aboutToShow.connect(mapperShow.map)
        action.setText(group.GetString("name"))

    return action


def addActions(menu, commands):
    """Add actions to menu."""
    actions = cpc.actionList()

    # Empty menu
    for act in menu.actions():
        menu.removeAction(act)

    # Add actions
    for cmd in commands:
        if cmd == "CPSeparator":
            menu.addSeparator()
        elif cmd == "CPMenu":
            pass
        elif cmd.startswith("CPMenu"):
            ma = menuAction(cmd)
            if ma:
                menu.addAction(ma)
        elif cmd in actions:
            menu.addAction(actions[cmd])
        else:
            pass


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


mapperShow.mapped[str].connect(populateSub)
