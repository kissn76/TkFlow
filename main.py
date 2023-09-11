import mainwindow as mw
import sys



sys.path.append('./plugins')


mainwindow = mw.Mainwindow()


def main():
    mainwindow.mainloop()


if __name__ == '__main__':
    main()
