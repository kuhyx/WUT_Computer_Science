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
		static bool findNodeFrom(treeNode* curr, treeNode*& nodeToFound, int givenKey);
		int sumNodeSub(const treeNode* start);
};

int Tree::sumNodeSub(const treeNode* start)
{
    // Without this the recursion has no base case and walks off the end of
    // the tree; the declaration/definition const mismatch meant the body was
    // never compiled, so it was never reached either.
    if (start == nullptr) return 0;
    return (sumNodeSub(start->right) 
	+ sumNodeSub(start->left) 
	+ start->key);
}

// As submitted this did not compile: it called findNode on a treeNode*, which
// is a Tree method, and its while loop never advanced curr so it could not
// have terminated either. Same intent -- search the tree for a key -- expressed
// as the recursion the original was reaching for.
bool Tree::findNodeFrom(treeNode* curr, treeNode*& nodeToFound, int givenKey)
{
	if(curr == nullptr) return 0;
	if(curr -> key == givenKey)
	{
		nodeToFound = curr;
		return 1;
	}
	if(findNodeFrom(curr -> left, nodeToFound, givenKey)) return 1;
	return findNodeFrom(curr -> right, nodeToFound, givenKey);
}

bool Tree::findNode(treeNode*& nodeToFound, int givenKey)
{
	return findNodeFrom(root, nodeToFound, givenKey);
}


bool Tree::checkKeys(int key)
{
    treeNode* start;
    if (!findNode(start, key)) return 0;  
	// if we did not find the node we cannot compare the keys of it's left and right subtrees
    return (sumNodeSub(start->left) > sumNodeSub(start->right));
}