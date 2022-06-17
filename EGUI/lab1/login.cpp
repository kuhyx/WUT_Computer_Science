#include "login.h"
#include "ui_login.h"
#include "blogsview.h"
#include "mainwindow.h"
#include "universalFunctions.h"
#include <QFileDialog>
#include <QMessageBox>
#include <iostream>
#include <QJsonObject>
#include <QJsonDocument>
#include <QTextStream>

login::login(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::login)
{
    ui->setupUi(this);
    defineConnections();
}

login::~login()
{
    delete ui;
}

void login::defineConnections() const
{
    connect(ui -> loginButton, &QPushButton::clicked, this, &login::loginUser);
    connect(ui -> registerButton, &QPushButton::clicked, this, &login::goRegister);
    connect(ui -> actionExit, &QAction::triggered, this, &login::exit);
    connect(ui -> actionLogin, &QAction::triggered, this, &login::loginUser);
    connect(ui -> actionRegister, &QAction::triggered, this, &login::goRegister);
}

void login::exit() const
{
    QApplication::quit();
}


void login::goRegister()
{
    MainWindow *r = new MainWindow();
    r -> show();
    hide();
}

void login::loginSuccessful(const QString &id, const QString &blogId)
{
    qDebug() << "blog id: " << blogId;
    blogsView *b = new blogsView();
    b -> setUserId(id);
    b -> setBlogId(blogId);
    b -> show();
    hide();
}

QString login::findCurrentBlogId(const QJsonObject &blogs, const QString &id)
{
    QString currentBlogId = "";
    QStringList keys = blogs.keys();
    for(int i = 0; i < keys.size(); i++)
    {
        QJsonObject currentBlog = blogs[keys.at(i)].toObject();
        if(currentBlog["ownerId"] == id)
        {
            currentBlogId = (currentBlog.take("blogId")).toString();
            return currentBlogId;
            break;
        }
    }
    return "";
}


void login::loginUser()
{
    QJsonObject users = readJsonFile("user.json");
    QJsonObject blogs = readJsonFile("blogs.json");

    QString id = ui->inputLoginID_2->text();
    if (!idExists(id, users, "THIS USER ID DOES NOT EXIST!", false)) return;
    QString enteredPassword = ui->inputPassword->text();
    if (!sameString(enteredPassword, "password", users, "WRONG PASSWORD!")) return;


    QString currentBlogId = findCurrentBlogId(blogs, id);
    if (stringEmpty(currentBlogId, "COULD NOT FOUND BLOG ID FOR THIS LOGIN \n SOMETHING WENT TERRIBLY WRONG WITH JSON FILE!")) return;

    loginSuccessful(id, currentBlogId);
}
