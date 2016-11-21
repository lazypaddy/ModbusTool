import argvemulator, os

argvemulator.ArgvCollector().mainloop()
exec(compile(open(os.path.join(os.path.split(__file__)[0], "setup.py")).read(), os.path.join(os.path.split(__file__)[0], "setup.py"), 'exec'))
