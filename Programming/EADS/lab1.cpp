#include <iostream>
#include <vector>

template<typename Key, typename Info>
class Sequence{
	
	private: 
		struct Node{
			Key key;
			Info info;
			Node* next;
		};
		Node* head;
		
	public:
		Sequence();
		void destroySequence();
		~Sequence();
		void copySequence(const Sequence<Key, Info>& otherSequence);
		Sequence(const Sequence<Key, Info>& otherSequence);
		const Sequence<Key, Info>& operator=(const Sequence<Key, Info>& otherSequence);
		int length() const;
		void print() const;
		bool isEmpty() const;
		bool getKeyandInfoAt(const int position, Key& keyToReturn, Info& infoToReturn) const;
		void insertAtEnd(const Key& newKey, const Info& newInfo);		
		
};


template<typename Key, typename Info>
Sequence<Key, Info>::Sequence()
{
	head = nullptr;
}

template<typename Key, typename Info>
void Sequence<Key, Info>::destroySequence()
{
	Node* curr;
	while(head != nullptr)
	{
		curr = head;
		head = head->next;
		delete curr;
	}
}

template<typename Key, typename Info>
Sequence<Key, Info>::~Sequence()
{
	destroySequence();
}

template<typename Key, typename Info>
void Sequence<Key, Info>::copySequence(const Sequence<Key, Info>& otherSequence)
{
	if(head != nullptr) destroySequence();
	if(otherSequence.head == nullptr) head = nullptr;
	else
	{
		Node* curr = otherSequence.head;
		head = new Node();
		head -> key  = curr -> key;
		head -> info = curr -> info;
		head -> next = nullptr;
		curr = curr -> next;
		Node* nextNode;
		while(curr != nullptr)
		{
			nextNode = new Node();
			nextNode->key = curr->key;
			nextNode->info = curr->info;
			nextNode->next = nullptr;
			curr = curr -> next;
		}
	}
}

template<typename Key, typename Info>
Sequence<Key, Info>::Sequence(const Sequence<Key, Info>& otherSequence)
{
	head = nullptr;
	copySequence(otherSequence);
}

template<typename Key, typename Info>
const Sequence<Key, Info>& Sequence<Key, Info>::operator=(const Sequence<Key, Info>& otherSequence)
{
	if(this != &otherSequence)
	{
		copySequence(otherSequence);
	}
	return *this;
}



template<typename Key, typename Info>
int Sequence<Key, Info>::length() const
{
	Node* curr = head;
	int length = 0;
	while(curr != nullptr)
	{
		curr = curr->next;
		length++;
	}
	return length;
}

template<typename Key, typename Info>
void Sequence<Key, Info>::print() const
{
	Node* curr = head;
	int position = 0;
	if(head == nullptr) std::cout << "Sequence is empty" << std::endl;
	while(curr != nullptr) 
	{
		std::cout << "Inspecting element number: [" << position << "]" << std::endl;
		std::cout << "Key value is: [" << curr -> key << "]" << std::endl;
		std::cout << "Info value is: [" << curr -> info << "]" << std::endl;
		curr = curr -> next;
		position++;
	}
}

template<typename Key, typename Info>
bool Sequence<Key, Info>::isEmpty() const
{
	return length() == 0;
}

template<typename Key, typename Info>
bool Sequence<Key, Info>::getKeyandInfoAt(const int position, Key& keyToReturn, Info& infoToReturn) const
{
	Node* curr = head;
	int currentPosition = 0;
	while(curr != nullptr)
	{
		if(currentPosition == position)
		{
			infoToReturn = curr -> info;
			keyToReturn = curr -> key;
			return 1;
		}
		curr = curr -> next;
		currentPosition++;
	}
	return 0;
}

template<typename Key, typename Info>
void Sequence<Key, Info>::insertAtEnd(const Key& newKey, const Info& newInfo)
{
	Node* newNode = new Node();
	newNode -> key = newKey;
	newNode -> info = newInfo;
	newNode -> next = nullptr;
	if(head == nullptr) head = newNode;
	else
	{
		Node* curr = head;
		while(curr->next != nullptr) curr = curr->next;
		curr -> next = newNode;
	}
}

template<typename Key, typename Info>
bool addSingleSequence(const Sequence <Key, Info>& seq, int start, int dl, int limit, Sequence <Key, Info>& outputSequence)
{
	int elementsFromFirstSequence = start + dl;
	int lengthOfFirstSequence = seq.length();
	int outputSize = outputSequence.length();
	bool maxSize = 0;
	for(int i = start; i <= elementsFromFirstSequence && i <= lengthOfFirstSequence; i++)
	{
		Key newKey;
		Info newInfo;
		if(seq.getKeyandInfoAt(i, newKey, newInfo))
		{
			outputSequence.insertAtEnd(newKey, newInfo);
			outputSize++;
			if(outputSize >= limit)
			{
				maxSize = 1;
				break;
			}
		}


	}
	return maxSize;
}

template<typename Key, typename Info>
Sequence<Key, Info> produce(
				const Sequence <Key, Info>& seq1, int start1, int dl1,
				const Sequence <Key, Info>& seq2, int start2, int dl2,
				int limit)
{
	Sequence<Key, Info> newSequence;
	bool maxSize = addSingleSequence(seq1, start1, dl1, limit, newSequence);

	if(maxSize) return newSequence;
	else addSingleSequence(seq2, start2, dl2, limit, newSequence);
	return newSequence;


}

