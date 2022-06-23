#ifndef BLOGENTRY_H
#define BLOGENTRY_H

#include <QWidget>
#include <QJsonObject>
#include <QFile>
#include <QJsonDocument>

namespace Ui {
class blogEntry;
}

class blogEntry : public QWidget
{
    Q_OBJECT

public:
    explicit blogEntry(QWidget *parent = nullptr);
    ~blogEntry();
    void setUserId(const QString &userId);
    void setBlogId(const QString &blogId);
    void setUpBlogEntryFromJson(const QJsonObject &entry);


private slots:

private:
    void removeEntry();
    void enableEdition();
    void disableEdition();
    void saveEntryMethod();
    void enableEditing();
    void editEntry();
    void saveEditedEntry();
    void defineConnections() const;
    void editEntryClicked();
    void saveEntry(QJsonObject &blogEntryJson, QJsonObject &blogsFile);
    void saveItemToBlogEntryToBlogsFile(QJsonArray &items, QJsonObject &blogEntryJson, QJsonObject &blogsFile);
    void fillEntry(const QJsonObject &entry);

    int findEntry(const QJsonArray &items);

    QJsonArray removeEntryFromArray(const QJsonObject &blogEntryJson);
    QJsonArray addEdit(const QJsonObject &blogEntryJson);
    QJsonArray getItemsList();

    QJsonObject setDateTime(QJsonObject &entry);
    QJsonObject setEntry();

    Ui::blogEntry *ui;
    QString userId;
    QString blogId;
    QString dateTime;
    bool editMode;
};

#endif // BLOGENTRY_H
