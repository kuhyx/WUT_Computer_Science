#include <iostream>

using namespace std;

template <typename Key, typename Info>
class Ring
{
private:
    struct Node
    {
        Key key;
        Info info;
        Node *prev;
        Node *next;
    };
    Node *head;

public:
    class Iterator
    {
    private:
        Node *ptr;
        Node *headPtr;
        Iterator(Node*);
        friend class Ring<Key, Info>;
    public:
        Iterator();
        Iterator(Ring);
        Info getInfo();
        Key getKey();
        void printData(int);
        Info operator*();
        Iterator& operator++();//prefix
        Iterator operator++(int);//postfix
        Iterator& operator--();//prefix
        Iterator operator--(int);//postfix
        bool operator==(const Iterator&);
        bool operator!=(const Iterator&);
        bool isFirst();
        bool isLast();
    };

    Ring();
    ~Ring();
    void insertAtBeginning(const Key& k, const Info& inf);
    void insertAtEnd(const Key& k, const Info& inf);
    void removeAtBeginning();
    void removeAtEnd();
    void clear();

    void printContent();
    void printContentReverse();

    Iterator begin();
    Iterator end();
};

//main function
int main()
{
    //test 1 - printing

    Ring<char, string> ring;

    ring.insertAtEnd('a', "letter 1");
    ring.insertAtEnd('b', "letter 2");
    ring.insertAtEnd('c', "letter 3");
    ring.insertAtEnd('d', "letter 4");
    ring.insertAtEnd('e', "letter 5");

    cout << "Normal print:" << endl;
    ring.printContent();

    Ring<char, string>::Iterator *ringIt = new Ring<char, string>::Iterator(ring);

    cout << endl << "Iterator print:" << endl;
    int number = 0;
    while (ringIt->isLast() == false)
    {
        ringIt->printData(number);

        number++;
        ++ringIt;
    }


    return 0;
}

//------------------------------Ring functions

template <typename Key, typename Info>
Ring<Key, Info>::Ring()
{
    head = nullptr;
}

template <typename Key, typename Info>
Ring<Key, Info>::~Ring()
{
    clear();
}

template <typename Key, typename Info>
void Ring<Key, Info>::insertAtBeginning(const Key& k, const Info& inf)
{
    if (head == nullptr)
    {
        Node *newNode = new Node();
        newNode->key = k;
        newNode->info = inf;
        newNode->next = newNode;
        newNode->prev = newNode;

        head = newNode;

        return;
    }

    Node *last = head->prev;

    Node *newNode = new Node();
    newNode->key = k;
    newNode->info = inf;
    newNode->prev = last;
    last->next = newNode;

    newNode->next = head;
    head->prev = newNode;

    head = newNode;
}

template <typename Key, typename Info>
void Ring<Key, Info>::insertAtEnd(const Key& k, const Info& inf)
{
    if (head == nullptr)
    {
        Node *newNode = new Node();
        newNode->key = k;
        newNode->info = inf;
        newNode->next = newNode;
        newNode->prev = newNode;

        head = newNode;

        return;
    }

    Node *last = head->prev;

    Node *newNode = new Node();
    newNode->key = k;
    newNode->info = inf;

    newNode->prev = last;
    last->next = newNode;

    newNode->next = head;
    head->prev = newNode;
}

template <typename Key, typename Info>
void Ring<Key, Info>::removeAtBeginning()
{
    if (head == nullptr)
        return;

    if (head->next == head)
    {
        delete head;
        head = nullptr;

        return;
    }

    Node *prev = head->prev;
    Node *next = head->next;

    prev->next = next;
    next->prev = prev;

    delete head;
    head = next;
}

template <typename Key, typename Info>
void Ring<Key, Info>::removeAtEnd()
{
    if (head == nullptr)
        return;

    if (head->next == head)
    {
        delete head;
        head = nullptr;

        return;
    }

    Node *prev = head->prev->prev;
    //Node *next = head;

    delete head->prev;

    prev->next = head;
    head->prev = prev;
}

template <typename Key, typename Info>
void Ring<Key, Info>::clear()
{
    while (head != nullptr)
        removeAtEnd();
}

template <typename Key, typename Info>
void Ring<Key, Info>::printContent()
{
    if (head == nullptr)
        return;

    Node *current = head;
    int number = 0;

    do
    {
        cout << number << "# - Key: " << current->key << ", Info: " << current->info << endl;

        number++;
        current = current->next;
    } while (current != head);
}

