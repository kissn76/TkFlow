import mainwindow as mw
import sys



sys.path.append('./plugins')


def main():
    fullscreen=False
    # fullscreen=True
    mainwindow = mw.Mainwindow(fullscreen=fullscreen)
    mainwindow.mainloop()


if __name__ == '__main__':
    main()
