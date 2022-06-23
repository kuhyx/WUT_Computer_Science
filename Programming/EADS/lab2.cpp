// Krzysztof Rudnicki, 307585, EADS 2
#include <iostream>

void print(const std::string s)
{
	std::cout << s << std::endl;
}

template<typename Key, typename Info>
class Ring{
private:
	struct Node{
		Key key;
		Info info;
		Node* next;
		Node* prev;
	};
	Node* any;
public:

	class Iterator
	{
		private:
			Node* pNode;
		public:
			Iterator() { pNode = nullptr; }
			~Iterator() { pNode = nullptr; }
			Iterator(Node* ptr) : pNode(ptr) {}
			
			bool operator!=(const Iterator& other) const
			{
				return pNode != other.pNode;
			}

			Iterator& operator++()
			{
				pNode = pNode -> next;
				return *this;
			}
			
			Iterator operator++(int)
			{
				Iterator it = *this;
				pNode = pNode -> next;
				return it;
			}
			
				Iterator& operator--()
			{
				pNode = pNode -> prev;
				return *this;
			}
			
			Iterator operator--(int)
			{
				Iterator it = *this;
				pNode = pNode -> prev;
				return it;
			}

			Node& operator[](int index)
			{
				Node* indexedNode = pNode;
				for(int i = 0; i < index; i++)
				{
					indexedNode = indexedNode -> next;
				}
				return *indexedNode;
			}
			
			Node* operator->()
			{
				return pNode;
			}
			
			Node& operator*()
			{
				return *pNode;
			}
			
			bool operator==(const Iterator& other) const
			{
				return pNode == other.pNode;
			}
	};
	
	Ring();
	~Ring();
	void clearRing();
	void print() const;
	void addAtEnd(Key newKey, Info newInfo);
	int size() const;
	Iterator begin() const // I will treat "any" Node as a "begining" of a ring
	{
		return Iterator(any);
	}
	
	Iterator end() const  // I will treat a Node just before "any" node as an "end" of a ring
	{
		if(any == nullptr) return nullptr;
		return any -> prev;
	}
};

template<typename Key, typename Info>
Ring<Key, Info>::Ring()
{
	any = nullptr;
}

template<typename Key, typename Info>
void Ring<Key, Info>::clearRing()
{
	if(any == nullptr) return;
	Node* curr = any;
	Node* temp = any;
	do{
		temp = curr;
		curr = curr->next;
		delete temp;
	}while(curr != any);

	delete any;
}

template<typename Key, typename Info>
Ring<Key, Info>::~Ring()
{
	this -> clearRing();
}

template<typename Key, typename Info>
void Ring<Key, Info>::print() const
{
	Node* curr = any;
	do{
		std::cout << curr -> key << "; " << curr->info << std::endl;
		curr = curr->next;
	}while (curr != any);
}

template<typename Key, typename Info>
void Ring<Key, Info>::addAtEnd(Key newKey, Info newInfo)
{
	Node* newNode = new Node();
	newNode -> key = newKey;
	newNode -> info = newInfo;
	if(any == nullptr)
	{
		any = newNode;
		any -> next = any;
		any -> prev = any;
		return;
	}
	
	if(any -> next == nullptr)
	{
		any -> next = newNode;
		any -> prev = newNode;
		newNode -> next = any;
		newNode -> prev = any;
		return;
	}
	
	Node* curr = any;
	while(curr -> next != any) curr = curr -> next;
	any->prev = newNode;
	curr->next = newNode;
	newNode -> prev = curr;
	newNode -> next = any;
}

template<typename Key, typename Info>
int Ring<Key, Info>::size() const
{
	Node* curr = any;
	int size = 0;
	do{
		size++;
		curr = curr -> next;
	}while (curr != any);
	return size;
}

template <typename Key, typename Info>
void printPair(const Key key, const Info info)
{
	std::cout << "Key: " << key << "; Info: " << info << std::endl;
}

bool testForEmpty()
{
	Ring<int, int> marcel;
	Ring<int, int>::Iterator it = marcel.begin();
	if(it != nullptr)
	{
		 print("testForEmpty");
		return false;
	}
	return true;
}

