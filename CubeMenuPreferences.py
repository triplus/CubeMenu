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

"""Cube menu for FreeCAD - Preferences."""


import os
import FreeCADGui as Gui
import FreeCAD as App
from PySide import QtGui
from PySide import QtCore
import CubeMenuCommon as cpc
import CubeMenuToolbars as cpt


p = cpc.p
mw = Gui.getMainWindow()
path = os.path.dirname(__file__) + "/Resources/icons/"
pCube = App.ParamGet("User parameter:BaseApp/Preferences/NaviCube")

cBoxWb = None
cBoxMenu = None
enabled = None
copyDomain = None
editContext = None


def createWidgets():
    """Create widgets on preferences dialog start."""
    global cBoxWb
    cBoxWb = QtGui.QComboBox()
    cBoxWb.setSizePolicy(QtGui.QSizePolicy.Expanding,
                         QtGui.QSizePolicy.Preferred)
    global cBoxMenu
    cBoxMenu = QtGui.QComboBox()
    cBoxMenu.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Preferred)
    global enabled
    enabled = QtGui.QListWidget()


def baseGroup():
    """Current workbench base group."""
    wb = cBoxWb.itemData(cBoxWb.currentIndex(), QtCore.Qt.UserRole)
    g = p.GetGroup("User").GetGroup(wb)
    return g


def saveEnabled():
    """Save enabled on change."""
    items = []
    for index in range(enabled.count()):
        items.append(enabled.item(index).data(QtCore.Qt.UserRole))
    domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
    if domain:
        g = cpc.findGroup(domain)
        if g:
            g.SetString("commands", ",".join(items))


def dialog():
    """Cube menu preferences dialog."""

    def onAccepted():
        """Close dialog on button close."""
        dia.done(1)

    def onFinished():
        """ Delete dialog on close."""
        dia.deleteLater()

    # Dialog
    dia = QtGui.QDialog(mw)
    dia.setModal(True)
    dia.resize(900, 500)
    dia.setWindowTitle("Cube menu preferences")
    dia.finished.connect(onFinished)

    # Stack
    stack = QtGui.QStackedWidget()
    layout = QtGui.QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    dia.setLayout(layout)
    layout.addWidget(stack)

    # Button settings
    btnSettings = QtGui.QPushButton("Settings")
    btnSettings.setToolTip("Open settings")

    def onSettings():
        """Stack widget index change."""
        stack.setCurrentIndex(2)

    btnSettings.clicked.connect(onSettings)

    # Button settings done
    btnSettingsDone = QtGui.QPushButton("Done")
    btnSettingsDone.setToolTip("Return to general preferences")

    def onBtnSettingsDone():
        """Return to general preferences."""
        btnSettings.clearFocus()
        stack.setCurrentIndex(0)
        if p.GetBool("Global", 0):
            cBoxWb.setCurrentIndex(cBoxWb.findData("GlobalPanel"))
        else:
            activeWb = Gui.activeWorkbench().__class__.__name__
            cBoxWb.setCurrentIndex(cBoxWb.findData(activeWb))

    btnSettingsDone.clicked.connect(onBtnSettingsDone)

    # Button close
    btnClose = QtGui.QPushButton("Close")
    btnClose.setToolTip("Close the preferences dialog")
    btnClose.clicked.connect(onAccepted)

    stack.insertWidget(0, general(dia, stack, btnClose, btnSettings))
    stack.insertWidget(1, edit(stack))
    stack.insertWidget(2, settings(stack, btnSettingsDone))

    btnClose.setDefault(True)
    btnClose.setFocus()

    return dia