bool testingTwoEmpty()
{
	Sequence<int, int> empty1;
	Sequence<int, int> empty2;
	Sequence<int, int> outputSequence = produce(empty1, 0, 1, empty2, 0, 1, 5);
	if(!outputSequence.isEmpty())
	{
		outputSequence.print();
		std::cerr << "testingTwoEmpty()" << std::endl;
		return 0;
	}
	return 1;
}

bool testingOneEmpty()
{
	Sequence<int, int> empty1;
	Sequence<int, int> notEmpty;
	notEmpty.insertAtEnd(1, 2);
	notEmpty.insertAtEnd(3, 4);
	notEmpty.insertAtEnd(5, 6);
	Sequence<int, int> outputSequence = produce(empty1, 0, 1, notEmpty, 0, 4, 5);
	std::vector <int> keys(3);
	std::vector <int> infos(3);
	outputSequence.getKeyandInfoAt(0, keys.at(0), infos.at(0));
	outputSequence.getKeyandInfoAt(1, keys.at(1), infos.at(1));
	outputSequence.getKeyandInfoAt(2, keys.at(2), infos.at(2));
	if(keys.at(0) != 1 || keys.at(1) != 3 || keys.at(2) != 5 || 
	infos.at(0) != 2 || infos.at(1) != 4 || infos.at(2) != 6)
	{
		outputSequence.print();
		std::cerr << "testingOneEmpty()" << std::endl;
		return 0;
	}
	return 1;
}

bool testingFirstOverLimit()
{
	Sequence<int, int> overLimit;
	Sequence<int, int> shouldntMatter; 
	overLimit.insertAtEnd(1, 2);
	overLimit.insertAtEnd(3, 4);
	overLimit.insertAtEnd(5, 6);
	overLimit.insertAtEnd(7, 9);
	overLimit.insertAtEnd(9, 10);
	shouldntMatter.insertAtEnd(100, 200);
	Sequence<int, int> outputSequence = produce(overLimit, 0, 5, shouldntMatter, 0, 1, 4);
	if(outputSequence.length() != 4)
	{
		outputSequence.print();
		std::cerr << "testingFirstOverLimit()" << std::endl;
		return 0;
	}				
	return 1;
}

bool testingSecondOverLimit()
{
	Sequence<int, int> empty;
	Sequence<int, int> overLimit; 
	overLimit.insertAtEnd(1, 2);
	overLimit.insertAtEnd(3, 4);
	overLimit.insertAtEnd(5, 6);
	overLimit.insertAtEnd(7, 9);
	overLimit.insertAtEnd(9, 10);
	Sequence<int, int> outputSequence = produce(empty, 0, 2, overLimit, 0, 5, 4);
	if(outputSequence.length() != 4)
	{
		outputSequence.print();
		std::cerr << "testingSecondOverLimit()" << std::endl;
		return 0;
	}				
	return 1;
}

bool testingTooBigStart()
{
	Sequence<int, int> tooSmall;
	Sequence<int, int> shouldntMatter;
	tooSmall.insertAtEnd(1, 2);
	tooSmall.insertAtEnd(3, 4);
	tooSmall.insertAtEnd(5, 6);
	Sequence<int, int> outputSequence = produce(tooSmall, 4, 5, shouldntMatter, 1, 0, 5);
	if(!outputSequence.isEmpty())
	{
		outputSequence.print();
		std::cerr << "testingTooBigStart()" << std::endl;
		return 0;
	}
	return 1;
}

bool testingTooBigLength()
{
	Sequence<int, int> tooShort;
	Sequence<int, int> shouldntMatter;
	tooShort.insertAtEnd(1, 2);
	tooShort.insertAtEnd(3, 4);
	tooShort.insertAtEnd(5, 6);
	Sequence<int, int> outputSequence = produce(tooShort, 0, 6, shouldntMatter, 1, 0, 7);
	if(outputSequence.length() != 3)
	{
		outputSequence.print();
		std::cerr << "testingTooBigLength()" << std::endl;
		return 0;
	}
	return 1;
}

bool testingNormal()
{
	Sequence<int, int> normal1;
	Sequence<int, int> normal2;
	normal1.insertAtEnd(1, 2);
	normal1.insertAtEnd(3, 4);
	normal2.insertAtEnd(5, 6);
	Sequence<int, int> outputSequence = produce(normal1, 0, 2, normal2, 0, 1, 3);	
	std::vector <int> keys(3);
	std::vector <int> infos(3);
	outputSequence.getKeyandInfoAt(0, keys.at(0), infos.at(0));
	outputSequence.getKeyandInfoAt(1, keys.at(1), infos.at(1));
	outputSequence.getKeyandInfoAt(2, keys.at(2), infos.at(2));
	if(keys.at(0) != 1 || keys.at(1) != 3 || keys.at(2) != 5 || 
	infos.at(0) != 2 || infos.at(1) != 4 || infos.at(2) != 6)
	{
		outputSequence.print();
		std::cerr << "testingNormal()" << std::endl;
		return 0;
	}
	return 1;
}

bool tests()
{
	return testingTwoEmpty()&&testingOneEmpty()&&testingFirstOverLimit()&&
	testingSecondOverLimit()&&testingTooBigStart()&&testingTooBigLength()&&testingNormal();
	
}
int main()
{
	std::cout << "Result of tests: " << tests() << std::endl;
	return 0;
}