bool testOneElement()
{
	Ring<int, int> marcel;
	marcel.addAtEnd(1, 1);
	Ring<int, int>::Iterator it = marcel.begin();
	if(it -> key != 1 || it -> info != 1)
	{
		print("testForwardIncrementingOneElement");
		return false;
	}
	return true;
}

bool testForwardIncrementing()
{
	Ring<int, int> marcel;
	marcel.addAtEnd(1, 1);
	marcel.addAtEnd(2, 2);
	marcel.addAtEnd(3, 3);
	marcel.addAtEnd(4, 4);
	marcel.addAtEnd(5, 5);
	int i = 0;
	for( Ring<int, int>::Iterator it = marcel.begin();
	it != marcel.end(); it++, i++)
	{
		if(it -> key != i + 1 || it -> info != i + 1)
		{
			print("testForwardIncrementingNormal");
			return false;
		}
	}
	if(marcel.end() -> key != 5 || marcel.end() -> info != 5)
	{
		print("testForwardIncrementingNormal");
		return false;
	}

	return true;
}

bool testBackwardDecrementing()
{
	Ring<int, int> marcel;
	marcel.addAtEnd(1, 1);
	marcel.addAtEnd(2, 2);
	marcel.addAtEnd(3, 3);
	marcel.addAtEnd(4, 4);
	marcel.addAtEnd(5, 5);
	int i = 0;
	for( Ring<int, int>::Iterator it = marcel.end();
	it != marcel.begin(); it++, i++)
	{
		if(it -> key != 5 - i || it -> info != 5 - i)
		{
			print("testBackwardDecrementing");
			return false;
		}
	}
	if(marcel.begin() -> key != 1 || marcel.begin() -> info != 1)
	{
		print("testBackwardDecrementing");
		return false;
	}

	return true;
}

bool testForwardSquareBracket()
{
	Ring<int, int> marcel;
	marcel.addAtEnd(1, 1);
	marcel.addAtEnd(2, 2);
	marcel.addAtEnd(3, 3);
	marcel.addAtEnd(4, 4);
	marcel.addAtEnd(5, 5);
	Ring<int, int>::Iterator it = marcel.begin();
	for(int i = 0; i < marcel.size(); i++)
	{
		if(it[i].key != i + 1 || it[i].info != i + 1)
		{
			print("testForwardSquareBracket");
			return false;
		}
	}
	return true;
}


bool testBackwardSquareBracket()
{
	Ring<int, int> marcel;
	marcel.addAtEnd(1, 1);
	marcel.addAtEnd(2, 2);
	marcel.addAtEnd(3, 3);
	marcel.addAtEnd(4, 4);
	marcel.addAtEnd(5, 5);
	Ring<int, int>::Iterator it = marcel.end();
	for(int i = marcel.size(); i > 0; i--)
	{
		if(it[i].key != i || it[i].info != i)
		{
			print("testBackwardSquareBracket");
			return false;
		}
	}
	return true;
}

bool testSquareBracketRandomOverflow()
{
	Ring<int, int> marcel;
	marcel.addAtEnd(1, 1);
	marcel.addAtEnd(2, 2);
	marcel.addAtEnd(3, 3);
	marcel.addAtEnd(4, 4);
	marcel.addAtEnd(5, 5);
	Ring<int, int>::Iterator it = marcel.begin();
	//Checking for some random places in ring:
	if(it[2].key != 3) 
	{
		print("testSquareBracketRandomOverflow");
		return false;
	}
	
	if(it[4].key != 5) 
	{
		print("testSquareBracketRandomOverflow");
		return false;
	}
	
	if(it[0].key != 1) 
	{
		print("testSquareBracketRandomOverflow");
		return false;
	}
	//Checking for overflow:
	if(it[10].key != 1) 
	{
		print("testSquareBracketRandomOverflow");
		return false;
	}
	return true;
}

bool tests()
{
	return testForEmpty()&&testOneElement()&&testForwardIncrementing()
	&&testBackwardDecrementing()&&testForwardSquareBracket()&&testBackwardSquareBracket()
	&&testSquareBracketRandomOverflow();
}

int main()
{
	std::cout << "Result of tests is: " << tests() << std::endl;
	return 1;
	
}