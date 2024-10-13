---
title: Android forEach vs fastForEach 비교
author: jaepark
date: 2024-10-13 22:50:00 +0900
categories: [Android]
tags: [compose]
pin: false
img_path: '/assets/img'
---
Android Compose를 이용하여 개발하면서 우연히 fastForEach를 발견하게 됐습니다. 왜 kotlin의 기존 forEach를 제쳐두고 별도로 fastForEach를 만들어
사용했는지 궁금하여 fastForEach와 forEach의 차이점을 알아보고 추후 코드를 작성할 때 언제 이용하는게 유리한지 알아보겠습니다.

### forEach fastForEach의 동작 방식

우선, kotlin에서 가본으로 제공하는 forEach의 내부 코드와 자바 코드로 어떻게 디컴파일 되는지 살펴봤습니다.

```kotlin
@kotlin.internal.HidesMembers
public inline fun <T> Iterable<T>.forEach(action: (T) -> Unit): Unit {
  for (element in this) action(element)
}
```

내부 코드를 살펴보면 forEach는 Collection의 최상위 interface인 Iterable의 확장 함수로 작성돼있는 것을 알 수 있었습니다. for문을 돌려서
List, Set, Queue 같은 Collection들의 element를 고차함수의 인자로 넘겨서 forEach { element -> ptrintln(element) }와 같은 간결한
kotlin 코드를 작성할 수 있게 해줍니다.

```kotlin
listOf("element_1", "element_2", "element_3").forEach { println(it) }
```

위의 코드를 java 코드로 디컴파일 하면 다음과 같이 나옵니다.

```java
String[]var0=new String[]{"element_1","element_2","element_3"};
Iterable $this$forEach$iv=(Iterable)CollectionsKt.listOf(var0);
int $i$f$forEach=false;
Iterator var2=$this$forEach$iv.iterator();

while(var2.hasNext()) {
    Object element$iv=var2.next();
    String it=(String)element$iv;
    int var5=false;
    System.out.println(it);
}
```
var2라는 iterator의 객체를 할당하여 iterator의 element의 마지막까지 돌아가는 while문을 돌려 element를 반환하고 있습니다.
다음은 fastForEach는 내부 코드가 어떻게 됐는지 살펴봤습니다.
```kotlin
@Suppress("BanInlineOptIn")
@OptIn(ExperimentalContracts::class)
inline fun <T> List<T>.fastForEach(action: (T) -> Unit) {
  contract { callsInPlace(action) }
  for (index in indices) {
    val item = get(index)
    action(item)
  }
}
```
forEach와 다르게 fastForEach는 Iterable의 확장함수가 아닌 Iterable을 최종적으로 상속하는 interface 중 하나인 List의 확장함수로 돼있습니다.
이 부분에서 알 수 있는 점은 모든 Collection을 지원하지 않고 일부 Collection만 지원한다는 것입니다. 또한 list의 index를 사용하여 element를
get 하는 부분이 눈에 띄었으며, contract { callsInPlace(action) }를 사용하여 컴파일러에게 action의 반복 횟수를 알려주고 있는 것을 보아 컴파일러는
Iterator를 사용하면 반복횟수를 알 수 있지만 List의 index를 사용한다면 반복횟수를 알 수 없다는점을 확인하게 됐습니다. 마찬가지로 fastForEach로 바꿔서
디컴파일 해보면 다음과 같습니다.
```java
String[]var0=new String[]{"element_1","element_2","element_3"};
List $this$fastForEach$iv=CollectionsKt.listOf(var0);
int $i$f$fastForEach=false;
int index$iv=0;

for(int var3=$this$fastForEach$iv.size(); index$iv<var3; ++index$iv) {
    Object item$iv=$this$fastForEach$iv.get(index$iv);
    String it=(String)item$iv;
    int var6=false;
    System.out.println(it);
}
```
디컴파일 해보면 Iterator 대신 원시 타입인 index 변수를 사용하여 for문 안에서 list.get(index) 형식으로 각각의 element를 보내고 있습니다.

### 성능의 차이
성능의 차이로 봤을 때 fastForEach가 좀 더 성능을 낼만한 점은 2가지로 추릴 수 있습니다. 
- Iterator 객체 대신 index 역할을 하는 int 변수를 메모리에 할당
- iterator의 next() 대신 get(i)를 사용

