#include "blogentry.h"
#include "ui_blogentry.h"
#include "universalFunctions.h"
#include <QDateTime>
#include <QJsonObject>
#include <QFile>
#include <QJsonDocument>
#include <QJsonArray>

blogEntry::blogEntry(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::blogEntry)
{
    editMode = false;
    ui->setupUi(this);
    ui -> editEntryButton -> setDisabled(true);
    defineConnections();
}


void blogEntry::disableEdition()
{
    ui -> textEdit -> setReadOnly(true);
    ui -> lineEdit -> setReadOnly(true);
}

void blogEntry::enableEdition()
{
    ui -> textEdit -> setReadOnly(false);
    ui -> lineEdit -> setReadOnly(false);
}


void blogEntry::defineConnections() const
{
    connect(ui -> pushButton, &QPushButton::clicked, this, &blogEntry::removeEntry);
    connect(ui -> editEntryButton, &QPushButton::clicked, this, &blogEntry::editEntryClicked);
    connect(ui -> saveEntry, &QPushButton::clicked, this, &blogEntry::saveEntryMethod);
}

void blogEntry::fillEntry(const QJsonObject &entry)
{
    ui -> lineEdit -> setText(entry["title"].toString());
    ui -> textEdit -> setText(entry["content"].toString());
    ui -> dateTime -> setText(entry["datetime"].toString());
    ui -> ownerID -> setText("Owner ID: " + userId);
}

void blogEntry::setUpBlogEntryFromJson(const QJsonObject &entry)
{
    dateTime = entry["datetime"].toString();
    fillEntry(entry);
    disableEdition();
    enableEditing();
}

blogEntry::~blogEntry()
{
    delete ui;
}

void blogEntry::setUserId(const QString &userId)
{
    qDebug() << "blogEntry id: " << userId;
    this->userId = userId;
    ui -> ownerID -> setText("Owner ID: " + userId);
}

void blogEntry::setBlogId(const QString &blogId)
{
    this->blogId = blogId;
}

QJsonObject blogEntry::setDateTime(QJsonObject &entry)
{
    QString Time = QTime::currentTime().toString();
    QString Date = QDate::currentDate().toString();
    entry["datetime"] = Time + " " + Date;
    dateTime = Time + " " + Date;
    ui -> dateTime -> setText( Time + " " + Date);
    return entry;
}

void blogEntry::enableEditing()
{
    ui -> saveEntry -> setDisabled(true);
    ui -> editEntryButton -> setDisabled(false);
}

QJsonObject blogEntry::setEntry()
{
    QJsonObject entry;
    entry["title"] = ui -> lineEdit -> text();

    entry = setDateTime(entry);

    entry["content"] = ui -> textEdit -> toPlainText();
    return entry;
}

void blogEntry::saveEntryMethod()
{
    disableEdition();

    QJsonObject blogsFile = readJsonFile("blogs.json");
    QJsonObject blogEntryJson = blogsFile[blogId].toObject();
    QJsonObject entry = setEntry();

    QJsonArray items = blogEntryJson["items"].toArray();
    items.append(entry);
    saveItemToBlogEntryToBlogsFile(items, blogEntryJson, blogsFile);
    enableEditing();
}

int blogEntry::findEntry(const QJsonArray &items)
{
    int i = 0;
    for(i = 0; i < items.size(); i++)
    {
        QJsonObject currentItem = items[i].toObject();
        if(currentItem["datetime"].toString() == dateTime)
        {
            return i;
        }
    }
    return -1;
}

QJsonArray blogEntry::removeEntryFromArray(const QJsonObject &blogEntryJson)
{

    QJsonArray items = blogEntryJson["items"].toArray();
    int entryI = findEntry(items);
    if(entryI == -1)
    {
        return items;
    }
    items.removeAt(entryI);
    return items;
}

void blogEntry::removeEntry()
{
    QJsonObject blogsFile = readJsonFile("blogs.json");
    QJsonObject blogEntryJson = blogsFile[blogId].toObject();
    QJsonArray items = removeEntryFromArray(blogEntryJson);
    saveItemToBlogEntryToBlogsFile(items, blogEntryJson, blogsFile);
    this -> ~blogEntry();
}

void blogEntry::editEntry()
{
    editMode = true;
    enableEdition();
    ui -> saveEntry -> setDisabled(true);
    ui -> editEntryButton -> setText("Save edit");
}

QJsonArray blogEntry::addEdit(const QJsonObject &blogEntryJson)
{
    QJsonArray items = blogEntryJson["items"].toArray();

    for(int i = 0; i < items.size(); i++)
    {
        QJsonObject currentItem = items[i].toObject();
        if(currentItem["datetime"].toString() == dateTime)
        {
            currentItem["title"] = ui -> lineEdit -> text();
            currentItem["content"] = ui -> textEdit -> toPlainText();
            items.removeAt(i);
            items.append(currentItem);
            break;
        }
    }
    return items;
}

void blogEntry::saveItemToBlogEntryToBlogsFile(QJsonArray &items, QJsonObject &blogEntryJson, QJsonObject &blogsFile)
{
    blogEntryJson.insert("items", items);
    blogsFile.insert(blogId, blogEntryJson);
    saveJsonFile(blogsFile, "blogs.json");
}

void blogEntry::saveEntry(QJsonObject &blogEntryJson, QJsonObject &blogsFile)
{
    QJsonArray items = addEdit(blogEntryJson);
    saveItemToBlogEntryToBlogsFile(items, blogEntryJson, blogsFile);
}

void blogEntry::saveEditedEntry()
{
    disableEdition();
    editMode = false;
    ui -> editEntryButton -> setText("Edit Entry");
    QJsonObject blogsFile = readJsonFile("blogs.json");
    QJsonObject blogEntryJson = blogsFile[blogId].toObject();
    saveEntry(blogEntryJson, blogsFile);

}

void blogEntry::editEntryClicked()
{
    if(!editMode) editEntry();
    else saveEditedEntry();
}

