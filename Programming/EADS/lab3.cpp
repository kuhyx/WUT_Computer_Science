// Krzysztof Rudnicki, 307585, lab3 EADS

#include <iostream>
#include <string>



template<typename Key, typename Info>
struct Node{
	Key key;
	Info info;
	int balanceFactor;
	Node<Key, Info>* left;
	Node<Key, Info>* right;
};

template<typename Key, typename Info>
class Dictionary{
private:

	Node<Key, Info>* root;
public:
	Dictionary();
	Node<Key, Info>* getRoot() const;
	void destroy(Node<Key, Info>* &someNode);
	~Dictionary();
	void copyDictionary(Dictionary *&copiedDictRoot, Dictionary *otherTreeRoot);
	Dictionary(const Dictionary &other);
	void insert(const Key &newKey, const Info &newInfo);
	void remove(const Key &keyToRemove);
	Info& search(const Key &keyToFind) const;
	void print() const;
	void insertAndPrint(const Key &newKey, const Info &newInfo);
	Dictionary& operator=(const Dictionary& otherDictionary);
};

void print(std::string s) 
{
	std::cout << s << std::endl;
}

template<typename Key, typename Info>
Dictionary<Key, Info>::Dictionary()
{
	root = nullptr;
}

template<typename Key, typename Info>
Node<Key, Info>* Dictionary<Key, Info>::getRoot() const
{
	return root;
}

template<typename Key, typename Info>
void Dictionary<Key, Info>::destroy(Node<Key, Info>* &someNode)
{
	if( someNode != nullptr)
	{
		destroy(someNode -> left);
		destroy(someNode -> right);
		delete someNode;
		someNode = nullptr;
	}
}

template<typename Key, typename Info>
Dictionary<Key, Info>::~Dictionary() { destroy(root); }

template<typename Key, typename Info>
void Dictionary<Key, Info>::copyDictionary(Dictionary* &copiedDictRoot, Dictionary* otherDictRoot)
{
	if(otherDictRoot == nullptr) copiedDictRoot = nullptr;
	else
	{
		copiedDictRoot = new Dictionary;
		copiedDictRoot->info = otherDictRoot -> info;
		copyDictionary(copiedDictRoot -> left, otherDictRoot -> left);
		copyDictionary(copiedDictRoot -> right, otherDictRoot -> right);
	}
}

template<typename Key, typename Info>
Dictionary<Key, Info>::Dictionary(const Dictionary &other)
{
	if(other.root == nullptr) root = nullptr;
	else copyTree(root, other.root);
}

template<typename Key, typename Info>
Dictionary<Key, Info>& Dictionary<Key, Info>::operator=(const Dictionary& otherDictionary)
{
	if(this != &otherDictionary)
	{
		if(root != nullptr) destroy(root);
		if(otherDictionary.root == nullptr) root = nullptr;
		else copyDictionary(root, otherDictionary.root);
	}
	return *this;
}

template<typename Key, typename Info>
void rotateToLeft(Node<Key, Info>* &root)
{
	Node<Key, Info>* p;
	if (root == nullptr) std::cerr << "Error in the tree" << std::endl;
	else if (root->right == nullptr)
		std::cerr << "Error in the tree:"
		<<" No right subtree to rotate." << std::endl;
	else
	{
		p = root->right;
		root->right = p->left; 
		p->left = root;
		root = p;
	}
}
	
template<typename Key, typename Info>
void rotateToRight(Node<Key, Info>* &root)
{
	Node<Key, Info> *p;
	if (root == NULL) std::cerr << "Error in the tree" << std::endl;
	else if (root-> left == NULL)
		std::cerr << "Error in the tree:"
		<< " No left subtree to rotate." << std::endl;
	else
	{
		p = root->left;
		root->left = p->right;
		p->right = root;
		root = p;
	}
}

template<typename Key, typename Info>
void balanceFromLeft(Node<Key, Info>* &root)
{
	Node<Key, Info> *p;
	Node<Key, Info> *w;
	p = root->left;
	switch (p->balanceFactor)
	{
		case -1:
		root->balanceFactor = 0;
		p->balanceFactor = 0;
		rotateToRight(root);
		break;
		case 0:
		std::cerr << "Error: Cannot balance from the left." << std::endl;
		break;
		case 1:
		w = p->right;
		switch (w->balanceFactor)
		{
			case -1:
				root->balanceFactor = 1;
				p->balanceFactor = 0;
			break;
			case 0:
				root->balanceFactor = 0;
				p->balanceFactor = 0;
			break;
			case 1:
				root->balanceFactor = 0;
				p->balanceFactor = -1;
		}
		w->balanceFactor = 0;
		rotateToLeft(p);
		root->left = p;
		rotateToRight(root);
	};
}

