#include <stdio.h> // printf()
#include <unistd.h> // fork()
#include <time.h> // clock()
#include <stdlib.h> // malloc() 
#include <signal.h> // sigaction(), SIGTERM
#include <sys/wait.h> // wait()
#define WITH_SIGNALS 
const int NUM_CHILD = 5;
int KEYBOARD_INTERRUPT_MARK = 0;


void ourOwnSigTermHandler()
{
	printf("Process: %d was terminated\n", getpid());
}

void childProcessAlgorithm()
{
	#ifdef WITH_SIGNALS
	// 3.a in the child process
        struct sigaction ignoreSignal;
        ignoreSignal.sa_handler = SIG_IGN;
       	sigaction(SIGTERM, &ignoreSignal, NULL); // ignore handling of the
	// keyboard interrupt signal
	struct sigaction sigTermHandler;
	sigTermHandler.sa_handler = ourOwnSigTermHandler;
	// set own handler of the sigterm signal, which will only
	// print a message of the termination of this process
	sigaction(SIGTERM, &sigTermHandler, NULL);
	#endif
	printf("Process identifier of parent process: %d \n", getppid());
	// print process identifier of the parent process
	sleep(10); // sleep for 10 seconds
	printf("Execution for child: %d complete! \n", getpid());
	// print a message about execution completion
	exit(0); // !exit from process!
}


void sendSIGTERMsignal(pid_t *children)
{
	for(int i = 0; i < NUM_CHILD; i++) // go through each child
	{
		kill(children[i], SIGTERM); // and send sigterm signal using kill
	}
}

void createChildProcesses(pid_t *children)
{
	kill(-2, SIGTERM);
	for(int i = 0; i < NUM_CHILD; i++) // Create NUM_CHILD child processes
	{
		children[i] = fork(); // use the fork() function
		#ifdef WITH_SIGNALS
		// 3.c check the mark which may be set by the keyboard interrupt
		// handler
		if(KEYBOARD_INTERRUPT_MARK)
		{
			printf("interrupt of the creation process");
			// print a message about interrupt of the creation
			// process
			printf(" during creation of children[");
			printf("%d] = %d\n", i, children[i]);	
			sendSIGTERMsignal(children);
			// signal all just created processes with the sigterm
			return;
		}
		#endif
		if(children[i] == 0) childProcessAlgorithm(); // child algorithm
		else 
		{
			printf("fork for child[%d] failed! \n", i);
			kill(-2, SIGTERM); // -2 means that sigterm will be 
			// sent to every process in the process group
			// whose id is -2
		}
		sleep(1); // insert one second delays between fork calls
	}
}

int childProcessCorrect(const pid_t child)
{
	return child >= 0; // -1 would mean that we could not create the child
}

int correctChildProcesses(const pid_t *children)
{
	for(int i = 0; i < NUM_CHILD; i++) // go through each child
	{
		if(!childProcessCorrect(children[i])) // check if it was created correctly
		{
			printf("children[%d] = %d", i, children[i]); 
			// print approrpriate message that child was not created
			// correctly
			printf(", Was NOT declared correctly!\n");
			return 0;
		}
	}
	return 1;
}


void printCreationOfAllChildProcesses(const pid_t *children)
{
	// print a message about creation of all child processes
	for(int i = 0; i < NUM_CHILD; i++)
	{
		printf("Process children[%d] = %d created \n", i, children[i]);
	}
}

void terminateChildren(pid_t *children)
{
	int childTerminations = 0;
	for(int i = 0; i < NUM_CHILD; i++)
	{
		pid_t waitValue = wait(NULL); // call wait in loop
		if(waitValue != -1)
		{
			childTerminations++;
			// 2.4 count child processes terminations
			printf("Number of child processes terminations:");
			printf(" %d \n", childTerminations);
		}else
		{
			printf("Termination of the child %d", getpid());
			printf(" went wrong!\n");
		}
	}
	// 2.4 print a message that there are no more child processes
	printf("There are no more child processes \n");
	printf("Number of received child processes exit codes:");
	printf(" %d \n", childTerminations);
	// 2.4 priinta message with the number of just received child processes
	// exit codes
}

int noSignalsVersion()
{
        pid_t *children = malloc(sizeof(pid_t) * NUM_CHILD); 
	// allocate space for all children
        
	createChildProcesses(children); // create NUM_CHILD child processes
	if(!correctChildProcesses(children)) 
	{
		sendSIGTERMsignal(children); // if not send sigterm signals
                return 1;                                                       
        }                                                                       
        printCreationOfAllChildProcesses(children);
	terminateChildren(children);                                            
        return 0;                   
}


void ourOwnKeyboardInterrupt()
{
	printf("Received keyboard interrupt \n");
	KEYBOARD_INTERRUPT_MARK = 1;
}

int signalsVersion()
{
	struct sigaction ignoreSignals;
	ignoreSignals.sa_handler = SIG_IGN;
	for(int i = 0; i < _NSIG; i++) // 3.a Go through every single possible signal
	{
		sigaction(i, &ignoreSignals, NULL); // 3.a and ignore it
	}

	ignoreSignals.sa_handler = SIG_DFL; // Restore to default handler
	sigaction(SIGCHLD, &ignoreSignals, NULL); // 3.a the sigchld signal
	struct sigaction ownKeyboardInterrupt; // 3.b used to set our own
	// keyboard interrupt
	ownKeyboardInterrupt.sa_handler = ourOwnKeyboardInterrupt; 
	// 3.c this function just prints info about receiving keyboard
	// interrupt and sets keyboard interrupt occurance global variable
	sigaction(SIGINT, &ownKeyboardInterrupt, NULL);
	// 3.c set it so that interruption by default uses ownKeyboardInterrupt
	pid_t *children = malloc(sizeof(pid_t) * NUM_CHILD);
	// allocate memory for children
	createChildProcesses(children);
	if(!correctChildProcesses(children))
	{
		sendSIGTERMsignal(children);
		return 1;
	}
	printCreationOfAllChildProcesses(children);
	terminateChildren(children);
	struct sigaction restoreSignals;
	ignoreSignals.sa_handler = SIG_DFL;
	for(int i = 0; i < _NSIG; i++) 
	{
		// old service handlers of all signals should be restored
		sigaction(i, &restoreSignals, NULL); 
	}
	return 0;
}

int main()
{
	#ifndef WITH_SIGNALS
	printf("Entering NO signals version! \n");
	return noSignalsVersion();
	#endif
	#ifdef WITH_SIGNALS
	printf("Entering signals version! \n");
	signalsVersion();
	return 0;
	#endif
}
