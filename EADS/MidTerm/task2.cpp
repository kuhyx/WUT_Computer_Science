// Krzysztof Rudnicki, 307585

struct treeNode
{
	int key;
	treeNode *left;
	treeNode *right;
};

class Tree{

	private:
		treeNode *root;
	public:
		bool checkKeys(int givenKey);
		bool findNode(treeNode*& nodeToFound, int givenKey);
		int sumNodeSub(treeNode* start);
};

int Tree::sumNodeSub(const treeNode* start)
{
    return (sumNodeSub(start->right) 
	+ sumNodeSub(start->left) 
	+ start->key);
}

bool Tree::findNode(treeNode*& nodeToFound, int givenKey);
{
	treeNode* curr = root;
	treeNode* Cleft = curr->left;
	treeNode* Cright = curr->right;
	while(curr != nullptr)
	{
		if(curr -> key == givenKey)
		{
			nodeToFound = curr;
			return 1;
		}else
		{
			if(Cleft.findNode(nodeToFound, givenKey)) return 1;
			if(Cright.findNode(nodeToFound, givenKey)) return 1;
		}
	}
	return 0;
}



bool Tree::checkKeys(int key)
{
    treeNode* start;
    if (!findNode(start, key)) return 0;  
	// if we did not find the node we cannot compare the keys of it's left and right subtrees
    return (sumNodeSub(start->left) > sumNodeSub(start->right));
}