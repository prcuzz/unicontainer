#include <unistd.h>
#include <stdio.h>
#include <string.h>

const char *str = "Hello ZZC!\n";

void main()
{
  // printf(str);
  write(1, str, strlen(str));
}