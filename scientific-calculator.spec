# PyInstaller spec: windowed onedir build (plus a .app bundle on macOS).
import sys

a = Analysis(
    ["src/scientific_calculator/__main__.py"],
    pathex=["src"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="scientific-calculator",
    console=False,
)
coll = COLLECT(exe, a.binaries, a.datas, name="scientific-calculator")

if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="Scientific Calculator.app",
        bundle_identifier="io.github.cristianat98.scientific-calculator",
    )
