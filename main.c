#define _GNU_SOURCE
#include <limits.h>
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mount.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <sys/wait.h>
#include <unistd.h>


#define STACK_SIZE 8 * 1024 * 1024

#define panic(msg) fprintf(stderr, msg "\n"), exit(EXIT_FAILURE)
#define check(rt, msg)                                                         \
    if ((rt) < 0) {                                                            \
        perror(msg);                                                           \
        exit(EXIT_FAILURE);                                                    \
    }


struct CloneParams {
    char **argv;
    int fd[2];
};


void print_resuid() {
    uid_t ruid, euid, suid;
    int rt = getresuid(&ruid, &euid, &suid);
    if (rt < 0) panic("getresuid error");
    printf("real=%d; effective=%d; saved=%d\n", ruid, euid, suid);
}

void write_and_check(const char *path, const char *text) {
    FILE *file = fopen(path, "w");
    if (!file) panic("fopen error");

    int len = fprintf(file, "%s", text);
    if (len < 0) panic("fprintf error");

    int rt = fclose(file);
    check(rt, "fclose error");
}

void wait_init(int fd[2]) {
    close(fd[1]);
    int rt = read(fd[0], &(char){}, 1);
    if (rt < 0) panic("read error");
    close(fd[0]);
}

int run_argv(void *arg) {
    struct CloneParams *params = arg;
    wait_init(params->fd);

    print_resuid();

    int rt;
    rt = mount("alpine", "alpine", NULL, MS_BIND, NULL);
    check(rt, "mount root error");

    rt = chdir("alpine");
    check(rt, "chdir root");

    rt = syscall(SYS_pivot_root, ".", ".");
    check(rt, "pivot root error");

    rt = mount(NULL, "/proc", "proc", 0, NULL);
    check(rt, "mount proc error");

    rt = umount2(".", MNT_DETACH);
    check(rt, "umount root error");

    return execvp(*params->argv, params->argv);
}


int main(int argc, char *argv[]) {
    if (argc < 2) panic("Not enough arguments");

    struct CloneParams params = {.argv = argv + 1};
    check(pipe(params.fd), "pipe");
    void *child_stack = malloc(STACK_SIZE) + STACK_SIZE;
    int clone_flags = CLONE_NEWUSER | CLONE_NEWPID | CLONE_NEWNS |
                      CLONE_NEWUTS | CLONE_NEWNET | CLONE_NEWIPC |
                      CLONE_NEWCGROUP | SIGCHLD;

    int pid = clone(run_argv, child_stack, clone_flags, &params);
    if (pid < 0) panic("clone error");
    close(params.fd[0]);


    int uid = getuid();
    char path[64], text[64];
    snprintf(text, sizeof text, "0 %d 1", uid);

    snprintf(path, sizeof path, "/proc/%d/uid_map", pid);
    write_and_check(path, text);

    snprintf(path, sizeof path, "/proc/%d/setgroups", pid);
    write_and_check(path, "deny");

    snprintf(path, sizeof path, "/proc/%d/gid_map", pid);
    write_and_check(path, text);

    write(params.fd[1], &(char){}, 1);
    close(params.fd[1]);


    int status;
    waitpid(pid, &status, 0);

    printf("ok\n");
    return !WIFEXITED(status) || WEXITSTATUS(status);
}
