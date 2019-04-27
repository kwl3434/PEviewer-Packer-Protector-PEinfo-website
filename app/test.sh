#!/bin/bash
value = wc -c /root/ouput.txt | awk '{print $1}' 
if [ $value -gt 232 ]; then  # 바이러스없는 출력 결과물의 바이트 수보다 크면 바이러스 파일이므로라 삭제
          #sed -e '1,$d' /root/test1.txt > /root/test1.txt
          #rm ./uploadfile/*.* #바이러스 파일이므로 파일 삭제
       echo "this is  if test"
elif[ $value -le 232 ]; then #바이러스없는 출력 결과물의 바이트 수가 작거나 같으면 아무 이상 없음
          echo "this is  if test"                                                       #PEviwer PEinfo 실행
         # rm ./uploadfile/*.* #업로드된 파일을 모두 지우는 이유는 업로드경로상에 파일이 남아있으면 test1.txt에 해쉬값이 계속 쌓이기 때문에
                            #바이러스 토탈에서 바이러스가 있든 없든 같은 파일 해쉬값을 분석 하기 때문
 fi
