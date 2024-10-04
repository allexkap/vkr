#define _GNU_SOURCE
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>


#define STACK_SIZE 8 * 1024 * 1024

#define panic(msg) fprintf(stderr, msg "\n"), exit(EXIT_FAILURE)
#define check(rt, msg)                                                         \
    if ((rt) < 0) {                                                            \
        perror(msg);                                                           \
        exit(EXIT_FAILURE);                                                    \
    }


void print_resuid() {
    uid_t ruid, euid, suid;
    int rt = getresuid(&ruid, &euid, &suid);
    if (rt < 0) panic("getresuid error");
    printf("real=%d; effective=%d; saved=%d\n", ruid, euid, suid);
}

int run_argv(void *arg) {
    print_resuid();
    char **argv = arg;
    return execvp(*argv, argv);
}


int main(int argc, char *argv[]) {
    if (argc < 2) panic("Not enough arguments");

    void *child_stack = malloc(STACK_SIZE) + STACK_SIZE;
    int clone_flags = SIGCHLD | CLONE_NEWUSER | CLONE_NEWUTS | CLONE_NEWIPC |
                      CLONE_NEWNS | CLONE_NEWPID | CLONE_NEWNET |
                      CLONE_NEWCGROUP;

    int pid = clone(run_argv, child_stack, clone_flags, argv + 1);
    if (pid < 0) panic("clone error");

    int status;
    waitpid(pid, &status, 0);

    printf("ok\n");
    return !WIFEXITED(status) || WEXITSTATUS(status);
}
