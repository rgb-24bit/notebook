import java.util.*;

public class Test {
  public static void main(String[] args) {
    List<Integer> list = new ArrayList<>();

    list.add(1000);
    list.remove(new Integer(1000));

    System.out.println(list);
  }
}