template <typename Key, typename Info>
void Ring<Key, Info>::printContentReverse()
{
    if (head == nullptr)
        return;


    if (head->next == head)
    {
        cout << "0# - Key: " << head->key << ", Info: " << head->info << endl;
    }

    Node *current = head->prev;
    int number = 0;

    do
    {
        cout << number << "# - Key: " << current->key << ", Info: " << current->info << endl;

        number++;
        current = current->prev;
    } while (current != head);
}

template <typename Key, typename Info>
typename Ring<Key, Info>::Iterator Ring<Key, Info>::begin()
{
    Ring<Key, Info>::Iterator tempIter = new Ring<Key, Info>::Iterator(head);

    return tempIter;
}

template <typename Key, typename Info>
typename Ring<Key, Info>::Iterator Ring<Key, Info>::end()
{
    Ring<Key, Info>::Iterator tempIter = new Ring<Key, Info>::Iterator(head->prev);

    return tempIter;
}

//------------------------------Ring Iterator functions

template <typename Key, typename Info>
Ring<Key, Info>::Iterator::Iterator()
{
    ptr = nullptr;
    headPtr = nullptr;
}

template <typename Key, typename Info>
Ring<Key, Info>::Iterator::Iterator(Node* nodePtr)
{
    ptr = nodePtr;
    headPtr = nodePtr;
}

template <typename Key, typename Info>
Ring<Key, Info>::Iterator::Iterator(Ring<Key, Info> ring)
{
    ptr = ring.head;
    headPtr = ring.head;
}

template <typename Key, typename Info>
Info Ring<Key, Info>::Iterator::getInfo()
{
    if (ptr != nullptr)
        return ptr->info;
    else
        throw "Iterator was nullptr";
}

template <typename Key, typename Info>
Key Ring<Key, Info>::Iterator::getKey()
{
    if (ptr != nullptr)
        return ptr->key;
    else
        throw "Iterator was nullptr";
}

template <typename Key, typename Info>
void Ring<Key, Info>::Iterator::printData(int number)
{
    if (ptr != nullptr)
        cout << number << "# - Key: " << ptr->key << ", Info: " << ptr->info << endl;
    else
        cout << "Tried to print an empty iterator" << endl;
}

template <typename Key, typename Info>
Info Ring<Key, Info>::Iterator::operator*()
{
    if (ptr != nullptr)
        return ptr->info;
    else
        throw "Iterator was nullptr";
}

template <typename Key, typename Info>
typename Ring<Key, Info>::Iterator& Ring<Key, Info>::Iterator::operator++()
{
    if (ptr != nullptr && headPtr != nullptr && ptr->next != headPtr)
        ptr = ptr->next;

    return *this;
}

template <typename Key, typename Info>
typename Ring<Key, Info>::Iterator Ring<Key, Info>::Iterator::operator++(int)
{
    Ring<Key, Info>::Iterator incremented = *this;

    ++(*this);
    return incremented;
}

template <typename Key, typename Info>
typename Ring<Key, Info>::Iterator& Ring<Key, Info>::Iterator::operator--()
{
    if (ptr != nullptr && headPtr != nullptr && ptr != headPtr)
        ptr = ptr->prev;

    return *this;
}

template <typename Key, typename Info>
typename Ring<Key, Info>::Iterator Ring<Key, Info>::Iterator::operator--(int)
{
    Ring<Key, Info>::Iterator decremented = *this;

    --(*this);
    return decremented;
}

template <typename Key, typename Info>
bool Ring<Key, Info>::Iterator::operator==(const Ring<Key, Info>::Iterator& iter)
{
    if (ptr == iter->ptr)
        return true;
    else
        return false;
}

template <typename Key, typename Info>
bool Ring<Key, Info>::Iterator::operator!=(const Ring<Key, Info>::Iterator& iter)
{
    if (operator==(this))
        return false;
    else
        return true;
}


template <typename Key, typename Info>
bool Ring<Key, Info>::Iterator::isLast()
{
    cout << (ptr != nullptr) << " " << (headPtr != nullptr) << " " << (ptr->next == headPtr) << endl;
    if (ptr != nullptr && headPtr != nullptr && ptr->next == headPtr)
        return true;
    else
        return false;
}

template <typename Key, typename Info>
bool Ring<Key, Info>::Iterator::isFirst()
{
    if (ptr != nullptr && headPtr != nullptr && ptr == headPtr)
        return true;
    else
        return false;
}
