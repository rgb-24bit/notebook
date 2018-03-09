#include <stdio.h>

/* sizeof(char) = 1 */
typedef unsigned char* byte_pointer;


void show_bytes(byte_pointer start, size_t len) {
  for (size_t i = 0; i < len; ++i) {
    printf("%p %.2x\n", &start[i], start[i]);
  }
}


int main(int argc, char* argv[]) {
  int num = 0x01234567;
  show_bytes((byte_pointer)&num, sizeof(int));
}