메모리를 객체 대신 원시 타입을 할당하는 점은 성능상 유리한 부분을 가져올 수 있지만 next() 대신 get(i)를 사용하여 반복문 안에서 element를 return
하는 것이 왜 유리한가에 대한 의문점이 있었습니다. 그 의문점을 해결하기 위한 실마리가 fastForEach 공식 문서 설명에 있었습니다. 

> Do not use for collections that come from public APIs, since they may not support random access in an efficient way, 
> and this method may actually be a lot slower. Only use for collections that are created by code we control and are known to support random access.
{: .prompt-info }

공통 API에서 제공되는 Collection에서는 random access를 지원하지 않을 수 있어 더 느릴 수 있으니 사용하지 말고, 
우리가 직접 만든 코드 또는 random access를 지원한다는 것이 알려진 collection에서 fastForEach를 사용하라는 문구에서 볼 수 있듯이 random access를 
지원하는 Collection에서는 이 방법이 더 빠른것을 알 수 있습니다. 그렇다면 RandomAccess는 무엇일까 찾아봤더니,
**java의 List Collection중에 element를 가져올 때 더 효율적인 알고리즘을 제공하기 위한 목적으로 만들어진 java의 interface 였습니다.**
[공식문서의 설명을 읽어보면 RandomAccess를 Implementing 하는 Collection들은 반복문을 돌 때 iterator의 next()보다 get(i)의 접근이 더 
성능상 빠르다고 설명합니다.](https://developer.android.com/reference/java/util/RandomAccess)
<br><br>
즉, RandomAccess를 지원하는 Collection은 get(i)가 더 유리함으로 Kotlin의 forEach보다 더 좋은 성능을 가져갈 수 있다는 사실을 알 수 있습니다. 

### 결론
**kotlin에서 forEach 대신 fastForEach를 사용하면 더 좋은 성능을 내는 자료구조형은 RandomAccess를 Implementing 하는 모든 Collection입니다.**
대표적인 Collection들은<br>
- java : ArrayList, AttributeList, CopyOnWriteArrayList, RoleList, RoleUnresolvedList, Stack, Vector<br>
- kotlin : List(CollectionsJVM에서 ListBuilder를 통해 RandomAccess Implementing) , MutableList<br>
- android : 직접 만든 자료 구조형인 SnapshotStateList 등등..

다양하게 있습니다 추후 버전이 업데이트 되면서 새로운 자료구조형이 나타나 RandomAccess를 지원하는 잠재적인 Collection 또한 포함이 된다고 볼 수 있습니다.
<br>
**반대로 forEach의 성능이 좋은 자료구조형은 RandomAccess를 지원하지 않는 Collection이라고 볼 수 있습니다.**

**참고**<br>
- [https://developer.android.com/reference/java/util/RandomAccess](https://developer.android.com/reference/java/util/RandomAccess)
- [https://developer.android.com/reference/kotlin/androidx/compose/ui/util/package-summary#(kotlin.collections.List).fastForEach(kotlin.Function1)](https://developer.android.com/reference/kotlin/androidx/compose/ui/util/package-summary#(kotlin.collections.List).fastForEach(kotlin.Function1))
- [https://jisungbin.medium.com/%EC%BD%94%ED%8B%80%EB%A6%B0-%EB%8C%80%EC%9A%A9%EB%9F%89-%EB%B0%98%EB%B3%B5%EB%AC%B8%EC%9D%84-%ED%9A%A8%EC%9C%A8%EC%A0%81%EC%9C%BC%EB%A1%9C-%EB%8F%8C%EB%A6%AC%EA%B8%B0-b857cda50f14](https://jisungbin.medium.com/%EC%BD%94%ED%8B%80%EB%A6%B0-%EB%8C%80%EC%9A%A9%EB%9F%89-%EB%B0%98%EB%B3%B5%EB%AC%B8%EC%9D%84-%ED%9A%A8%EC%9C%A8%EC%A0%81%EC%9C%BC%EB%A1%9C-%EB%8F%8C%EB%A6%AC%EA%B8%B0-b857cda50f14)