def general(dia, stack, btnClose, btnSettings):
    """General command panel preferences."""

    # Widgets
    lo = QtGui.QVBoxLayout()
    w = QtGui.QWidget(mw)
    w.setLayout(lo)

    # Search
    search = QtGui.QLineEdit()

    # Available commands
    commands = QtGui.QListWidget()
    commands.setSortingEnabled(True)
    commands.sortItems(QtCore.Qt.AscendingOrder)

    # Reset workbench
    btnResetWb = QtGui.QPushButton()
    btnResetWb.setToolTip("Reset workbench to defaults")
    btnResetWb.setIcon(QtGui.QIcon(path + "CommandPanelReset.svg"))

    # Checkbox default menu
    ckDefault = QtGui.QCheckBox()
    ckDefault.setToolTip("Set menu as default workbench menu")

    # Button add workbench menu
    btnAddWbMenu = QtGui.QPushButton()
    btnAddWbMenu.setToolTip("Add new workbench menu")
    btnAddWbMenu.setIcon(QtGui.QIcon(path + "CommandPanelAdd.svg"))

    # Button remove workbench menu
    btnRemoveWbMenu = QtGui.QPushButton()
    btnRemoveWbMenu.setToolTip("Remove selected workbench menu")
    btnRemoveWbMenu.setIcon(QtGui.QIcon(path + "CommandPanelRemove.svg"))

    # Button copy workbench menu
    btnCopyWbMenu = QtGui.QPushButton()
    btnCopyWbMenu.setToolTip("Copy existing workbench menu")
    btnCopyWbMenu.setIcon(QtGui.QIcon(path + "CommandPanelCopy.svg"))

    # Button rename workbench menu
    btnRenameWbMenu = QtGui.QPushButton()
    btnRenameWbMenu.setToolTip("Rename selected workbench menu")
    btnRenameWbMenu.setIcon(QtGui.QIcon(path + "CommandPanelRename.svg"))

    # Button add command
    btnAddCommand = QtGui.QPushButton()
    btnAddCommand.setToolTip("Add selected command")
    btnAddCommand.setIcon(QtGui.QIcon(path + "CommandPanelAddCommand.svg"))

    # Button remove command
    btnRemoveCommand = QtGui.QPushButton()
    btnRemoveCommand.setToolTip("Remove selected command")
    btnRemoveCommand.setIcon(QtGui.QIcon(path +
                                         "CommandPanelRemoveCommand.svg"))

    # Button move up
    btnMoveUp = QtGui.QPushButton()
    btnMoveUp.setToolTip("Move selected command up")
    btnMoveUp.setIcon(QtGui.QIcon(path + "CommandPanelUp.svg"))

    # Button move down
    btnMoveDown = QtGui.QPushButton()
    btnMoveDown.setToolTip("Move selected command down")
    btnMoveDown.setIcon(QtGui.QIcon(path + "CommandPanelDown.svg"))

    # Button add separator
    btnAddSeparator = QtGui.QPushButton()
    btnAddSeparator.setToolTip("Add separator")
    btnAddSeparator.setIcon(QtGui.QIcon(path +
                                        "CommandPanelAddSeparator.svg"))

    # Button add menu
    btnAddMenu = QtGui.QPushButton()
    btnAddMenu.setToolTip("Add menu")
    btnAddMenu.setIcon(QtGui.QIcon(path + "CommandPanelAddMenu.svg"))

    # Button edit menu
    btnEditMenu = QtGui.QPushButton()
    btnEditMenu.setEnabled(False)
    btnEditMenu.setToolTip("Edit menu")
    btnEditMenu.setIcon(QtGui.QIcon(path + "CommandPanelEditMenu.svg"))

    # Layout
    loPanels = QtGui.QHBoxLayout()
    loLeft = QtGui.QVBoxLayout()
    loRight = QtGui.QVBoxLayout()
    loPanels.insertLayout(0, loLeft)
    loPanels.insertLayout(1, loRight)

    loLeft.addWidget(search)
    loLeft.addWidget(commands)

    loCBoxWb = QtGui.QHBoxLayout()
    loCBoxWb.addWidget(cBoxWb)
    loCBoxWb.addWidget(btnResetWb)

    loCBoxMenu = QtGui.QHBoxLayout()
    loCBoxMenu.addWidget(ckDefault)
    loCBoxMenu.addWidget(cBoxMenu)
    loCBoxMenu.addWidget(btnAddWbMenu)
    loCBoxMenu.addWidget(btnRemoveWbMenu)
    loCBoxMenu.addWidget(btnRenameWbMenu)
    loCBoxMenu.addWidget(btnCopyWbMenu)

    loControls = QtGui.QHBoxLayout()
    loControls.addStretch()
    loControls.addWidget(btnAddCommand)
    loControls.addWidget(btnRemoveCommand)
    loControls.addWidget(btnMoveUp)
    loControls.addWidget(btnMoveDown)
    loControls.addWidget(btnAddSeparator)
    loControls.addWidget(btnAddMenu)
    loControls.addWidget(btnEditMenu)

    loRight.insertLayout(0, loCBoxWb)
    loRight.insertLayout(1, loCBoxMenu)
    loRight.addWidget(enabled)
    loRight.insertLayout(3, loControls)

    loBottom = QtGui.QHBoxLayout()
    loBottom.addWidget(btnSettings)
    loBottom.addStretch()
    loBottom.addWidget(btnClose)

    lo.insertLayout(0, loPanels)
    lo.insertLayout(1, loBottom)

    # Functions and connections

    def onSearch(text):
        """Show or hide commands on search."""
        for index in range(commands.count()):
            if text.lower() in commands.item(index).text().lower():
                commands.item(index).setHidden(False)
            else:
                commands.item(index).setHidden(True)

    search.textEdited.connect(onSearch)

    def populateCommands():
        """Populate available commands panel."""
        actions = cpc.actionList()
        commands.blockSignals(True)
        commands.clear()
        for i in actions:
            item = QtGui.QListWidgetItem(commands)
            item.setText(actions[i].text().replace("&", ""))
            item.setToolTip(actions[i].toolTip())
            icon = actions[i].icon()
            if icon.isNull():
                item.setIcon(QtGui.QIcon(":/icons/freecad"))
            else:
                item.setIcon(icon)
            item.setData(QtCore.Qt.UserRole, actions[i].objectName())
        commands.setCurrentRow(0)
        commands.blockSignals(False)

    def populateCBoxWb():
        """Workbench selector combo box."""
        wb = Gui.listWorkbenches()
        wbSort = list(wb)
        wbSort.sort()
        wbSort.reverse()
        cBoxWb.blockSignals(True)
        cBoxWb.clear()
        for i in wbSort:
            try:
                icon = cpc.wbIcon(wb[i].Icon)
            except AttributeError:
                icon = QtGui.QIcon(":/icons/freecad")
            mt = wb[i].MenuText
            cn = wb[i].__class__.__name__
            cBoxWb.insertItem(0, icon, mt, cn)
        cBoxWb.insertSeparator(0)
        cBoxWb.insertItem(0,
                          QtGui.QIcon(":/icons/freecad"),
                          "Global menu",
                          "GlobalPanel")
        if p.GetBool("Global", 0):
            cBoxWb.setCurrentIndex(cBoxWb.findData("GlobalPanel"))
        else:
            activeWb = Gui.activeWorkbench().__class__.__name__
            cBoxWb.setCurrentIndex(cBoxWb.findData(activeWb))
        cBoxWb.blockSignals(False)

    def onCBoxWb():
        """Activate workbench on selection."""
        base = baseGroup()
        wb = Gui.listWorkbenches()
        current = cBoxWb.itemData(cBoxWb.currentIndex(),
                                  QtCore.Qt.UserRole)
        for i in wb:
            if wb[i].__class__.__name__ == current:
                Gui.activateWorkbench(i)
        cpc.defaultGroup(base)
        populateCommands()
        populateCBoxMenu()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain:
            populateEnabled(cpc.findGroup(domain))
        btnClose.setFocus()

    cBoxWb.currentIndexChanged.connect(onCBoxWb)

    def populateCBoxMenu():
        """Workbench menu combo box."""
        base = baseGroup()
        index = cpc.splitIndex(base)
        ckDefault.blockSignals(True)
        cBoxMenu.blockSignals(True)
        cBoxMenu.clear()
        for i in index:
            name = base.GetGroup(i).GetString("name")
            uid = base.GetGroup(i).GetString("uuid")
            wb = cBoxWb.itemData(cBoxWb.currentIndex(), QtCore.Qt.UserRole)
            domain = "CPMenu" + "." + "User" + "." + wb + "." + uid
            try:
                cBoxMenu.insertItem(0, name.decode("UTF-8"), domain)
            except AttributeError:
                cBoxMenu.insertItem(0, name, domain)
        default = base.GetString("default")
        data = cBoxMenu.findData(default)
        cBoxMenu.setCurrentIndex(data)
        if isDefaultMenu():
            ckDefault.setChecked(True)
        else:
            cBoxMenu.setCurrentIndex(0)
            ckDefault.setChecked(False)
        ckDefault.blockSignals(False)
        cBoxMenu.blockSignals(False)

    def onCBoxMenu():
        """Load workbench menu data."""
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())

        ckDefault.blockSignals(True)
        if isDefaultMenu():
            ckDefault.setChecked(True)
        else:
            ckDefault.setChecked(False)
        ckDefault.blockSignals(False)
        populateEnabled(cpc.findGroup(domain))
        btnClose.setFocus()

    cBoxMenu.currentIndexChanged.connect(onCBoxMenu)

    def onBtnResetWb():
        """Reset workbench to defaults."""
        base = baseGroup()
        base.Clear()
        cpc.defaultGroup(base)
        populateCBoxMenu()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain:
            populateEnabled(cpc.findGroup(domain))
        btnClose.setFocus()

    btnResetWb.clicked.connect(onBtnResetWb)

    def onBtnAddWbMenu():
        """Add new workbench menu."""
        d = QtGui.QInputDialog(dia)
        d.setModal(True)
        d.setInputMode(QtGui.QInputDialog.InputMode.TextInput)
        text, ok = QtGui.QInputDialog.getText(dia,
                                              "New menu",
                                              "Please insert menu name.")
        if ok:
            wb = cBoxWb.itemData(cBoxWb.currentIndex())
            domain = "CPMenu" + "." + "User" + "." + wb
            g = cpc.newGroup(domain)
            if g:
                uid = g.GetString("uuid")
                domain = domain + "." + uid
                try:
                    g.SetString("name", text.encode("UTF-8"))
                except TypeError:
                    g.SetString("name", text)
                populateCBoxMenu()
                cBoxMenu.setCurrentIndex(cBoxMenu.findData(domain))
                populateEnabled(g)
        d.deleteLater()
        btnClose.setFocus()

    btnAddWbMenu.clicked.connect(onBtnAddWbMenu)

    def onBtnRemoveWbMenu():
        """Remove selected workbench menu."""
        base = baseGroup()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain:
            cpc.deleteGroup(domain)
        cpc.defaultGroup(base)
        populateCBoxMenu()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        populateEnabled(cpc.findGroup(domain))
        btnClose.setFocus()

    btnRemoveWbMenu.clicked.connect(onBtnRemoveWbMenu)

    def onBtnRenameWbMenu():
        """Rename existing workbench menu."""
        d = QtGui.QInputDialog(dia)
        d.setModal(True)
        d.setInputMode(QtGui.QInputDialog.InputMode.TextInput)
        text, ok = QtGui.QInputDialog.getText(dia,
                                              "Rename menu",
                                              "Please insert new menu name.")
        if ok:
            domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
            g = cpc.findGroup(domain)
            if g:
                try:
                    g.SetString("name", text.encode("UTF-8"))
                except TypeError:
                    g.SetString("name", text)
                populateCBoxMenu()
                cBoxMenu.setCurrentIndex(cBoxMenu.findData(domain))
                populateEnabled(g)

        d.deleteLater()
        btnClose.setFocus()

    btnRenameWbMenu.clicked.connect(onBtnRenameWbMenu)

    def onCKDefault(checked):
        """Set the checkbox state."""
        base = baseGroup()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if checked:
            base.SetString("default", domain)
        else:
            base.RemString("default")

    ckDefault.stateChanged.connect(onCKDefault)

    def isDefaultMenu():
        """Check if current menu is the default menu."""
        default = False
        base = baseGroup()
        domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
        if domain and base.GetString("default") == domain:
            default = True
        return default

    def populateEnabled(group):
        """Populate enabled commands panel."""
        if group:
            items = group.GetString("commands")
        else:
            items = []
        if items:
            items = items.split(",")
        else:
            items = []
        actions = cpc.actionList()
        enabled.blockSignals(True)
        enabled.clear()
        for i in items:
            item = QtGui.QListWidgetItem(enabled)
            if i == "CPSeparator":
                item.setText("Separator")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path +
                                         "CommandPanelAddSeparator.svg"))
            elif i.startswith("CPMenu"):
                g = cpc.findGroup(i)
                if g:
                    try:
                        text = g.GetString("name").decode("UTF-8")
                    except AttributeError:
                        text = g.GetString("name")
                    item.setText("Menu: " + text)
                else:
                    item.setText("Menu")
                item.setData(QtCore.Qt.UserRole, i)
                item.setIcon(QtGui.QIcon(path + "CommandPanelAddMenu.svg"))
            elif i in actions:
                item.setText(actions[i].text().replace("&", ""))
                item.setToolTip(actions[i].toolTip())
                icon = actions[i].icon()
                if icon.isNull():
                    item.setIcon(QtGui.QIcon(":/icons/freecad"))
                else:
                    item.setIcon(icon)
                item.setData(QtCore.Qt.UserRole, i)
            else:
                item.setText(i)
                item.setToolTip("Command " + i + " is not currently available")
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icons/freecad"))
                item.setIcon(QtGui.QIcon(icon.pixmap(256,
                                                     QtGui.QIcon.Disabled)))
                item.setData(QtCore.Qt.UserRole, i)
        enabled.setCurrentRow(0)
        enabled.blockSignals(False)
        onSelectionChanged()

    def onBtnAddCommand():
        """Add the selected command."""
        row = enabled.currentRow()
        data = commands.currentItem().data(QtCore.Qt.UserRole)
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText(commands.currentItem().text().replace("&", ""))
        item.setToolTip(commands.currentItem().toolTip())
        item.setIcon(commands.currentItem().icon())
        item.setData(QtCore.Qt.UserRole, data)
        saveEnabled()

    btnAddCommand.clicked.connect(onBtnAddCommand)
    commands.itemDoubleClicked.connect(onBtnAddCommand)

    def onBtnRemoveCommand():
        """Remove the selected command."""
        row = enabled.currentRow()
        item = enabled.takeItem(row)
        if item:
            del item
            if row == enabled.count():
                enabled.setCurrentRow(row - 1)
            else:
                enabled.setCurrentRow(row)
            saveEnabled()

    btnRemoveCommand.clicked.connect(onBtnRemoveCommand)

    def onBtnMoveUp():
        """Move selected command up."""
        row = enabled.currentRow()
        if row != 0:
            item = enabled.takeItem(row)
            enabled.insertItem(row - 1, item)
            enabled.setCurrentRow(row - 1)
            saveEnabled()

    btnMoveUp.clicked.connect(onBtnMoveUp)

    def onBtnMoveDown():
        """Move selected command down."""
        row = enabled.currentRow()
        if row != enabled.count() - 1 and row != -1:
            item = enabled.takeItem(row)
            enabled.insertItem(row + 1, item)
            enabled.setCurrentRow(row + 1)
            saveEnabled()

    btnMoveDown.clicked.connect(onBtnMoveDown)

    def onBtnAddSeparator():
        """Add separator."""
        row = enabled.currentRow()
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText("Separator")
        item.setData(QtCore.Qt.UserRole, "CPSeparator")
        item.setIcon(QtGui.QIcon(path + "CommandPanelAddSeparator.svg"))
        saveEnabled()

    btnAddSeparator.clicked.connect(onBtnAddSeparator)

    def onBtnAddMenu():
        """Add menu."""
        row = enabled.currentRow()
        item = QtGui.QListWidgetItem()
        enabled.insertItem(row + 1, item)
        enabled.setCurrentRow(row + 1)
        item.setText("Menu")
        item.setData(QtCore.Qt.UserRole, "CPMenu")
        item.setIcon(QtGui.QIcon(path + "CommandPanelAddMenu.svg"))
        saveEnabled()
        onSelectionChanged()

    btnAddMenu.clicked.connect(onBtnAddMenu)

    def onSelectionChanged():
        """Set enabled state for widgets on selection changed."""
        current = enabled.currentItem()
        if current:
            data = current.data(QtCore.Qt.UserRole)
        if current and data and data.startswith("CPMenu"):
            btnEditMenu.setEnabled(True)
            btnEditMenu.setFocus()
        else:
            btnEditMenu.setEnabled(False)

    enabled.itemSelectionChanged.connect(onSelectionChanged)

    def onEditMenu():
        """Open edit dialog for selected menu ."""
        current = enabled.currentItem()
        if current and current.data(QtCore.Qt.UserRole).startswith("CPMenu"):
            global editContext
            editContext = "Set"
            stack.setCurrentIndex(1)

    btnEditMenu.clicked.connect(onEditMenu)
    enabled.itemDoubleClicked.connect(onEditMenu)

    def onCopyWbMenu():
        """Open copy menu dialog."""
        global editContext
        editContext = "Copy"
        stack.setCurrentIndex(1)

    btnCopyWbMenu.clicked.connect(onCopyWbMenu)

    def onStack(n):
        """Stack widget index change."""
        global copyDomain
        if n == 0:
            row = enabled.currentRow()
            domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
            if domain:
                populateEnabled(cpc.findGroup(domain))
            enabled.setCurrentRow(row)
            btnClose.setDefault(True)
            if copyDomain:
                populateCBoxMenu()
                cBoxMenu.setCurrentIndex(cBoxMenu.findData(copyDomain))
                domain = cBoxMenu.itemData(cBoxMenu.currentIndex())
                populateEnabled(cpc.findGroup(domain))
                copyDomain = None
        onSelectionChanged()

    stack.currentChanged.connect(onStack)

    # Available workbenches
    populateCBoxWb()
    # Default menu
    cpc.defaultGroup(baseGroup())
    # Available menus
    populateCBoxMenu()
    # Available commands
    populateCommands()
    # Enabled commands
    populateEnabled(cpc.findGroup(cBoxMenu.itemData(cBoxMenu.currentIndex())))

    return w