template<typename Key, typename Info>
void balanceFromRight(Node<Key, Info>* &root)
{
	Node<Key, Info> *p;
	Node<Key, Info> *w;
	p = root->right;
	switch (p->balanceFactor)
	{
		case -1:
		w = p->left;
		switch (w->balanceFactor)
		{
			case -1:
			root->balanceFactor = 0;
			p->balanceFactor = 1;
			break;
			case 0:
			root->balanceFactor = 0;
			p->balanceFactor = 0;
			break;
			case 1:
			root->balanceFactor = -1;
			p->balanceFactor = 0;
		}
		w->balanceFactor = 0;
		rotateToRight(p);
		root->right = p;
		rotateToLeft(root);
		break;
		case 0:
		std::cerr << "Error: Cannot balance from the left." << std::endl;
		break;
		case 1:
		root->balanceFactor = 0;
		p->balanceFactor = 0;
		rotateToLeft(root);
	}
}

template <typename Key, typename Info>
void insertIntoDict(Node<Key, Info>* &root, Node<Key, Info> *newNode, bool& isTaller)
{
	if (root == NULL)
	{
		root = newNode;
		isTaller = true;
	}
	else if (root->key == newNode->key) // if two nodes have the same key we replace one with another
	{
		root = newNode;
		isTaller = true;
	}
	else if (root->key > newNode->key) 
	{
		insertIntoDict(root->left, newNode, isTaller);
		if (isTaller) 
		switch (root->balanceFactor)
		{
			case -1:
				balanceFromLeft(root);
				isTaller = false;
			break;
			case 0:
				root->balanceFactor = -1;
				isTaller = true;
			break;
			case 1:
				root->balanceFactor = 0;
				isTaller = false;
		}
	}
	else
	{
		insertIntoDict(root->right, newNode, isTaller);
		if (isTaller) 
		switch (root->balanceFactor)
		{
			case -1:
				root->balanceFactor = 0;
				isTaller = false;
				break;
			case 0:
				root->balanceFactor = 1;
				isTaller = true;
				break;
			case 1:
				balanceFromRight(root);
				isTaller = false;
		}
	}
}

template<typename Key, typename Info>
Info& Dictionary<Key, Info>::search(const Key& keyToFind) const
{
	Node<Key, Info> *curr;
	bool found = 0;
	
	if(root == nullptr)
	{
		std::cerr << "cannot search if tree is empty" << std::endl;
	}else
	{
		curr = root;
		while(curr != nullptr && !found)
		{
			if( curr -> key == keyToFind) found = true;
			else if (curr -> key > keyToFind) curr = curr -> left;
			else curr = curr -> right;
		}
	}
	if(found) return curr -> info;
	else throw "Key not found";

}


template<typename Key, typename Info>
void printDict(const std::string& prefix, const Node<Key, Info>* node, bool isLeft)
{
    if( node != nullptr )
    {
        std::cout << prefix;

        std::cout << (isLeft ? "├──" : "└──" );

        // print the value of the node
        std::cout << "( " << node->info << ", " << node->key << ")" << std::endl;

        // enter the next tree level - left and right branch
        printDict( prefix + (isLeft ? "│   " : "    "), node->left, true);
        printDict( prefix + (isLeft ? "│   " : "    "), node->right, false);
    }
}

template<typename Key, typename Info>
void Dictionary<Key, Info>::print() const
{
	printDict("", root, false);
	std::cout << std::endl;
}


template <typename Key, typename Info>
void Dictionary<Key, Info>::insert(const Key &newKey, const Info &newInfo)
{
	bool isTaller = false;
	Node<Key, Info>* newNode;
	newNode = new Node<Key, Info>;
	newNode -> key = newKey;
	newNode->info = newInfo;
	newNode->balanceFactor = 0;
	newNode->left = NULL;
	newNode->right = NULL;
	insertIntoDict(root, newNode, isTaller);
}

template <typename Key, typename Info>
void Dictionary<Key, Info>::insertAndPrint(const Key &newKey, const Info &newInfo)
{
	insert(newKey, newInfo);
	print();
}

template <typename Key, typename Info>
Node<Key, Info>* minKeyNode(Node<Key, Info>* node)
{
	Node<Key, Info>* curr = node;
	while(curr -> left != nullptr) curr = curr -> left;
	return curr;
}

