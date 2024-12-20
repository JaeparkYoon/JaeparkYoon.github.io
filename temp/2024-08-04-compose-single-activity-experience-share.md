---
title: Android compose single activity 도입 및 시행착오 공유
author: jaepark
date: 2024-08-04 10:38:00 +0900
categories: [Android]
tags: [compose, structure]
pin: false
img_path: '/assets/img'
---
reade reference before write post
https://medium.com/@chethan.n/viewmodels-with-hilt-and-compose-navigation-c11923df1540
https://developer.android.com/guide/navigation/backstack

고민한 내용
1. one screen one ViewModel?
2. navigate 할때마다 증식하는 viewModel instance를 해결하라
3. 다른 스크린에서 결괏값을 받아오는 방식 적립 (activity for result?)

장점
1. LifeCycle 관련 처리가 매끄러움 (Application에서 Activity Lifecycle Listener로 처리하지 않아도 됨)
2. Compose navigation에서 화면 전환 애니메이션을 사용하기 때문에 좀 더 세련된 앱을 만들 수 있다.
단점
1. Activity가 한개이기 때문에 딥링크 처리하는 Activity를 별도로 생성하기가 애매하다.
2. Compose Navigation 처리 및 구축에 관련한 낮지 않은 러닝커브가 있다.
