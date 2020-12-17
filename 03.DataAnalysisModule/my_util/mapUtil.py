import pandas as pd 

# 행정구
tmp_gu_dict = {
    '수원':['장안구', '권선구', '팔달구', '영통구'], 
    '성남':['수정구', '중원구', '분당구'], 
    '안양':['만안구', '동안구'], 
    '안산':['상록구', '단원구'], 
    '고양':['덕양구', '일산동구', '일산서구'], 
    '용인':['처인구', '기흥구', '수지구'], 
    '청주':['상당구', '서원구', '흥덕구', '청원구'], 
    '천안':['동남구', '서북구'], 
    '전주':['완산구', '덕진구'], 
    '포항':['남구', '북구'], 
    '창원':['의창구', '성산구', '진해구', '마산합포구', '마산회원구']
}

def split_addr(dfarg):
    metro, city = [], []
    for i in dfarg.index:
        addr = str(dfarg['도로명주소'][i]).split()
        metro.append(addr[0])
        if (addr[1][:2] in tmp_gu_dict.keys()):
            city.append(addr[2])
        else:
            city.append(addr[1])
    dfarg['광역시도'] = metro
    dfarg['시군구'] = city
    return dfarg

def get_ID(dfarg):
    si_name = [None] * len(dfarg)
    for n in dfarg.index:
        if dfarg['광역시도'][n][-3:] not in ['광역시', '특별시', '자치시']:
        
            # 같은 '시도' 이름을 가지는 고성 지역 처리
            if dfarg['시군구'][n].strip()[:-1]=='고성' and dfarg['광역시도'][n]=='강원도':
                si_name[n] = '고성(강원)'
            elif dfarg['시군구'][n].strip()[:-1]=='고성' and dfarg['광역시도'][n]=='경상남도':
                si_name[n] = '고성(경남)'
            else:
                si_name[n] = dfarg['시군구'][n].strip()[:-1] 
        
            # 광역시가 아니면서 구를 가지고 있는 시 처리 
            for keys, values in tmp_gu_dict.items():
                if dfarg['시군구'][n].strip() in values:
                    if len(dfarg['시군구'][n]) == 2:
                        si_name[n] = keys + ' ' + dfarg['시군구'][n]
                    elif dfarg['시군구'][n] in ['마산합포구','마산회원구']:
                        si_name[n] = keys + ' ' + dfarg['시군구'][n][2:-1]
                    else:
                        si_name[n] = keys + ' ' + dfarg['시군구'][n][:-1]
        
        elif dfarg['광역시도'][n] == '세종특별자치시':  # 세종자치시의 경우는 세종으로
            si_name[n] = '세종'
        
        else:  # tmp_gu_dict와 세종을 제외한 나머지 지역 처리 
            if len(dfarg['시군구'][n].strip()) >= 3:
                si_name[n] = dfarg['광역시도'][n][:2] + ' ' + dfarg['시군구'][n][:-1]
            else:   # 인천 미추홀구 
                if dfarg['시군구'][n] == '남구' and dfarg['광역시도'][n] == '인천광역시':
                    si_name[n] = '인천 미추홀'
                else:
                    si_name[n] = dfarg['광역시도'][n][:2] + ' ' + dfarg['시군구'][n]
        
    return si_name