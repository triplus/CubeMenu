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

"""Cube menu for FreeCAD - Gui."""


from PySide import QtGui
from PySide import QtCore
import FreeCAD as App
import FreeCADGui as Gui
import CubeMenuCommon as cpc
import CubeMenuCommands as cpcmd
import CubeMenuPreferences as cpp


p = cpc.p
layout = None
mw = Gui.getMainWindow()


def onShow():
    pass


def onWorkbench():
    pass


def accessoriesMenu():
    """Add cube menu preferences to accessories menu."""
    pref = QtGui.QAction(mw)
    pref.setText("Cube menu...")
    pref.setObjectName("CubeMenu")
    pref.triggered.connect(onPreferences)
    try:
        import AccessoriesMenu
        AccessoriesMenu.addItem("CubeMenu")
    except ImportError:
        a = mw.findChild(QtGui.QAction, "AccessoriesMenu")
        if a:
            a.menu().addAction(pref)
        else:
            mb = mw.menuBar()
            action = QtGui.QAction(mw)
            action.setObjectName("AccessoriesMenu")
            action.setIconText("Accessories")
            menu = QtGui.QMenu()
            action.setMenu(menu)
            menu.addAction(pref)

            def addMenu():
                """Add accessories menu to the menu bar."""
                mb.addAction(action)
                action.setVisible(True)

            addMenu()
            mw.workbenchActivated.connect(addMenu)


def onPreferences():
    """Open the preferences dialog."""
    cpp.createWidgets()
    dialog = cpp.dialog()
    dialog.show()


def onStart():
    """Start cube menu."""
    start = False
    try:
        mw.mainWindowClosed
        start = True
    except AttributeError:
        pass
    if start:
        t.stop()
        t.deleteLater()
        accessoriesMenu()
        mw.mainWindowClosed.connect(onClose)


def onClose():
    """Remove system presets and groups without index on FreeCAD close."""
    p.RemGroup("System")

    for wb in Gui.listWorkbenches():
        base = p.GetGroup("User").GetGroup(wb)
        if not cpc.splitIndex(base):
            p.GetGroup("User").RemGroup(wb)


def onPreStart():
    """Start if FreeCAD 0.18 or above is used."""
    version = App.Version()[0] + "." + App.Version()[1]
    if version >= "0.18" and mw.property("eventLoop"):
        onStart()


t = QtCore.QTimer()
t.timeout.connect(onPreStart)
t.start(500)
