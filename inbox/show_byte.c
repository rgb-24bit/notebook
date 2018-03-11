#include <stdio.h>

/* sizeof(char) = 1 */
typedef unsigned char* byte_pointer;


void show_bytes(byte_pointer start, size_t len) {
  for (size_t i = 0; i < len; ++i) {
    printf("%p %.2x\n", &start[i], start[i]);
  }
}


int main(int argc, char* argv[]) {
  int i_num = 0x01234567;
  float f_num = 0x01234567f;

  printf("%p\n", &i_num);
  show_bytes((byte_pointer)&i_num, sizeof(int));

  printf("%p\n", &f_num);
  show_bytes((byte_pointer)&f_num, sizeof(float));

  return 0;
}
