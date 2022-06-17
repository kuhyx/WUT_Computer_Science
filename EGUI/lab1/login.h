#ifndef LOGIN_H
#define LOGIN_H

#include <QMainWindow>

namespace Ui {
class login;
}

class login : public QMainWindow
{
    Q_OBJECT

public:
    explicit login(QWidget *parent = nullptr);
    ~login();

private slots:

private:
    void loginUser();
    void loginSuccessful(const QString &id, const QString &blogId);
    void defineConnections() const;
    void goRegister();
    void exit() const;
    QString findCurrentBlogId(const QJsonObject &blogs, const QString &id);
    Ui::login *ui;
};

#endif // LOGIN_H
