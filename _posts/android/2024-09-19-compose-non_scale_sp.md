---
title: Android 시스템 글자 크기 설정에 영향받지 않는 sp 단위
author: jaepark
date: 2024-09-19 20:18:00 +0900
categories: [Android]
tags: [compose]
pin: false
img_path: '/assets/img'
---
Android 앱 개발을 하면서 가끔은 시스템 설정의 글자 크기를 무시하고 고정 사이즈를 필요로 하는 상황을 맞이할 수 있습니다. 기존 xml의 TextView에서는
sp 단위가 아닌 dp 단위를 써서 고정시킬 수 있었습니다. 하지만 Compose에서는 Text의 단위는 sp 또는 em 단위를 써야 합니다. sp 단위는 시스템의 글자 크기 
설정에 따라 크기가 변화하고, em은 각 시스템 폰트마다 정해놓은 1em의 단위가 고정돼 있지만, 각 폰트마다 1em의 크기가 다릅니다. 이를 해결하기 위해 fontScale을
가져와 sp를 구하는 확장 함수를 구현할 수 있었습니다.

```kotlin
val Int.nonScaledSp 
    @Composable
    get() = (this / LocalDensity.current.fontScale).sp

val Float.nonScaledSp
    @Composable
    get() = (this / LocalDensity.current.fontScale).sp
```

**참고**
- [https://stackoverflow.com/questions/69108033/prevent-text-in-jetpack-compose-from-enlarging-when-device-font-size-is-increase](https://stackoverflow.com/questions/69108033/prevent-text-in-jetpack-compose-from-enlarging-when-device-font-size-is-increase)