def edit(stack):
    """Preferences for editable commands."""

    items = []

    # Widgets
    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    widget.setLayout(layout)

    tree = QtGui.QTreeWidget()
    if editContext == "Copy":
        tree.setHeaderLabel("Copy menu: None")
    else:
        tree.setHeaderLabel("Set menu: None")

    # Button edit done
    btnEditDone = QtGui.QPushButton()
    btnEditDone.setText("Done")
    btnEditDone.setToolTip("Return to general preferences")

    # Layout button edit done
    loBtnEditDone = QtGui.QHBoxLayout()
    loBtnEditDone.addStretch()
    loBtnEditDone.addWidget(btnEditDone)

    layout.addWidget(tree)
    layout.insertLayout(1, loBtnEditDone)

    # Functions and connections

    def updateTree():
        """Update tree widget and add available menus."""
        tree.blockSignals = True
        wb = Gui.listWorkbenches()
        currentWb = cBoxWb.itemData(cBoxWb.currentIndex())

        wbSort = list(wb)
        wbSort.sort()
        if currentWb in wbSort:
            wbSort.remove(currentWb)

        def treeItems(currentWb=None,
                      mt=None,
                      cn=None,
                      expanded=False,
                      itemTop=None):
            """Create tree widget items."""
            if currentWb:
                try:
                    icon = cpc.wbIcon(wb[currentWb].Icon)
                except AttributeError:
                    icon = QtGui.QIcon(":/icons/freecad")
            else:
                icon = QtGui.QIcon(":/icons/freecad")

            if not mt:
                mt = wb[currentWb].MenuText
            if not cn:
                cn = wb[currentWb].__class__.__name__

            if itemTop:
                item = QtGui.QTreeWidgetItem(itemTop)
            else:
                item = QtGui.QTreeWidgetItem(tree)

            if cn != "GlobalPanel":
                item.setIcon(0, icon)

            try:
                item.setText(0, mt.decode("UTF-8"))
            except AttributeError:
                item.setText(0, mt)

            item.setExpanded(expanded)

            source = ["User", "System"]
            for s in source:
                itemSource = QtGui.QTreeWidgetItem(item)
                itemSource.setText(0, s)
                itemSource.setExpanded(expanded)

                base = p.GetGroup(s).GetGroup(cn)
                index = cpc.splitIndex(base)
                for i in index:
                    g = base.GetGroup(i)
                    uid = g.GetString("uuid")
                    domain = "CPMenu" + "." + s + "." + cn + "." + uid
                    itemMenu = QtGui.QTreeWidgetItem(itemSource)
                    name = g.GetString("name")
                    try:
                        itemMenu.setText(0, name.decode("UTF-8"))
                    except AttributeError:
                        itemMenu.setText(0, name)
                    itemMenu.setCheckState(0, QtCore.Qt.Unchecked)
                    itemMenu.setData(0, QtCore.Qt.UserRole, domain)
                    items.append(itemMenu)

                if itemSource.childCount() == 0:
                    item.removeChild(itemSource)

        # Current workbench
        if currentWb != "GlobalPanel":
            treeItems(currentWb, None, None, True, None)
        else:
            treeItems(None, "Global", "GlobalPanel", True, None)

        # Other workbenches
        item = QtGui.QTreeWidgetItem(tree)
        item.setText(0, "Workbenches")
        for i in wbSort:
            treeItems(i, None, None, False, item)

        # Remove empty
        for i in reversed(range(item.childCount())):
            if item.child(i).childCount() == 0:
                item.removeChild(item.child(i))

        # Global menus
        if currentWb != "GlobalPanel":
            treeItems(None, "Global", "GlobalPanel", False, None)

        # Toolbars (for copy mode only)
        if editContext == "Copy":
            tree.setHeaderLabel("Copy: None")
            itemsToolbar = QtGui.QTreeWidgetItem(tree)
            itemsToolbar.setText(0, "Toolbars")
            tb = []
            for i in mw.findChildren(QtGui.QToolBar):
                if i.objectName():
                    tb.append(i.objectName())
            tb.sort()
            for name in tb:
                domain = "CPMenu" + "." + "Toolbar" + "." + name
                itemTb = QtGui.QTreeWidgetItem(itemsToolbar)
                itemTb.setText(0, name)
                itemTb.setCheckState(0, QtCore.Qt.Unchecked)
                itemTb.setData(0, QtCore.Qt.UserRole, domain)
                items.append(itemTb)

        # Current (for set mode only)
        if editContext == "Set":
            current = enabled.currentItem()
            if current and (current.data(QtCore.Qt.UserRole)
                            .startswith("CPMenu")):
                data = current.data(QtCore.Qt.UserRole)
                for i in items:
                    if i.data(0, QtCore.Qt.UserRole) == data:
                        i.setCheckState(0, QtCore.Qt.Checked)
                        text = i.text(0)
                        tree.setHeaderLabel("Set menu: " + text)

                        parent = i.parent()
                        while parent:
                            parent.setExpanded(True)
                            parent = parent.parent()

        tree.blockSignals = False

    def onChecked(item):
        """Copy or set menu."""
        global copyDomain
        tree.blockSignals = True
        if item.checkState(0) == QtCore.Qt.Checked:
            for i in items:
                if i.checkState(0) == QtCore.Qt.Checked and i is not item:
                    i.setCheckState(0, QtCore.Qt.Unchecked)
            data = item.data(0, QtCore.Qt.UserRole)
        else:
            data = None

        text = item.text(0)

        if editContext == "Set" and data:
            tree.setHeaderLabel("Set menu: " + text)
            enabled.currentItem().setData(QtCore.Qt.UserRole,
                                          item.data(0, QtCore.Qt.UserRole))
            saveEnabled()
        elif editContext == "Set" and not data:
            tree.setHeaderLabel("Set menu: None")
            enabled.currentItem().setData(QtCore.Qt.UserRole, "CPMenu")
            saveEnabled()
        elif editContext == "Copy" and data:
            tree.setHeaderLabel("Copy: " + text)
            copyDomain = data
        elif editContext == "Copy" and not data:
            tree.setHeaderLabel("Copy: None")
            copyDomain = None
        else:
            pass
        tree.blockSignals = False

    def onEditDone():
        """Switch to general preferences."""
        global copyDomain
        tree.itemChanged.disconnect(onChecked)
        del items[:]
        tree.clear()

        if copyDomain:
            wb = cBoxWb.itemData(cBoxWb.currentIndex())
            domain = "CPMenu" + "." + "User" + "." + wb
            if copyDomain.startswith("CPMenu.Toolbar"):
                name = copyDomain.split(".")[2]
                grpCopy = cpc.newGroup(domain)
                uid = grpCopy.GetString("uuid")
                copyDomain = domain + "." + uid
                grpCopy.SetString("name", name)
                grpCopy.SetString("commands",
                                  ",".join(cpt.toolbarCommands(name)))
            else:
                grpOrigin = cpc.findGroup(copyDomain)
                grpCopy = cpc.newGroup(domain)
                uid = grpCopy.GetString("uuid")
                domain = domain + "." + uid
                if grpOrigin and grpCopy:
                    grpCopy.SetString("name", grpOrigin.GetString("name"))
                    grpCopy.SetString("commands",
                                      grpOrigin.GetString("commands"))
                    copyDomain = domain
                else:
                    copyDomain = None

        stack.setCurrentIndex(0)

    btnEditDone.clicked.connect(onEditDone)

    def onStack(n):
        """Stack widget index change."""
        if n == 1:
            btnEditDone.setDefault(True)
            btnEditDone.setFocus()
            updateTree()
            tree.itemChanged.connect(onChecked)

    stack.currentChanged.connect(onStack)

    return widget


