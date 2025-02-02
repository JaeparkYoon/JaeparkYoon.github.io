---
title: Android 프로젝트에서 Compose UI를 선택한 이유
author: jaepark
date: 2024-02-15 10:38:00 +0900
categories: [Android]
tags: [compose]
pin: false
media_subpath: '/assets/img'
---
## **특정 트리거로 인해 UI Update 시 불필요한 렌더링 완화로 인한 성능 향상**
[기존 View System에서 자식뷰가 새로 그려지게 되면 그 위에있는 ViewGroup 안에 있는 뷰도 같이 새로 그려지게 됩니다.](https://developer.android.com/topic/performance/rendering/optimizing-view-hierarchies#managing)
Compose는 이를 보완하여 Recompose 시 다시 그릴 필요없는 UI 렌더링을 스킵하도록 설계 되어있어 성능 향상를 불러옵니다.
> Compose는 어떻게 불필요한 UI 렌더링을 스킵 하는지 궁금하시면 여기 [링크](https://developer.android.com/jetpack/compose/lifecycle#skipping)에서 확인하실 수 있습니다.
{: .prompt-tip }

## **개발 퍼포먼스 및 유지 보수 효율성 향상**
Compose는 기존 xml과 비교 했을 때 개발 퍼포먼스 및 유지 보수 효율성이 다음과 같은 이유로 향상됩니다.

### **더 짧은 코드 작성과 적은 Context Change 비용**
Compose는 네이티브 코드와 xml 창을 동시에 띄우지 않아도 코드 하나로 개발이 가능합니다. 이는 xml 코드 따로, 네티이브 코드 따로 작성이 필요한 기존 View 보다
더 적은 코드 작성으로 개발 퍼포먼스를 향상 시킬 수 있습니다. 대표적인 예가 List View를 작성할 때 입니다. 기존 View System에서는 List UI를 작성할 때 ListView 또는 RecyclerView를 사용합니다.
이 두개의 위젯은 각각 Item의 Adapter가 필요하기 때문에 코드의 길이가 길어지며, Context change 비용이 커집니다.
#### **기존 View System**
TestRecyclerViewAdapter.kt
```kotlin
class TestRecyclerViewAdapter(
    private val list: List<String>
): RecyclerView.Adapter<TestRecyclerViewAdapter.ViewHolder>() {
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding: ItemTestBinding = DataBindingUtil.inflate(
            LayoutInflater.from(parent.context),
            R.layout.item_test,
            parent,
            false
        )
        return ViewHolder(binding)
    }

    override fun getItemCount(): Int = list.size

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        with(holder.binding) {
            text = "$position Item"
        }
    }

    class ViewHolder(val binding: ItemTestBinding) : RecyclerView.ViewHolder(binding.root)
}
```
item_test.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<layout xmlns:app="http://schemas.android.com/apk/res-auto">
    <data>
        <variable
            name="text"
            type="String" />
    </data>
    <androidx.constraintlayout.widget.ConstraintLayout
        xmlns:android="http://schemas.android.com/apk/res/android"
        android:layout_width="match_parent"
        android:layout_height="wrap_content">

        <TextView
            android:id="@+id/tv_test"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:textSize="16sp"
            android:text="@{text}"
            app:layout_constraintTop_toTopOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            />
    </androidx.constraintlayout.widget.ConstraintLayout>
</layout>
```

#### **Compose**
TestScreen.kt
```kotlin
@Preview
@Composable
fun TestScreen(
  list: List<String>
) {
  LazyColumn(horizontalAlignment = Alignment.Start) {
    items(list.size) { position ->
      Text(
        text = "$position Item",
        fontSize = 16.sp
      )
    }
  }
}
```
이렇게 코드를 놓고 비교했을 때도 Compose UI의 코드가 기존 View System에 비해 현저히 적으며 한 개의 함수로 View를 그릴 수 있어 CContext Change 비용이 적습니다.
### **복잡한 상속 관계 해소**
View System에서 모든 UI(TextView, ImageView, ButtonView..)는 View를 상속합니다. 그리고 android UI가 업데이트되면 될수록 
ImageView를 상속하는 또 다른 자식 class가 생성되어 상속 관계가 복잡해졌습니다.
[이러한 부작용을 예시로 잘 설명한 블로그 글](https://wooooooak.github.io/jetpack%20compose/2021/05/18/%EC%BB%B4%ED%8F%AC%EC%A6%88%EA%B0%80%ED%95%84%EC%9A%94%ED%95%9C%EC%9D%B4%EC%9C%A0/)에 의하면 다음 과
같은 예시가 나오는데, 저 또한 겪은일이고 공감하게 되어 인용하자면 다음과 같습니다.
> 텍스트가 아니라 이미지가 랜더링되는 Button을 사용하고 싶어졌다고 해봅시다. 아마도 Button을 상속한 ImageButton이란게 있지 않을까?라는 생각으로 ImageButton를 찾아봅니다. 
> 역시나 ImageButton 클래스가 존재했고, XML에서 기존의 Button을 ImageButton으로 교체합니다. 
> 그러나 ImageButton도 Button이니까 당연히 아무런 문제 없이 돌아갈 거라고 생각했지만, 실행조차 되지 않고 컴파일 에러가 납니다😭. 
> 에러는 기존에 코틀린으로 findViewById를 사용하여 Button을 찾아서 Button의 메서드를 호출한 부분에서 발생하였습니다. 
> ImageButton도 Button인데 왜 Button의 메서드를 호출하는 코드에서 에러가 난걸까요? 그 이유는, 
> 사실 Button과 ImageButton이 굉장히 밀접한 관계가 있을거라 생각했지만 사실은 전혀 관계가 없기 때문입니다😞.

알고보니 Button은 TextView를 상속하고 있었고, ImageButton은 ImageView를 상속하고 있었습니다. 이는 추후 유지보수에 있어서 비효율적인 추가 작업을 야기합니다.
이를 해결하기 위해 Compose는 상속 보다는 합성을 선택했습니다. 

> 더 이상 Button에서 text를 변경할 때, 상속받은 text 속성에 “hello”를 입력하지 않아야 합니다. 대신 Button이 Text를 가지고 있게 해서, Text가 랜더링 하도록 위임하면 됩니다. 
> 그리고 이게 바로 Compose가 설계된 방식이고, 여러분이 Jetpack Compose로 UI를 그릴 때 사용할 방식입니다.

```kotlin
Button(onClick = { /*TODO*/ }) {
    Text(text = "Hello")
}
```

### **위젯 분리의 편리함**
Compose는 함수 단위로 위젯을 분리하기가 좋은 구조로 돼있습니다. 다양한 앱 디자인을 보면 공통적으로 사용되는 컴포넌트들이 있기에 이를 공용으로 사용하도록 
분리하여 다양한 화면에서 사용한다면 코드 재사용성이 늘어나고, 유지 보수에의 효율성이 크게 증가하게 됩니다.

## **Compose Multiplatform UI Framework 확장성에 대한 기대**
[더 나아가 현재 JetBrains에서 Flutter, React Native 와 같은 Compose UI를 기반한 멀티 플랫폼을 제작하고 있습니다.](https://www.jetbrains.com/lp/compose-multiplatform/) 
현재 시점(2024. 03. 06)에서 아직 iOS는 Alpha 버전이지만, 추후 정식 버전으로 릴리스될 것으로 기대하고 있습니다. 
Flutter, React Native 같은 크로스 플랫폼의 수요는 여전히 많아 Compose Multi Platform이 정식 릴리스된다면 많은 개발자들이 흥미를 가질 거라 생각합니다. 
Kotlin이라는 매력적인 언어를 사용하면서 멀티 플랫폼이 가능하다고 생각하면 저의 개인적인 입장에서는 정말 흥미롭고 배우고 싶다는 생각이 들게 만듭니다.


**참고했던 글**<br>
- [https://developer.android.com/topic/performance/rendering/optimizing-view-hierarchies#managing](https://developer.android.com/topic/performance/rendering/optimizing-view-hierarchies#managing)
- [https://wooooooak.github.io/jetpack%20compose/2021/05/18/%EC%BB%B4%ED%8F%AC%EC%A6%88%EA%B0%80%ED%95%84%EC%9A%94%ED%95%9C%EC%9D%B4%EC%9C%A0/](https://wooooooak.github.io/jetpack%20compose/2021/05/18/%EC%BB%B4%ED%8F%AC%EC%A6%88%EA%B0%80%ED%95%84%EC%9A%94%ED%95%9C%EC%9D%B4%EC%9C%A0/)