int max(int a, int b) { return ( a > b ? a : b ); }

template <typename Key, typename Info>
int height(Node<Key, Info>* root)
{
	if(root == nullptr) return 0;
	else return 1 + max(height(root -> left), height(root -> right));
}

template <typename Key, typename Info>
int getBalance(Node<Key, Info>* root)
{
	if(root == nullptr) return 0;
	return height(root -> left) - height(root -> right);
}


template <typename Key, typename Info>
Node<Key, Info>* deleteNode(Node<Key, Info>* root, const Key& keyToDelete)  
{  
    if (root == nullptr) return root;  
    if ( (root -> key) > keyToDelete) root->left = deleteNode(root->left, keyToDelete);  
    else if( (root -> key) < keyToDelete) root->right = deleteNode(root->right, keyToDelete);  
    else
    {  
        if( (root->left == nullptr) || (root->right == nullptr) )  
        {  
        	Node<Key, Info> *temp;
        	if(root -> left == nullptr) temp = root -> right;
        	else temp = root -> left;
            if (temp == nullptr)  
            {  
                temp = root;  
                root = nullptr;  
            }  
            else 
            {
            	*root = *temp; 
            	delete temp;  
            }
        }  
        else
        {  
            Node<Key, Info>* temp = minKeyNode(root->right);   
            root->key = temp->key;
            root->info = temp->info;  
            root->right = deleteNode(root->right, temp->key);  
        }  
    }    
    if (root == nullptr) return root;       
    int balance = getBalance(root);   
    if (balance > 1 && getBalance(root->left) >= 0) 
    {
    	rotateToRight(root);  
    	return root;
    }

    if (balance > 1 &&  getBalance(root->left) < 0)  
    {  
        rotateToLeft(root->left);  
        rotateToRight(root);  
        return root;
    }  
    
    if (balance < -1 && getBalance(root->right) <= 0)  
    {
        rotateToLeft(root);  
        return root;
    }
    
    if (balance < -1 && getBalance(root->right) > 0)  
    {  
        rotateToRight(root->right);  
        rotateToLeft(root);  
        return root;
    }  
  
    return root;  
}  

template<typename Key, typename Info>
void Dictionary<Key, Info>::remove(const Key& keyToRemove)
{
	deleteNode(root, keyToRemove);
}

bool testInsertEmpty()
{
	print("testInsertEmpty print:");
	Dictionary<std::string, int> marcel;
	marcel.print();
	return true;
}

bool testInsertOneElement()
{
	print("testInsertOneElement print:");
	Dictionary<std::string, int> marcel;
	marcel.insert("perception", 1);
	marcel.print();
	return true;
}

bool testInsertMoreElements()
{
	print("testInsertMoreElements print:");
	Dictionary<std::string, int> marcel;
	marcel.insertAndPrint("thank", 20);
	marcel.insertAndPrint("accept", 90);
	marcel.insertAndPrint("public", 30);
	marcel.insertAndPrint("rack", 8);
	marcel.insertAndPrint("pest", 10);
	return true;
}


bool testInsert()
{
	
	return testInsertEmpty()&&testInsertOneElement()&&testInsertMoreElements();
}

bool testSearchEmpty()
{
	Dictionary<std::string, int> marcel;
	try{ 
		 marcel.search("marcel"); 
	}
	catch  (char const* e) 
	{ 
		return true;
	};
	return false;
}


bool testSearchOneElement()
{
	Dictionary<std::string, int> marcel;
	marcel.insert("jungle", 20);
	if(marcel.search("jungle") != 20)
	{
		print("Error in testSearchOneElement");
		return 0;
	}
	return 1;
}

bool testSearchMoreElements()
{
	Dictionary<std::string, int> marcel;
	marcel.insert("thank", 20);
	marcel.insert("accept", 90);
	marcel.insert("public", 30);
	marcel.insert("rack", 8);
	marcel.insert("pest", 10);
	if(marcel.search("public") != 30)
	{
		print("Error in testSearchMoreElements");
		return 0;
	}
	return 1;
}

bool testSearch()
{
	return testSearchEmpty()&&testSearchOneElement()&&testSearchMoreElements();
}

bool testRemoveEmpty()
{
	Dictionary<std::string, int> marcel;
	marcel.remove("marcel");
	return true;
}

bool testRemove()
{
	return testRemoveEmpty();
}

bool tests()
{
	return testInsert()&&testSearch()&&testRemove();

}


int main()
{
	bool resultOfTests = tests();
	std::cout << "Result of tests is: " << resultOfTests << std::endl;
							
	return 1;
}
