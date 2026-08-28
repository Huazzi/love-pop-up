# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[("assets/fonts/LXGWBright-Regular.ttf", "assets/fonts")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Love Pop-Up",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Love Pop-Up",
)

app = BUNDLE(
    coll,
    name="Love Pop-Up.app",
    icon="assets/love.icns",
    bundle_identifier="com.personal.lovepopup",
    info_plist={
        "NSPrincipalClass": "NSApplication",
        "CFBundleName": "Love Pop-Up",
        "CFBundleDisplayName": "Love Pop-Up",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleVersion": "1",
    },
)
