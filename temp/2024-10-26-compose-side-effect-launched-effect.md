---
title: Android Compose의 SideEffect - 1. 개념 및 예시
author: jaepark
date: 2024-10-26 :47:00 +0900
categories: [Android]
tags: [compose, side-effect]
pin: false
img_path: '/assets/img'
---
## 개념
프로그래밍에서 SideEffect를 보편적으로 예상하지 못한 동작에서 일어난 결과를 얘기합니다. 이와 같은 맥락으로 Compose의 SideEffect는
Composable 함수 범위 밖에서 일어나는 앱 상태의 변화 때문에 예상치 못한 Recomposition이 발생하여 Composable 안에서 다른 순서로 Recomposition이
되거나, Recomposition이 생략될 수 있는 상황을 말합니다. // TODO 개념 다시 정리하기

## 예시
1. Button Click 이후 Dialog가 나타날 때

```kotlin
@Composable
fun ComposeScreen() { 
  var isShowSnackBar by remember { mutableStateOf(false) }
  if (isShowSnackBar) {
      
  }
  Button(
    onClick = {
        isShowSnackBar = true
    }
  ) {
      
  }
}
```

