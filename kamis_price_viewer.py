# 필요한 라이브러리 임포트
from kamis.client import CertificationPair, KamisOpenApi  # KAMIS API 관련 클래스
import logging  # 로깅을 위한 라이브러리
import os  # 환경변수 접근용
from dotenv import load_dotenv  # .env 파일 로드
from tabulate import tabulate  # 테이블 형식 출력용

# 로깅 설정 (DEBUG 레벨로 자세한 로그 출력)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def format_price_table(prices):
   """가격 정보를 테이블 형태로 포맷팅하는 함수"""
   table_data = []  # 테이블에 들어갈 데이터를 저장할 리스트
   headers = ["상품명", "단위", "당일", "1일전", "1개월전", "1년전", "변동률"]  # 테이블 헤더
   
   # 각 상품의 가격 정보를 순회하며 테이블 데이터 구성
   for item in prices:
       prices = item.date_price_dict
       row = [
           f"{item.product_name:<12}",  # 상품명 (왼쪽 정렬, 12자리)
           f"{item.unit:<6}",           # 단위 (왼쪽 정렬, 6자리)
           f"{prices['당일']:>6,}",       # 당일 가격 (오른쪽 정렬, 천단위 구분)
           f"{prices['1일전']:>6,}",      # 1일전 가격
           f"{prices['1개월전']:>6,}" if prices['1개월전'] else '-',  # 1개월전 가격 (없으면 '-')
           f"{prices['1년전']:>6,}" if prices['1년전'] else '-',      # 1년전 가격 (없으면 '-')
           f"{item.direction_value:>4}%"  # 변동률 (오른쪽 정렬, 4자리)
       ]
       table_data.append(row)
   
   # tabulate 라이브러리를 사용하여 테이블 형식으로 변환
   return tabulate(table_data, headers=headers, tablefmt="simple")

def main():
   # .env 파일에서 환경변수 로드
   load_dotenv()
   
   # 환경변수에서 KAMIS API 인증정보 가져오기
   cert_id = os.getenv('KAMIS_CERT_ID')
   cert_key = os.getenv('KAMIS_CERT_KEY')
   
   # KAMIS API 클라이언트 초기화
   client = KamisOpenApi(
       CertificationPair(cert_key=cert_key, cert_id=cert_id)
   )
   print("KAMIS API 연결 완료")

   try:
       # 최근 일자 가격정보 조회
       print("\n가격 정보 조회 중...")
       daily_sales = client.daily_sales_list()
       print(f"\n총 {len(daily_sales.prices)}개의 가격 정보 (단위: 원)")
       print(format_price_table(daily_sales.prices))
   
   except Exception as e:
       # 에러 발생시 로그 기록
       logger.error(f"에러 발생: {str(e)}")

# 스크립트가 직접 실행될 때만 main() 함수 실행
if __name__ == "__main__":
   main()