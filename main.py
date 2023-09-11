import mainwindow as mw
import sys



sys.path.append('./plugins')


def main():
    mainwindow = mw.Mainwindow()
    mainwindow.mainloop()


if __name__ == '__main__':
    main()
