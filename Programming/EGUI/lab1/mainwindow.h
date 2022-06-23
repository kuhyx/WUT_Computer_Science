#ifndef MAINWINDOW_H // make sure that header is not loaded more than once
#define MAINWINDOW_H

#include <QMainWindow> // Provide main application window in wchich user interface is build
// We can add more functionality using #include <Q...>
#include <QJsonObject>


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; } // we are saying that we want to use standard ui namespace
// tied to our UI file "mainwindow.ui"
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT // base class for all qt objects we work with
    // The class declaration contains the Q_OBJECT macro.
    // It must come first in the class definition, and declares our class as a QObject.
    // Naturally, it must also inherit from QObject.
    // A QObject adds several abilities to a normal C++ class.
    // Notably, the class name and slot names can be queried at runtime.
    // It is also possible to query a slot's parameter types and invoke it.

public:
    MainWindow(QWidget *parent = nullptr); // constructor, we pass nullptr so no parents
    // (top-level widget)
    ~MainWindow(); // destructor, free resources

private slots:


private:
    void newDocument() const;
    void open() const;
    void saveRegisteredUser();
    void goToLogin();
    void defineConnections() const;
    void registerUser(QJsonObject &users, QJsonObject &blogs, const QString &blogId, const QString &id);
    QJsonObject createUserObject(const QString &mail, const QString &password, const QString &userId) const;
    QJsonObject createBlogObject(const QString &id, const QString &ownerId) const;
    void exit() const;
    QJsonObject insertUserObject(QJsonObject &users, const QString &id);
    void saveFiles(QJsonObject &users, QJsonObject &blogs);
    QJsonObject insertBlogObject(QJsonObject &blogs, const QString &blogId, const QString &ownerId);
    Ui::MainWindow *ui; // we point to ui class "mainwindow.ui"
};
#endif // MAINWINDOW_H
