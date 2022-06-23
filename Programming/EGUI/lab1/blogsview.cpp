#include "universalFunctions.h"
#include "blogsview.h"
#include "ui_blogsview.h"
#include "blogentry.h"
#include "ui_blogentry.h"

#include <algorithm>
#include <QJsonObject>
#include <QFile>
#include <QJsonDocument>
#include <QJsonArray>

blogsView::blogsView(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::blogsView)
{
    ui->setupUi(this);
    defineConnections();
}

void blogsView::defineConnections() const
{
    connect(ui -> actionCreate_new_Blog_entry, &QAction::triggered, this, &blogsView::createNewBlogEntry);
    connect(ui -> actionExit, &QAction::triggered, this, &blogsView::exit);
}

blogsView::~blogsView()
{
    delete ui;
}

void blogsView::setUserId(const QString &userId)
{
    this->userId = userId;
}

void blogsView::setBlogId(const QString &blogId)
{
    qDebug() << "blog id before set: " << blogId;
    this->blogId = blogId;
    qDebug() << "blog id after set: " << this->blogId;
    displayBlogEntries();
}


void blogsView::createNewBlogEntry()
{
    blogEntry *e = new blogEntry();
    e -> setUserId(userId);
    e -> setBlogId(blogId);
    ui -> blogsLayout -> addWidget(e);
}

void blogsView::displayBlogEntriesLoop(const QJsonArray &blogEntries)
{
    for(int i = 0; i < blogEntries.size(); i++)
    {
        QJsonObject entry = (blogEntries.at(i)).toObject();
        createNewBlogEntry();
    }
}

void blogsView::displayBlogEntries()
{
    QJsonObject blogsFile = readJsonFile("blogs.json");
    QJsonObject userBlog = blogsFile[blogId].toObject();
    qDebug() << blogId;
    qDebug() << userBlog["blogId"].toString();
    QJsonArray blogEntries = userBlog["items"].toArray();
    displayBlogEntriesLoop(blogEntries);

}

 void blogsView::exit()
{
    QApplication::quit();
}


