// Krzysztof Rudnicki, 307585, task 3

template<typename Key>
class Ring{
	private:
		struct Node{
			Key key;
			Node* prev;
			Node* next;
		};
		Node* any;
public:
	bool removeNeighbours(const Key& givenKey);
};

template<typename Key>
bool Ring<Key>::removeNeighbours(const Key& givenKey)
{
	Node* curr = any;
	if(any == nullptr || any -> next == nullptr) return 0;
	// we can't remove 2 nodes if there is less than 2 nodes
	bool foundKey = 0;
	// we are interested in 5 nodes, lets call them, from left to right:
	// A; B; C; D; E
	// I will use this for comments
	// if C has a key then at the end we want to get:
	// A; C; E
	do{
		if(curr -> key == givenKey)
		{
			Node* temp = curr;
			curr -> prev -> prev -> next = curr;  
			// curr -> prev -> prev points to Node "A"
			// it used to point "next" to Node "B" which we are going to remove so it must
			// start to point to a new node in our case node "C"
			curr -> next -> next -> prev = curr;
			// curr -> next -> next points to Node "E"
			// it used to point "prev" to Node "D" which we are going to remove so it must
			// start to point to a new node in our case node "C"
			curr -> next = curr -> next -> next;
			// curr points to Node "C"
			// it used to point "next" to Node "D" which we are going to remove so it must
			// start to point to a new node in our case node "E"
			curr -> prev = curr -> prev -> prev;
			// curr points to Node "C"
			// it used to point "prev" to Node "B" which we are going to remove so it must
			// start to point to a new node in our case node "A"
			if(curr->prev == any || curr -> next == any) any = curr;
			// if any of the neighours that we are going to delete is "any", we must provide
			// the ring with a new "any" node
			delete temp->prev;
			// this way we will delete what USED to be curr->prev
			// temp->prev points to "B" node
			delete temp->next;
			// this way we will delete what USED to be curr->next
			// temp->next points to "D" node
			foundKey = 1;
		}
		curr = curr->next;
	}while(curr != any);
	return foundKey;
}