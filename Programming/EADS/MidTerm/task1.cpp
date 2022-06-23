// KRZYSZTOF RUDNICKI, 307585, task 1

class List
{
	private:
		struct Node{
			double key;
			Node* next;
		};
		Node* head;
		public:
		int insert(double newVal, double firstVal, double secondVal);
};

int List::insert(double newVal, double firstVal, double secondVal)
{
	Node* curr = head;

	if(head == nullptr) return 0; // we can't insert anything inside empty list
	if(curr->next == nullptr) return 0;  // we can't insert a node between two nodes if there is only one node
	if(curr->next->next == nullptr) // If there is exactly two nodes
	{
		if(head -> key == firstVal && head -> next -> key == secondVal)
		{
			Node* newNode = new Node();
			newNode -> key = newVal;
			newNode -> next = head -> next;
			head -> next = newNode; 
			return 1;
		}else return 0;
	}
	
	int insertions = 0;
	while(curr -> next != nullptr) // If there is three nodes or more
	{
		bool foundKeys = 0;
		if(curr -> key == firstVal && curr -> next -> key == secondVal)
		{
			Node* newNode = new Node();
			newNode -> key = newVal;
			newNode -> next = curr->next;
			curr -> next = newNode; 
			insertions++;
			foundKeys = 1;
			curr = newNode -> next; // If newVal == firstVal, then without this line we will have 
			// infintie loop, to counteract this we skip newly added node. 
		}
		if(!foundKeys) curr = curr -> next;
	}
	
	return insertions;
}

int main()
{
	return 0;
}