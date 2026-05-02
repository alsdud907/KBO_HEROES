나는 kbo 야구선수의 시합 기록을 실시간으로 누적하고 비교하는 사이트를 만들고 싶어.
나는 git page를 이용해서 만들고 싶어.
나는 다음 선수들의 기록을 비교하고 싶어. 

2025년도~현재까지의 키움 히어로즈 김건희 의 기록
https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx

2022년도~현재까지의 키움 히어로즈 안우진 의 기록
https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerID=66349&tab=1&startY goog1
2022년도~현재까지의 삼성 라이온즈 원태인의 기록
https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerID=69298&tab=1&startY goog1
2022년도~현재까지의 롯데 자이언츠 박세웅의 기록
https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerID=67130&tab=1&startY goog1
2022년도~현재까지의 nc 다이노스 구창모의 기록
https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerID=68049&tab=1&startY goog1
2022년도~현재까지의 기아 타이거즈 이의리 의 기록
https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerID=71320&tab=1&startY goog1
2022년도~현재까지의 한화 이글스 문동주의 기록
https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerID=69032&tab=1&startY goog1
2022년도~현재까지의 kt 위즈 고영표의 기록
https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerID=69347&tab=1&startY goog1
2022년도~현재까지의 두산 베어스 곽빈의 기록
https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerID=68582&tab=1&startY goog1
2022년도~현재까지의 lg트윈스 임찬규의 기록
https://www.koreabaseball.com/Record/Player/PitcherBasic/Basic1.aspx?playerID=68726&tab=1&startY goog1

이 선수들의 기록을 비교할 거야.
키움 히어로즈 김건희는 타자이고 나머지는 투수야.
타자는 본인의 기록을 연도별로 비교해줘.
투수는 연도별로 각각의 스탯을 다른 투수와 비교해줘. 

타자의 스탯, 투수의 스탯 기록은 내가 사이트에 접속했을때 수집해줘.

디자인은 이렇다하게 정해진 건 없고, #f3f6ff
#cef26d #3770bf #8dc2ff 컬러 위주로 이쁘게 만들어줘.

투수별 whip지표 데이터가 누락됐어
각 지표가 무엇을 뜻하는지도 아래를 참조해서 표시해줘
[
  {
    "indicator": "ERA (평균자책점)",
    "definition": "9이닝당 평균 자책점"
  },
  {
    "indicator": "WHIP (이닝당 출루 허용)",
    "definition": "이닝당 허용한 안타+볼넷 수"
  },
  {
    "indicator": "G / IP",
    "definition": "출장 경기 수 / 소화 이닝 수"
  },
  {
    "indicator": "W / L / WPCT",
    "definition": "승 / 패 / 승률"
  },
  {
    "indicator": "SV / HLD",
    "definition": "세이브 / 홀드"
  },
  {
    "indicator": "BB / HBP",
    "definition": "볼넷 / 몸에 맞는 공"
  },
  {
    "indicator": "SO (탈삼진)",
    "definition": "삼진을 잡아낸 횟수"
  },
  {
    "indicator": "H / HR",
    "definition": "피안타 / 피홈런"
  },
  {
    "indicator": "R / ER",
    "definition": "총 실점 / 자책점"
  }
]
 
막대그래프별로 스탯별 상위, 평균, 하위 점수를 아래 데이터 참조해서 막대그래프에 표시해줘
[
  {
    "지표": "ERA (평균자책점)",
    "상위": "3.50 이하",
    "중위": "4.30 ~ 4.80",
    "하위": "5.50 이상"
  },
  {
    "지표": "WHIP (이닝당 출루 허용)",
    "상위": "1.20 미만",
    "중위": "1.35 ~ 1.50",
    "하위": "1.65 이상"
  },
  {
    "지표": "IP (이닝 소화)",
    "상위": "170이닝 이상",
    "중위": "144이닝(규정)",
    "하위": "100이닝 미만"
  },
  {
    "지표": "WPCT (승률)",
    "상위": "0.650 이상",
    "중위": "0.500 내외",
    "하위": "0.400 이하"
  },
  {
    "지표": "BB/9 (9이닝당 볼넷)",
    "상위": "2.5개 이하",
    "중위": "3.5 ~ 4.0개",
    "하위": "5.0개 이상"
  },
  {
    "지표": "K/9 (9이닝당 탈삼진)",
    "상위": "9.0개 이상",
    "중위": "6.5 ~ 7.5개",
    "하위": "5.0개 이하"
  },
  {
    "지표": "K/BB (삼진/볼넷 비율)",
    "상위": "3.50 이상",
    "중위": "2.00 ~ 2.50",
    "하위": "1.50 이하"
  },
  {
    "지표": "HR/9 (9이닝당 피홈런)",
    "상위": "0.7개 이하",
    "중위": "1.0 ~ 1.2개",
    "하위": "1.5개 이상"
  }
]


