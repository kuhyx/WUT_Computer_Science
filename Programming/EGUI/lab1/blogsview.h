#ifndef BLOGSVIEW_H
#define BLOGSVIEW_H

#include <QMainWindow>


namespace Ui {
class blogsView;
}

class blogsView : public QMainWindow
{
    Q_OBJECT

public:
    explicit blogsView(QWidget *parent = nullptr);
    ~blogsView();
    void setUserId(const QString &userId);
    void setBlogId(const QString &blogId);

private slots:
    void displayBlogEntries();
    void exit();

private:
    void defineConnections() const;
    void displayBlogEntriesLoop(const QJsonArray &blogEntries);
    void createNewBlogEntry();
    Ui::blogsView *ui;
    QString userId;
    QString blogId;
};

#endif // BLOGSVIEW_H
