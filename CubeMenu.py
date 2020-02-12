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

"""Cube menu for FreeCAD - API."""


import CubeMenuCommon as cpc


p = cpc.p


def addMenu(menu=None):
    """addMenu({menu})

    Command panel API provides ability to preset commands for workbench.
    Settings are deleted when FreeCAD exits normally. Following is a two
    menus example for Start workbench.

    import CommandPanel as cp


    workbench = "StartWorkbench"
    # workbench = "GlobalPanel"                         # Global panel


    menuDemo = {
        "workbench": workbench,                         # Mandatory
        "uuid": "StartDemo",                            # Mandatory
        "name": "Demo",
        "commands": [
            "Std_ViewFront",                            # Command name
            "CPSeparator",                              # Separator
            "Std_ViewTop",
            "Std_ViewRight"]}


    domainDemo = cp.addMenu(menuDemo)                   # Add menuDemo


    menuDefault = {
        "workbench": workbench,
        "uuid": "StartDefault",
        "name": "Default",
        "default": True,                                # Set as default menu
        "commands": [
            "CPGlobalDefault",                          # Add global defaults
            domainDemo]}                                # Add menuDemo


    cp.addMenu(menuDefault)"""

    # Workbench
    if menu and "workbench" in menu:
        wb = menu["workbench"]
        if "." in wb or "," in wb:
            wb = None
    else:
        wb = None

    # UUID
    if wb and "uuid" in menu:
        uid = menu["uuid"]
        if "." in uid or "," in uid:
            uid = None
    else:
        uid = None

    if wb and uid:
        domain = ".".join(["CPMenu", "System", wb, uid])
        group = cpc.findGroup(domain)
        if not group:
            group = cpc.newGroup(domain)
        if group:
            # UUID
            group.SetString("uuid", uid)
            # Name
            if "name" in menu:
                group.SetString("name", menu["name"])
            # Commands
            if "commands" in menu:
                temp = []
                for cmd in menu["commands"]:
                    if cmd.startswith("CPMenu") and "," not in cmd:
                        temp.append(cmd)
                    elif "." not in cmd and "," not in cmd:
                        temp.append(cmd)
                    else:
                        pass
                group.SetString("commands", ",".join(temp))
            # Default
            if "default" in menu:
                base = p.GetGroup("System").GetGroup(wb)
                base.SetString("default", domain)
        else:
            domain = None
    else:
        domain = None

    return domain