def colorIcon(col):
    """Create a color icon."""
    pix = QtGui.QPixmap(64, 64)
    c = QtGui.QColor()
    c.setRgba(col)
    pix.fill(c)
    return QtGui.QIcon(pix)


def colorDialog(col):
    """Return a color dialog."""
    return QtGui.QColorDialog.getColor(QtGui.QColor().fromRgba(col),
                                       None,
                                       None,
                                       QtGui.QColorDialog.ShowAlphaChannel |
                                       QtGui.QColorDialog.DontUseNativeDialog)


def settings(stack, btnSettingsDone):
    """Settings widget for preferences."""

    # Colors rgba
    txtColor = 4278190080
    colFront = 2164260863
    colBack = 2162354671
    colHilite = 4289389311
    colButton = 2162354671

    # Widgets
    widgetSettings = QtGui.QWidget()
    layoutMain = QtGui.QVBoxLayout()
    widgetSettings.setLayout(layoutMain)
    widget = QtGui.QWidget()
    layout = QtGui.QVBoxLayout()
    widget.setLayout(layout)
    scroll = QtGui.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    layoutMain.addWidget(scroll)

    # Mode
    grpMode = QtGui.QGroupBox("Mode:")
    loMode = QtGui.QVBoxLayout()
    grpMode.setLayout(loMode)

    # Global panel mode
    loGlobal = QtGui.QHBoxLayout()
    lblGlobal = QtGui.QLabel("Global menu")
    ckBoxGlobal = QtGui.QCheckBox()
    ckBoxGlobal.setToolTip("Enable global menu mode")

    loGlobal.addWidget(lblGlobal)
    loGlobal.addStretch()
    loGlobal.addWidget(ckBoxGlobal)
    loMode.insertLayout(0, loGlobal)

    if p.GetBool("Global", 0):
        ckBoxGlobal.setChecked(True)

    def onCkBoxGlobal(checked):
        """Set global panel mode."""
        if checked:
            p.SetBool("Global", 1)
        else:
            p.SetBool("Global", 0)

    ckBoxGlobal.stateChanged.connect(onCkBoxGlobal)

    # Notify
    grpNotify = None
    if p.GetBool("NotifyMsg", 1):
        grpNotify = QtGui.QGroupBox("Notify:")
        loNotify = QtGui.QVBoxLayout()
        grpNotify.setLayout(loNotify)

        # Notify message
        loMsg = QtGui.QHBoxLayout()
        msg = "Create a new document to make below settings take effect."
        lblMsg = QtGui.QLabel(msg)
        btnMsg = QtGui.QPushButton()
        btnMsg.setText("Got it!")
        btnMsg.setToolTip("Don't show this message again")

        loMsg.addWidget(lblMsg)
        loMsg.addStretch()
        loMsg.addWidget(btnMsg)
        loNotify.insertLayout(0, loMsg)

        def onBtnMsg():
            """Don't show notify message."""
            p.SetBool("NotifyMsg", 0)
            grpNotify.hide()

        btnMsg.clicked.connect(onBtnMsg)

    # Style
    loStyle = QtGui.QVBoxLayout()
    grpStyle = QtGui.QGroupBox("Navigation cube:")
    grpStyle.setLayout(loStyle)

    # Style show CS
    lblShowCS = QtGui.QLabel()
    lblShowCS.setText("Show CS")
    ckShowCS = QtGui.QCheckBox()

    loShowCS = QtGui.QHBoxLayout()
    loShowCS.addWidget(lblShowCS)
    loShowCS.addStretch()
    loShowCS.addWidget(ckShowCS)

    # Style size
    ckSize = QtGui.QCheckBox()
    ckSize.setText("Size")
    spinSize = QtGui.QSpinBox()
    spinSize.setEnabled(False)
    spinSize.setRange(1, 10000)
    spinSize.setValue(pCube.GetInt("CubeSize", 132))

    loSize = QtGui.QHBoxLayout()
    loSize.addWidget(ckSize)
    loSize.addStretch()
    loSize.addWidget(spinSize)

    # Offset X
    ckOffsetX = QtGui.QCheckBox()
    ckOffsetX.setText("Offset X")
    spinOffsetX = QtGui.QSpinBox()
    spinOffsetX.setEnabled(False)
    spinOffsetX.setRange(0, 10000)
    spinOffsetX.setValue(pCube.GetInt("OffsetX", 0))

    loOffsetX = QtGui.QHBoxLayout()
    loOffsetX.addWidget(ckOffsetX)
    loOffsetX.addStretch()
    loOffsetX.addWidget(spinOffsetX)

    # Offset Y
    ckOffsetY = QtGui.QCheckBox()
    ckOffsetY.setText("Offset Y")
    spinOffsetY = QtGui.QSpinBox()
    spinOffsetY.setEnabled(False)
    spinOffsetY.setRange(0, 10000)
    spinOffsetY.setValue(pCube.GetInt("OffsetY", 0))

    loOffsetY = QtGui.QHBoxLayout()
    loOffsetY.addWidget(ckOffsetY)
    loOffsetY.addStretch()
    loOffsetY.addWidget(spinOffsetY)

    # Style color front
    ckFrontColor = QtGui.QCheckBox()
    ckFrontColor.setText("Front color")
    btnFrontColor = QtGui.QPushButton()
    btnFrontColor.setEnabled(False)

    loFrontColor = QtGui.QHBoxLayout()
    loFrontColor.addWidget(ckFrontColor)
    loFrontColor.addStretch()
    loFrontColor.addWidget(btnFrontColor)

    # Style color back
    ckBackColor = QtGui.QCheckBox()
    ckBackColor.setText("Back color")
    btnBackColor = QtGui.QPushButton()
    btnBackColor.setEnabled(False)

    loBackColor = QtGui.QHBoxLayout()
    loBackColor.addWidget(ckBackColor)
    loBackColor.addStretch()
    loBackColor.addWidget(btnBackColor)

    # Style color hilite
    ckHiliteColor = QtGui.QCheckBox()
    ckHiliteColor.setText("Hilite color")
    btnHiliteColor = QtGui.QPushButton()
    btnHiliteColor.setEnabled(False)

    loHiliteColor = QtGui.QHBoxLayout()
    loHiliteColor.addWidget(ckHiliteColor)
    loHiliteColor.addStretch()
    loHiliteColor.addWidget(btnHiliteColor)

    # Style color button
    ckButtonColor = QtGui.QCheckBox()
    ckButtonColor.setText("Button color")
    btnButtonColor = QtGui.QPushButton()
    btnButtonColor.setEnabled(False)

    loButtonColor = QtGui.QHBoxLayout()
    loButtonColor.addWidget(ckButtonColor)
    loButtonColor.addStretch()
    loButtonColor.addWidget(btnButtonColor)

    # Style layout
    loStyle.insertLayout(0, loShowCS)
    loStyle.insertLayout(1, loSize)
    loStyle.insertLayout(2, loOffsetX)
    loStyle.insertLayout(3, loOffsetY)
    loStyle.insertLayout(4, loFrontColor)
    loStyle.insertLayout(5, loBackColor)
    loStyle.insertLayout(6, loHiliteColor)
    loStyle.insertLayout(7, loButtonColor)

    # Style set initial values
    if pCube.GetBool("ShowCS", 1):
        ckShowCS.setChecked(True)

    if p.GetBool("EnableSize", 0):
        ckSize.setChecked(True)
        spinSize.setEnabled(True)

    if p.GetBool("EnableOffsetX", 0):
        ckOffsetX.setChecked(True)
        spinOffsetX.setEnabled(True)

    if p.GetBool("EnableOffsetY", 0):
        ckOffsetY.setChecked(True)
        spinOffsetY.setEnabled(True)

    if p.GetBool("EnableFrontColor", 0):
        ckFrontColor.setChecked(True)
        btnFrontColor.setEnabled(True)

    if p.GetBool("EnableBackColor", 0):
        ckBackColor.setChecked(True)
        btnBackColor.setEnabled(True)

    if p.GetBool("EnableHiliteColor", 0):
        ckHiliteColor.setChecked(True)
        btnHiliteColor.setEnabled(True)

    if p.GetBool("EnableButtonColor", 0):
        ckButtonColor.setChecked(True)
        btnButtonColor.setEnabled(True)

    btnFrontColor.setIcon(colorIcon(pCube.
                                    GetUnsigned("FrontColor",
                                                colFront)))
    btnBackColor.setIcon(colorIcon(pCube.
                                   GetUnsigned("BackColor",
                                               colBack)))
    btnHiliteColor.setIcon(colorIcon(pCube.
                                     GetUnsigned("HiliteColor",
                                                 colHilite)))
    btnButtonColor.setIcon(colorIcon(pCube.
                                     GetUnsigned("ButtonColor",
                                                 colButton)))

    # Style functions
    # Style functions show CS
    def onCkShowCS(checked):
        """Show or hide CS."""
        if checked:
            pCube.RemBool("ShowCS")
        else:
            pCube.SetBool("ShowCS", 0)

    ckShowCS.stateChanged.connect(onCkShowCS)

    # Style functions size
    def onCkSize(checked):
        """Enable cube size setting."""
        if checked:
            p.SetBool("EnableSize", 1)
            pCube.SetInt("CubeSize", spinSize.value())
            spinSize.setEnabled(True)
            spinSize.setFocus()
        else:
            p.RemBool("EnableSize")
            pCube.RemInt("CubeSize")
            spinSize.setEnabled(False)

        spinSize.blockSignals(True)
        spinSize.setValue(pCube.GetInt("CubeSize", 132))
        spinSize.blockSignals(False)

    ckSize.stateChanged.connect(onCkSize)

    def onSpinSize(value):
        """Set cube size value."""
        pCube.SetInt("CubeSize", value)

    spinSize.valueChanged.connect(onSpinSize)

    # Style functions offset X
    def onCkOffsetX(checked):
        """Enable cube offset x setting."""
        if checked:
            p.SetBool("EnableOffsetX", 1)
            pCube.SetInt("OffsetX", spinOffsetX.value())
            spinOffsetX.setEnabled(True)
            spinOffsetX.setFocus()
        else:
            p.RemBool("EnableOffsetX")
            pCube.RemInt("OffsetX")
            spinOffsetX.setEnabled(False)

        spinOffsetX.blockSignals(True)
        spinOffsetX.setValue(pCube.GetInt("OffsetX", 0))
        spinOffsetX.blockSignals(False)

    ckOffsetX.stateChanged.connect(onCkOffsetX)

    def onSpinOffsetX(value):
        """Set cube offset y value."""
        pCube.SetInt("OffsetX", value)

    spinOffsetX.valueChanged.connect(onSpinOffsetX)

    # Style functions offset Y
    def onCkOffsetY(checked):
        """Enable cube offset y setting."""
        if checked:
            p.SetBool("EnableOffsetY", 1)
            pCube.SetInt("OffsetY", spinOffsetY.value())
            spinOffsetY.setEnabled(True)
            spinOffsetY.setFocus()
        else:
            p.RemBool("EnableOffsetY")
            pCube.RemInt("OffsetY")
            spinOffsetY.setEnabled(False)

        spinOffsetY.blockSignals(True)
        spinOffsetY.setValue(pCube.GetInt("OffsetY", 0))
        spinOffsetY.blockSignals(False)

    ckOffsetY.stateChanged.connect(onCkOffsetY)

    def onSpinOffsetY(value):
        """Set cube offset y value."""
        pCube.SetInt("OffsetY", value)

    spinOffsetY.valueChanged.connect(onSpinOffsetY)

    # Style functions color front
    def onCkFrontColor(checked):
        """Enable front color setting."""
        if checked:
            p.SetBool("EnableFrontColor", 1)
            btnFrontColor.setEnabled(True)
            btnFrontColor.setFocus()
            if not pCube.GetUnsigned("FrontColor"):
                pCube.SetUnsigned("FrontColor", colFront)
        else:
            p.RemBool("EnableFrontColor")
            pCube.RemUnsigned("FrontColor")
            btnFrontColor.setEnabled(False)

        btnFrontColor.setIcon(colorIcon(pCube.
                                        GetUnsigned("FrontColor",
                                                    colFront)))

    ckFrontColor.stateChanged.connect(onCkFrontColor)

    def onBtnFrontColor():
        """Set the front color."""
        col = colorDialog(pCube.GetUnsigned("FrontColor",
                                            colFront))
        if col.isValid():
            btnFrontColor.setIcon(colorIcon(col.rgba()))
            pCube.SetUnsigned("FrontColor", col.rgba())

    btnFrontColor.clicked.connect(onBtnFrontColor)

    # Style functions color back
    def onCkBackColor(checked):
        """Enable back color setting."""
        if checked:
            p.SetBool("EnableBackColor", 1)
            btnBackColor.setEnabled(True)
            btnBackColor.setFocus()
            if not pCube.GetUnsigned("BackColor"):
                pCube.SetUnsigned("BackColor", colBack)
        else:
            p.SetBool("EnableBackColor", 0)
            pCube.RemUnsigned("BackColor")
            btnBackColor.setEnabled(False)

        btnBackColor.setIcon(colorIcon(pCube.
                                       GetUnsigned("BackColor",
                                                   colBack)))

    ckBackColor.stateChanged.connect(onCkBackColor)

    def onBtnBackColor():
        """Set the back color."""
        col = colorDialog(pCube.GetUnsigned("BackColor",
                                            colBack))
        if col.isValid():
            btnBackColor.setIcon(colorIcon(col.rgba()))
            pCube.SetUnsigned("BackColor", col.rgba())

    btnBackColor.clicked.connect(onBtnBackColor)

    # Style functions color hilite
    def onCkHiliteColor(checked):
        """Enable hilite color setting."""
        if checked:
            p.SetBool("EnableHiliteColor", 1)
            btnHiliteColor.setEnabled(True)
            btnHiliteColor.setFocus()
            if not pCube.GetUnsigned("HiliteColor"):
                pCube.SetUnsigned("HiliteColor", colHilite)
        else:
            p.RemBool("EnableHiliteColor")
            pCube.RemUnsigned("HiliteColor")
            btnHiliteColor.setEnabled(False)

        btnHiliteColor.setIcon(colorIcon(pCube.
                                         GetUnsigned("HiliteColor",
                                                     colHilite)))

    ckHiliteColor.stateChanged.connect(onCkHiliteColor)

    def onBtnHiliteColor():
        """Set the hilite color."""
        col = colorDialog(pCube.GetUnsigned("HiliteColor",
                                            colHilite))
        if col.isValid():
            btnHiliteColor.setIcon(colorIcon(col.rgba()))
            pCube.SetUnsigned("HiliteColor", col.rgba())

    btnHiliteColor.clicked.connect(onBtnHiliteColor)

    # Style functions color button
    def onCkButtonColor(checked):
        """Enable button color setting."""
        if checked:
            p.SetBool("EnableButtonColor", 1)
            btnButtonColor.setEnabled(True)
            btnButtonColor.setFocus()
            if not pCube.GetUnsigned("ButtonColor"):
                pCube.SetUnsigned("ButtonColor", colButton)
        else:
            p.SetBool("EnableButtonColor", 0)
            pCube.RemUnsigned("ButtonColor")
            btnButtonColor.setEnabled(False)

        btnButtonColor.setIcon(colorIcon(pCube.
                                         GetUnsigned("ButtonColor",
                                                     colButton)))

    ckButtonColor.stateChanged.connect(onCkButtonColor)

    def onBtnButtonColor():
        """Set the button color."""
        col = colorDialog(pCube.GetUnsigned("ButtonColor",
                                            colButton))
        if col.isValid():
            btnButtonColor.setIcon(colorIcon(col.rgba()))
            pCube.SetUnsigned("ButtonColor", col.rgba())

    btnButtonColor.clicked.connect(onBtnButtonColor)

    # Text
    loText = QtGui.QVBoxLayout()
    grpText = QtGui.QGroupBox("Navigation cube text:")
    grpText.setLayout(loText)

    # Text color
    ckTextColor = QtGui.QCheckBox()
    ckTextColor.setText("Color")
    btnTextColor = QtGui.QPushButton()
    btnTextColor.setEnabled(False)

    loTextColor = QtGui.QHBoxLayout()
    loTextColor.addWidget(ckTextColor)
    loTextColor.addStretch()
    loTextColor.addWidget(btnTextColor)

    # Font weight
    ckTextWeight = QtGui.QCheckBox()
    ckTextWeight.setText("Weight")
    spinTextWeight = QtGui.QSpinBox()
    spinTextWeight.setEnabled(False)
    spinTextWeight.setRange(1, 99)
    spinTextWeight.setValue(pCube.GetInt("FontWeight", 87))

    loTextWeight = QtGui.QHBoxLayout()
    loTextWeight.addWidget(ckTextWeight)
    loTextWeight.addStretch()
    loTextWeight.addWidget(spinTextWeight)

    # Font stretch
    ckTextStretch = QtGui.QCheckBox()
    ckTextStretch.setText("Stretch")
    spinTextStretch = QtGui.QSpinBox()
    spinTextStretch.setEnabled(False)
    spinTextStretch.setRange(1, 1000)
    spinTextStretch.setValue(pCube.GetInt("FontStretch", 62))

    loTextStretch = QtGui.QHBoxLayout()
    loTextStretch.addWidget(ckTextStretch)
    loTextStretch.addStretch()
    loTextStretch.addWidget(spinTextStretch)

    # Font string
    ckFontString = QtGui.QCheckBox()
    ckFontString.setText("Font")
    btnFontString = QtGui.QPushButton()
    btnFontString.setEnabled(False)
    btnFontString.setText(pCube.GetString("FontString",
                                          "Font").split(",")[0])

    loFontString = QtGui.QHBoxLayout()
    loFontString.addWidget(ckFontString)
    loFontString.addStretch()
    loFontString.addWidget(btnFontString)

    # Text front
    ckTextFront = QtGui.QCheckBox()
    ckTextFront.setText("Front")
    leTextFront = QtGui.QLineEdit()
    leTextFront.setMaximumWidth(300)
    leTextFront.setEnabled(False)

    loTextFront = QtGui.QHBoxLayout()
    loTextFront.addWidget(ckTextFront)
    loTextFront.addStretch()
    loTextFront.addWidget(leTextFront)

    # Text Rear
    ckTextRear = QtGui.QCheckBox()
    ckTextRear.setText("Rear")
    leTextRear = QtGui.QLineEdit()
    leTextRear.setMaximumWidth(300)
    leTextRear.setEnabled(False)

    loTextRear = QtGui.QHBoxLayout()
    loTextRear.addWidget(ckTextRear)
    loTextRear.addStretch()
    loTextRear.addWidget(leTextRear)

    # Text Top
    ckTextTop = QtGui.QCheckBox()
    ckTextTop.setText("Top")
    leTextTop = QtGui.QLineEdit()
    leTextTop.setMaximumWidth(300)
    leTextTop.setEnabled(False)

    loTextTop = QtGui.QHBoxLayout()
    loTextTop.addWidget(ckTextTop)
    loTextTop.addStretch()
    loTextTop.addWidget(leTextTop)

    # Text Bottom
    ckTextBottom = QtGui.QCheckBox()
    ckTextBottom.setText("Bottom")
    leTextBottom = QtGui.QLineEdit()
    leTextBottom.setMaximumWidth(300)
    leTextBottom.setEnabled(False)

    loTextBottom = QtGui.QHBoxLayout()
    loTextBottom.addWidget(ckTextBottom)
    loTextBottom.addStretch()
    loTextBottom.addWidget(leTextBottom)

    # Text Left
    ckTextLeft = QtGui.QCheckBox()
    ckTextLeft.setText("Left")
    leTextLeft = QtGui.QLineEdit()
    leTextLeft.setMaximumWidth(300)
    leTextLeft.setEnabled(False)

    loTextLeft = QtGui.QHBoxLayout()
    loTextLeft.addWidget(ckTextLeft)
    loTextLeft.addStretch()
    loTextLeft.addWidget(leTextLeft)

    # Text Right
    ckTextRight = QtGui.QCheckBox()
    ckTextRight.setText("Right")
    leTextRight = QtGui.QLineEdit()
    leTextRight.setMaximumWidth(300)
    leTextRight.setEnabled(False)

    loTextRight = QtGui.QHBoxLayout()
    loTextRight.addWidget(ckTextRight)
    loTextRight.addStretch()
    loTextRight.addWidget(leTextRight)

    # Text set initial values
    if p.GetBool("EnableTextColor", 0):
        ckTextColor.setChecked(True)
        btnTextColor.setEnabled(True)

    if p.GetBool("EnableTextWeight", 0):
        ckTextWeight.setChecked(True)
        spinTextWeight.setEnabled(True)

    if p.GetBool("EnableTextStretch", 0):
        ckTextStretch.setChecked(True)
        spinTextStretch.setEnabled(True)

    if p.GetBool("EnableFontString", 0):
        ckFontString.setChecked(True)
        btnFontString.setEnabled(True)

    if p.GetBool("EnableTextFront", 0):
        ckTextFront.setChecked(True)
        leTextFront.setEnabled(True)

    if p.GetBool("EnableTextRear", 0):
        ckTextRear.setChecked(True)
        leTextRear.setEnabled(True)

    if p.GetBool("EnableTextTop", 0):
        ckTextTop.setChecked(True)
        leTextTop.setEnabled(True)

    if p.GetBool("EnableTextBottom", 0):
        ckTextBottom.setChecked(True)
        leTextBottom.setEnabled(True)

    if p.GetBool("EnableTextLeft", 0):
        ckTextLeft.setChecked(True)
        leTextLeft.setEnabled(True)

    if p.GetBool("EnableTextRight", 0):
        ckTextRight.setChecked(True)
        leTextRight.setEnabled(True)

    btnTextColor.setIcon(colorIcon(pCube.GetUnsigned("TextColor",
                                                     txtColor)))

    leTextFront.setText(pCube.GetString("TextFront", "FRONT"))
    leTextRear.setText(pCube.GetString("TextRear", "REAR"))
    leTextTop.setText(pCube.GetString("TextTop", "TOP"))
    leTextBottom.setText(pCube.GetString("TextBottom", "BOTTOM"))
    leTextLeft.setText(pCube.GetString("TextLeft", "LEFT"))
    leTextRight.setText(pCube.GetString("TextRight", "RIGHT"))

    # Text functions
    # Text functions color
    def onCkTextColor(checked):
        """Enable text color setting."""
        if checked:
            p.SetBool("EnableTextColor", 1)
            btnTextColor.setEnabled(True)
            btnTextColor.setFocus()
            if not pCube.GetUnsigned("TextColor"):
                pCube.SetUnsigned("TextColor", txtColor)
        else:
            p.RemBool("EnableTextColor")
            pCube.RemUnsigned("TextColor")
            btnTextColor.setEnabled(False)

        btnTextColor.setIcon(colorIcon(pCube.
                                       GetUnsigned("TextColor",
                                                   txtColor)))

    ckTextColor.stateChanged.connect(onCkTextColor)

    def onBtnTextColor():
        """Set the text color."""
        col = colorDialog(pCube.GetUnsigned("TextColor", txtColor))
        if col.isValid():
            btnTextColor.setIcon(colorIcon(col.rgba()))
            pCube.SetUnsigned("TextColor", col.rgba())

    btnTextColor.clicked.connect(onBtnTextColor)

    # Text functions weight
    def onCkTextWeight(checked):
        """Enable font weight setting."""
        if checked:
            p.SetBool("EnableTextWeight", 1)
            pCube.SetInt("FontWeight", spinTextWeight.value())
            spinTextWeight.setEnabled(True)
            spinTextWeight.setFocus()
        else:
            p.RemBool("EnableTextWeight")
            pCube.RemInt("FontWeight")
            spinTextWeight.setEnabled(False)

        spinTextWeight.blockSignals(True)
        spinTextWeight.setValue(pCube.GetInt("FontWeight", 87))
        spinTextWeight.blockSignals(False)

    ckTextWeight.stateChanged.connect(onCkTextWeight)

    def onSpinTextWeight(value):
        """Set font weight value."""
        pCube.SetInt("FontWeight", value)

    spinTextWeight.valueChanged.connect(onSpinTextWeight)

    # Text functions stretch
    def onCkTextStretch(checked):
        """Enable font stretch setting."""
        if checked:
            p.SetBool("EnableTextStretch", 1)
            pCube.SetInt("FontStretch", spinTextStretch.value())
            spinTextStretch.setEnabled(True)
            spinTextStretch.setFocus()
        else:
            p.RemBool("EnableTextStretch")
            pCube.RemInt("FontStretch")
            spinTextStretch.setEnabled(False)

        spinTextStretch.blockSignals(True)
        spinTextStretch.setValue(pCube.GetInt("FontStretch", 62))
        spinTextStretch.blockSignals(False)

    ckTextStretch.stateChanged.connect(onCkTextStretch)

    def onSpinTextStretch(value):
        """Set font stretch value."""
        pCube.SetInt("FontStretch", value)

    spinTextStretch.valueChanged.connect(onSpinTextStretch)

    # Font string
    def onCkFontString(checked):
        """Enable font string setting."""
        if checked:
            p.SetBool("EnableFontString", 1)
            btnFontString.setEnabled(True)
            btnFontString.setFocus()
        else:
            p.RemBool("EnableFontString")
            pCube.RemString("FontString")
            btnFontString.setEnabled(False)

        s = pCube.GetString("FontString", "Font")
        s = s.split(",")[0]
        btnFontString.setText(s)

    ckFontString.stateChanged.connect(onCkFontString)

    def onBtnFontString():
        """Save as font string."""
        font = QtGui.QFont()
        s = pCube.GetString("FontString")
        if s:
            font.fromString(s)
        (font, ok) = QtGui.QFontDialog.getFont(font)
        if ok:
            pCube.SetString("FontString", font.toString())
            s = font.toString()
            s = s.split(",")[0]
            btnFontString.setText(s)

    btnFontString.clicked.connect(onBtnFontString)

    # Text functions front
    def onCkTextFront(checked):
        """Enable front text setting."""
        if checked:
            p.SetBool("EnableTextFront", 1)
            leTextFront.setEnabled(True)
            leTextFront.setFocus()
        else:
            p.RemBool("EnableTextFront")
            pCube.RemString("TextFront")
            leTextFront.setEnabled(False)

        leTextFront.setText(pCube.GetString("TextFront", "FRONT"))

    ckTextFront.stateChanged.connect(onCkTextFront)

    def onLeTextFront():
        """Set the front text."""
        pCube.SetString("TextFront", leTextFront.text())

    leTextFront.editingFinished.connect(onLeTextFront)

    # Text functions rear
    def onCkTextRear(checked):
        """Enable rear text setting."""
        if checked:
            p.SetBool("EnableTextRear", 1)
            leTextRear.setEnabled(True)
            leTextRear.setFocus()
        else:
            p.RemBool("EnableTextRear")
            pCube.RemString("TextRear")
            leTextRear.setEnabled(False)

        leTextRear.setText(pCube.GetString("TextRear", "REAR"))

    ckTextRear.stateChanged.connect(onCkTextRear)

    def onLeTextRear():
        """Set the rear text."""
        pCube.SetString("TextRear", leTextRear.text())

    leTextRear.editingFinished.connect(onLeTextRear)

    # Text functions top
    def onCkTextTop(checked):
        """Enable top text setting."""
        if checked:
            p.SetBool("EnableTextTop", 1)
            leTextTop.setEnabled(True)
            leTextTop.setFocus()
        else:
            p.RemBool("EnableTextTop")
            pCube.RemString("TextTop")
            leTextTop.setEnabled(False)

        leTextTop.setText(pCube.GetString("TextTop", "TOP"))

    ckTextTop.stateChanged.connect(onCkTextTop)

    def onLeTextTop():
        """Set the top text."""
        pCube.SetString("TextTop", leTextTop.text())

    leTextTop.editingFinished.connect(onLeTextTop)

    # Text functions bottom
    def onCkTextBottom(checked):
        """Enable bottom text setting."""
        if checked:
            p.SetBool("EnableTextBottom", 1)
            leTextBottom.setEnabled(True)
            leTextBottom.setFocus()
        else:
            p.RemBool("EnableTextBottom")
            pCube.RemString("TextBottom")
            leTextBottom.setEnabled(False)

        leTextBottom.setText(pCube.GetString("TextBottom", "BOTTOM"))

    ckTextBottom.stateChanged.connect(onCkTextBottom)

    def onLeTextBottom():
        """Set the bottom text."""
        pCube.SetString("TextBottom", leTextBottom.text())

    leTextBottom.editingFinished.connect(onLeTextBottom)

    # Text functions left
    def onCkTextLeft(checked):
        """Enable left text setting."""
        if checked:
            p.SetBool("EnableTextLeft", 1)
            leTextLeft.setEnabled(True)
            leTextLeft.setFocus()
        else:
            p.RemBool("EnableTextLeft")
            pCube.RemString("TextLeft")
            leTextLeft.setEnabled(False)

        leTextLeft.setText(pCube.GetString("TextLeft", "LEFT"))

    ckTextLeft.stateChanged.connect(onCkTextLeft)

    def onLeTextLeft():
        """Set the left text."""
        pCube.SetString("TextLeft", leTextLeft.text())

    leTextLeft.editingFinished.connect(onLeTextLeft)

    # Text functions right
    def onCkTextRight(checked):
        """Enable right text setting."""
        if checked:
            p.SetBool("EnableTextRight", 1)
            leTextRight.setEnabled(True)
            leTextRight.setFocus()
        else:
            p.RemBool("EnableTextRight")
            pCube.RemString("TextRight")
            leTextRight.setEnabled(False)

        leTextRight.setText(pCube.GetString("TextRight", "RIGHT"))

    ckTextRight.stateChanged.connect(onCkTextRight)

    def onLeTextRight():
        """Set the right text."""
        pCube.SetString("TextRight", leTextRight.text())

    leTextRight.editingFinished.connect(onLeTextRight)

    # Layout
    loText.insertLayout(0, loTextColor)
    loText.insertLayout(1, loTextWeight)
    loText.insertLayout(2, loTextStretch)
    loText.insertLayout(3, loFontString)
    loText.insertLayout(4, loTextFront)
    loText.insertLayout(5, loTextTop)
    loText.insertLayout(6, loTextRight)
    loText.insertLayout(7, loTextRear)
    loText.insertLayout(8, loTextBottom)
    loText.insertLayout(9, loTextLeft)

    loBtnSettings = QtGui.QHBoxLayout()
    loBtnSettings.addStretch()
    loBtnSettings.addWidget(btnSettingsDone)

    # Layout main
    layout.addWidget(grpMode)
    if grpNotify:
        layout.addWidget(grpNotify)
    layout.addWidget(grpStyle)
    layout.addWidget(grpText)
    layout.addStretch()
    layoutMain.insertLayout(1, loBtnSettings)

    def onStack(n):
        """Stack widget index change."""
        if n == 2:
            btnSettingsDone.setDefault(True)
            btnSettingsDone.setFocus()

    stack.currentChanged.connect(onStack)

    return widgetSettings
