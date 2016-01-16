# -*- mode: python -*-
a = Analysis(['qiang.py'],
             pathex=['Y:\\code\\myproject'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='qiang.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
