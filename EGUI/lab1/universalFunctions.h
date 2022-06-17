#ifndef UNIVERSALFUNCTIONS_H
#define UNIVERSALFUNCTIONS_H

#include <QJsonObject>

QJsonObject readJsonFile(const QString title);
void saveJsonFile(QJsonObject &users, const QString name);
void outputMessageBox(const QString messageBoxText);
void exit();
bool stringEmpty(const QString &string, const QString &messageBoxMessage);
bool idExists(const QString &id, const QJsonObject &json, const QString &message, const bool &whenMessage);
bool sameString(const QString &stringToCompare, const QString &jsonId, const QJsonObject &json, const QString &message);

#endif // UNIVERSALFUNCTIONS_H
