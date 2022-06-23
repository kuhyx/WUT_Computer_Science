
#include "mainwindow.h" // header file included, header files for the Notepad widget
#include "universalFunctions.h"
#include <QApplication> // handle widgets, events, mouse movement, feel of window,
// header files for QApplication
#include <QLocale>
#include <QTranslator>
#include <QFile>
#include <QJsonDocument>



// main function that is the entry point for all C and C++ based applications:
int main(int argc, char *argv[]) // all exectution begins here
{
    QApplication a(argc, argv); // creates a QApplication object.
    // This object manages application-wide resources and is necessary to run
    // any Qt program that uses Qt Widgets. It constructs an application object
    // with argc command line arguments run in argv

    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "lab1_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            a.installTranslator(&translator);
            break;
        }
    }
    MainWindow w; // we create main application object
    // This is the object for which the wizard created the class and the UI file.
    // The user interface contains visual elements that are called widgets in Qt.
    // Examples of widgets are text edits, scroll bars, labels, and radio buttons.
    // A widget can also be a container for other widgets;
    // va dialog or a main application window, for example.
    w.show(); // we display it
    // The following line shows the mainWindow widget on the screen in its own window.
    // Widgets can also function as containers.
    // An example of this is QMainWindow which often contains several types of widgets.
    // Widgets are not visible by default; the function show() makes the widget visible.
    return a.exec(); // put app into loop where events in application are going to happen
    // The following line makes the QApplication enter its event loop.
    // When a Qt application is running,
    // events are generated and sent to the widgets of the application.
    // Examples of events are mouse presses and key strokes.
}
