"""Cube menu - global definitions."""


import CubeMenu as cp


GlobalDefaultCmd = [
    "Std_ViewIsometric",
    "Std_ViewDimetric",
    "Std_ViewTrimetric",
    "CPSeparator",
    "Std_OrthographicCamera",
    "Std_PerspectiveCamera",
    "CPSeparator",
    "Std_SelectAll",
    "Std_BoxSelection",
    "Std_SelectVisibleObjects",
    "Std_ViewFitAll",
    "Std_ViewFitSelection",
    "CPSeparator",
    "Std_ViewBoxZoom",
    "Std_ViewZoomIn",
    "Std_ViewZoomOut",
    "CPSeparator",
    "Std_AxisCross",
    "CPSeparator",
    "CubeMenu"]


GlobalDefault = {
    "workbench": "GlobalPanel",
    "uuid": "GlobalDefault",
    "name": "Default",
    "commands": GlobalDefaultCmd,
    "default": True}


cp.addMenu(GlobalDefault)
