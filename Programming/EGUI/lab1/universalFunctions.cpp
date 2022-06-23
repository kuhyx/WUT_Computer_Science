#ifndef UNIVERSAL_FUNCTIONS_CPP
#define UNIVERSAL_FUNCTIONS_CPP
#include <QJsonObject>
#include <QString>
#include <QJsonDocument>
#include <QFile>
#include <QMessageBox>
#include <QApplication>

QJsonObject readJsonFile(const QString title)
{
    QFile file(title);
    file.open(QIODevice::ReadWrite); // If the file does not exist we create it
    QByteArray bytes = file.readAll();
    file.close();
    QJsonDocument document = QJsonDocument::fromJson( bytes );
    return document.object();
}

void saveJsonFile(QJsonObject &users, const QString name)
{
    QFile jsonFile(name);
    QJsonDocument document;
    document.setObject( users );
    QByteArray bytes = document.toJson( QJsonDocument::Indented );
    jsonFile.open( QIODevice::WriteOnly | QIODevice::Text | QIODevice::Truncate );
    QTextStream iStream( &jsonFile );
    // iStream.setCodec( "utf-8" );
    iStream << bytes;
    jsonFile.close();
}

void outputMessageBox(const QString messageBoxText)
{
    QMessageBox idEmpty;
    idEmpty.setText(messageBoxText);
    idEmpty.exec();
}

void exit()
{
    QApplication::quit();
}

bool stringEmpty(const QString &string, const QString &messageBoxMessage)
{
    if(string == "")
    {
        outputMessageBox(messageBoxMessage);
        return true;
    }
    return false;
}

bool idExists(const QString &id, const QJsonObject &json, const QString &message, const bool &whenMessage)
{
    if (json.find(id) != json.end())
    {
        if (whenMessage) outputMessageBox(message);
        return true;
    }
    if (!whenMessage) outputMessageBox(message);
    return false;
}

bool sameString(const QString &stringToCompare, const QString &jsonId, const QJsonObject &json, const QString &message)
{
    if(json[jsonId].toString() != stringToCompare)
    {
        outputMessageBox(message);
        return false;
    }
    return true;
}

#endif
