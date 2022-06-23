#include <iostream>

struct list_node
{
    int value;
    list_node *next;

    list_node(int v, list_node* nxt = nullptr)
    {
        value = v;
        next = nxt;
    }
};

class list
{
    list_node *head;
    int listSize;
public:
    list()
    {
        head = nullptr;
        listSize = 0;
    }
    bool is_empty() const;
    int size() const;
    void push_front(int val);
    void pop_front();
    void clear();
    // removes first occurence of `val` in the list
    // returns true if removal occured
    bool remove(int val);
    list_node *get_head();
    void printValues() const;
};

bool list::is_empty() const
{
    return head == nullptr;
}

int list::size() const
{
    return listSize;
}

void list::push_front(int val)
{
     list_node *pNewNode = new list_node(val);
     pNewNode -> next = head;
     head = pNewNode;
     listSize++;
     return;
}

void list::pop_front()
{
    if(is_empty())
    {
        std::cout << "There are no elements to be popped!" << std::endl;
        return;
    }

    list_node *pTemp = head;
    pTemp = pTemp -> next;
    delete head;
    head = pTemp;
    listSize--;
    return;
}

void list::printValues() const
{
    if(head == nullptr)
    {
        std::cout << "There are no values to be printed!" << std::endl;
        return;
    }
    list_node *pNodes = head;
    int i = 1;
    while(pNodes)
    {
        std::cout << i << " value is: " << pNodes -> value << std::endl;
        pNodes = pNodes -> next;
        i++;
    }
    return;
}

void list::clear()
{
    if(head == nullptr)
    {
        std::cout << "The list is already empty! " << std::endl;
        return;
    }
    while(head) pop_front();
    listSize = 0;
    return;
}

bool list::remove(int val)
{
    list_node *current = head;
    list_node *previous = nullptr;
    bool valueFound = 0;
    while (current != nullptr)
    {
        if(current -> value == val)
        {
            valueFound = 1;
            break;
        }

        previous = current;
        current = current -> next;
    }

    if(!valueFound) return false;
    if(previous == nullptr) head = head -> next; // THIS ELEMENT IS FIRST ELEMENT
    else previous -> next = current -> next;
    delete current;
    listSize--;
    return true;
}

list_node *list::get_head()
{
    return head;
}

void printIsEmptyValue(list printedList)
{
    std::cout << "is_empty() method value: " << printedList.is_empty() << std::endl;
    return;
}

void isEmptyTest()
{
    std::cout << "TESTING is_empty() METHOD" << std::endl;
    list testIsEmpty;
    std::cout << "Testing for 0 elements" << std::endl;
    printIsEmptyValue(testIsEmpty);
    std::cout << "Testing for 1 element" << std::endl;
    testIsEmpty.push_front(1);
    printIsEmptyValue(testIsEmpty);
    std::cout <<"Testing after deleting 1 element" << std::endl;
    testIsEmpty.pop_front();
    printIsEmptyValue(testIsEmpty);
    return;
}

void printSize(list printList)
{
    std::cout << "Size of this list is: " << printList.size() << std::endl;
    return;
}

void sizeTest()
{
    std::cout << "TESTING size() METHOD" << std::endl;
    list testSize;
    std::cout << "Testing for empty list: " << std::endl;
    printSize(testSize);
    std::cout << "Testing for 1 element list: " << std::endl;
    testSize.push_front(1);
    printSize(testSize);
    std::cout << "Testing after removing one element from 1 element list: " << std::endl;
    testSize.pop_front();
    printSize(testSize);
    std::cout << "Testing for 5 elements list: " << std::endl;
    for(int i = 0; i < 5; i++) testSize.push_front(i);
    printSize(testSize);
    return;
}

void pop_frontTest()
{
    std::cout << "TESTING pop_front() METHOD" << std::endl;
    list testPopFront;
    std::cout << "Trying to pop empty list" << std::endl;
    testPopFront.pop_front();
    printIsEmptyValue(testPopFront);
    printSize(testPopFront);
    testPopFront.push_front(2137);
    std::cout << "Poping one element list" << std::endl;
    testPopFront.pop_front();
    printIsEmptyValue(testPopFront);
    printSize(testPopFront);
    std::cout << "Poping two element list" << std::endl;
    testPopFront.push_front(1);
    testPopFront.push_front(2);
    testPopFront.pop_front();
    printIsEmptyValue(testPopFront);
        printSize(testPopFront);
    testPopFront.printValues();
    return;
}

 void clearTest()
 {
     std::cout << "TESTING clear() METHOD" << std::endl;
     list testClear;
     std::cout << "Trying to clear empty list: " << std::endl;
     testClear.clear();
     printIsEmptyValue(testClear);
     printSize(testClear);
     testClear.printValues();
     std::cout << "Clearing one element list: " << std::endl;
     testClear.push_front(1);
     testClear.clear();
     printIsEmptyValue(testClear);
     printSize(testClear);
     testClear.printValues();
     std::cout << "Clearing two element list: " << std::endl;
     testClear.push_front(1);
     testClear.push_front(2);
     testClear.clear();
     printIsEmptyValue(testClear);
     printSize(testClear);
     testClear.printValues();
     std::cout << "Clearing five element list: " << std::endl;
     for(int i = 0; i < 5; i++) testClear.push_front(i);
     testClear.clear();
     printIsEmptyValue(testClear);
     printSize(testClear);
     testClear.printValues();
     return;
 }

 void printRemoveResult(list fromWhichRemove, int value)
 {
     if(fromWhichRemove.remove(value)) std::cout << "Removal of value: " << value << " Successful!" << std::endl;
     else std::cout << "Removal of value: " << value << " Failed! " << std::endl;
 }

 void removeTest()
 {
    std::cout << "TESTING remove() METHOD " << std::endl;
    list testRemove;
    std::cout << "Trying to remove element from empty list: " << std::endl;
    printRemoveResult(testRemove, 0);

    std::cout << "Trying to remove wrong element from 1 element list: " << std::endl;
    testRemove.push_front(1);
    printRemoveResult(testRemove, 2);
    std::cout << "Trying to remove right element from 1 element list: " << std::endl;
    testRemove.push_front(1);
    printRemoveResult(testRemove, 1);

    return;

 }

void getHeadTest()
{
    list testHead;
    std::cout << "Testing getHead for empty list: " << std::endl;
    std::cout << "getHead value: " << testHead.get_head() << std::endl;
    testHead.push_front(5);
    std::cout << "Testing getHead for non empty list: " << std::endl;
    std::cout << "getHead value: " << testHead.get_head() << std::endl;
    return;
}


void runTests()
{
    isEmptyTest();
    sizeTest();
    pop_frontTest();
    clearTest();
    removeTest();
    getHeadTest();
    return;
}

int main()
{
    runTests();
    return 0;
}
