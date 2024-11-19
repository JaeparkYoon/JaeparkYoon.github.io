---
title: Kotlin flow의 sample을 이용하여 UI 개선
author: jaepark
date: 2024-11-19
categories: [Kotlin]
tags: [flow,flow sample]
pin: false
img_path: '/assets/img'
---
## 문제 인식 및 해결
제가 만들고 있는 키보드 앱에서는 키보드 높낮이를 조절하는 기능이 있습니다. datastore에 키보드 높낮이 비율을 flow 값으로 갖고 있고, 이를 collect 하여
높낮이 비율 기준으로 계산하여 UI 높이를 다음과 같이 조절했습니다.

![webm_1](/kotlin/flow_sample/before_apply_sample.gif){: width="300" }

간헐적으로 높이 조절 시 키보드 UI가 깜빡거리는 느낌을 받아 사용자가 높이 조절 시 눈의 피로감과 부자연스러움을 느낄 수 있다는 생각에 이를 개선할 방법을
생각해 봤습니다.
<br>
원인을 파악해본 결과 높낮이 조절바를 연속적으로 조절할 때 바뀌는 모든 비율을 UI에 적용하고 있어, 빠르게 UI가 변화하는 사이에 간헐적인 깜빡임이 있었습니다.<br>
이러한 원인을 바탕으로 변화하는 비율의 값을 모두 받지 않고, 짧게 텀을 줘서 그 사이에서 변화하는 높낮이 비율의 최신 값을 받으면 된다는 접근 방법으로 코드를 개선해 봤습니다.
collect -> collectLatest로 바꿔봤지만, collectLatest가 중간에 취소하고 받는 게 빠르게 일어나고 있어 깜빡임의 현상은 여전히 일어나고 있어 이를
대체할 수 있는 방법을 찾은 것이 flow의 sample 이었습니다.

## sample
**flow의 sample은 지정한 시간 사이에서 방출된 가장 최신의 값을 받도록 해주는 함수입니다.** [공식문서](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/sample.html)
의 코드 예시를 보면 다음과 같습니다.
```kotlin
flow {
    repeat(10) {
        emit(it)
        delay(110)
    }
}.sample(200)
```
```
1, 3, 5, 7, 9 
```

## 적용 결과
값을 받는 텀을 대략 0.05초로 지정해주고 다음과 같이 적용해봤습니다.
```kotlin
settingDataStore.heightRate
  .sample(50)
  .collect { rate ->
    heightRate = rate
  }
```

![webm_1](/kotlin/flow_sample/after_apply_sample.gif){: width="300" }

이렇게 키보드 높낮이를 바꿀때 좀 더 부드러운 UI로 유저가 이용할 수 있도록 개선돼서 너무 기쁘네요!
