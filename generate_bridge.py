import os
import urllib.parse
import itertools
import json

BASE_URL = "https://bridge-massage.netlify.app"
BRAND_NAME = "브릿지마사지"

# --- 최신 SEO 반영: 검색 의도 및 문제 해결형 타이틀/메타 디스크립션 ---
MAIN_TITLE = "브릿지마사지 | 내 주변 검증된 출장마사지·홈케어 안전 가이드"
MAIN_DESC = "내 위치에서 가장 빠르고 안전하게 부를 수 있는 출장마사지 업체를 찾고 계신가요? 100% 후불제 검증, 투명한 가격, 실제 이용자 후기를 바탕으로 실패 없는 홈케어 선택 기준을 제시합니다."

TITLE_TEMPLATES = itertools.cycle([
    "{full_dong} 출장마사지 가격 및 검증된 후기 완벽 정리 | {brand}",
    "{short_dong} 홈케어 추천: 내상 없는 24시간 방문 마사지 찾는 법 - {brand}",
    "피로가 안 풀릴 때? {full_dong} 타이·스웨디시 코스별 특징과 선택 가이드 | {brand}",
    "{brand} | {full_dong} 100% 안심 후불제 출장 홈타이 비교"
])

DESC_TEMPLATES = itertools.cycle([
    "{full_dong}에서 안전하고 만족스러운 홈케어를 원하시나요? 선입금 없는 100% 후불제 업체 비교, 타이·스웨디시 코스별 특징과 실제 이용자의 생생한 리뷰를 통해 내게 꼭 맞는 테라피를 찾아보세요.",
    "퇴근길 복잡한 {dist} 일대가 막히는 저녁, {full_dong} 자택으로 방문하는 프리미엄 홈타이를 소개합니다. 코스별 정확한 요금과 관리사 프로필 확인 방법을 안내해 드립니다.",
    "{short_dong} 주변에서 실제 이용자 평점이 가장 높은 출장 업체는 어디일까요? 단순 홍보가 아닌, 깐깐하게 검증된 업소 6곳의 특징과 고객들이 직접 남긴 긍정·부정 후기 요약을 확인하세요.",
    "스트레스와 만성 피로로 지친 하루, {full_dong} 지역 30분 내 방문 가능한 안심 업소를 찾으시나요? 요금 바가지 없이 투명하게 운영되는 정찰제 마사지 전문점들의 상세 정보를 제공합니다."
])

# --- 업체 리스트 (버튼 제거, 순수 텍스트) ---
SHOPS_DATA = [
    {"name": "퀸즈홈테라피", "phone": "0507-1280-3296", "desc": "[체형 맞춤 특화] 전문 힐러진의 1:1 진단을 통한 집중 피로회복 및 천연 에센셜 오일 관리. (실제 후기: 목/어깨 뭉침 해소에 탁월함)", "price": "80,000원부터~", "score": "4.9", "type": "홈타이"},
    {"name": "한국미인테라피", "phone": "0507-1280-3140", "desc": "[프라이빗 릴렉싱] 베테랑 한국인 테라피스트 배정. 의사소통이 원활하여 원하는 압과 부위를 정확히 케어받을 수 있습니다.", "price": "70,000원부터~", "score": "4.9", "type": "스웨디시"},
    {"name": "오늘밤테라피", "phone": "0507-1280-3199", "desc": "[100% 안심 후불제 보장] 타이, 전신아로마 및 VIP 감성힐링 전문. 선입금 요구가 일절 없어 첫 이용자에게 가장 추천하는 업소.", "price": "60,000원부터~", "score": "4.9", "type": "아로마"},
    {"name": "주주테라피", "phone": "0507-1280-3197", "desc": "[위생 최우선] 일회용 베드커버 및 철저한 소독 관리. 고급 수용성 오일을 사용한 최고급 럭셔리 스웨디시 프로그램.", "price": "60,000원부터~", "score": "4.8", "type": "스웨디시"},
    {"name": "기쁨테라피", "phone": "0507-1280-3183", "desc": "[활력 충전] 건식 타이와 오일 테라피를 결합한 전신 힐링. 강한 압을 선호하는 남성 및 운동선수 출신 고객들의 재방문율 1위.", "price": "60,000원부터~", "score": "4.9", "type": "타이"},
    {"name": "미인클럽테라피", "phone": "0507-1280-3180", "desc": "[스페셜 감성 케어] 젊고 세련된 감각의 2030 테라피스트들이 제공하는 트렌디한 아로마 테라피. 불면증 완화에 도움을 줍니다.", "price": "70,000원부터~", "score": "4.9", "type": "아로마"}
]

# --- 서울/경기/인천 통합 지역 데이터 ---
REGION_DATA = {
    'seoul': {
        'name': '서울특별시',
        'districts': {
            'gangnam': {'name': '강남구', 'dongs': ['역삼1동', '역삼2동', '개포1동', '개포2동', '개포4동', '청담동', '삼성1동', '삼성2동', '대치1동', '대치2동', '대치4동', '신사동', '논현1동', '논현2동', '압구정동', '세곡동', '자곡동', '일원동', '수서동', '도곡1동', '도곡2동']},
            'jungrang': {'name': '중랑구', 'dongs': ['면목본동', '면목2동', '면목3.4동', '면목5동', '면목7동', '상봉1동', '상봉2동', '중화1동', '중화2동', '묵1동', '묵2동', '망우본동', '망우3동', '신내1동', '신내2동']},
            'songpa': {'name': '송파구', 'dongs': ['잠실본동', '잠실2동', '잠실3동', '잠실4동', '잠실6동', '잠실7동', '풍납1동', '풍납2동', '거여1동', '거여2동', '마천1동', '마천2동', '방이1동', '방이2동', '오륜동', '오금동', '송파1동', '송파2동', '석촌동', '삼전동', '가락본동', '가락1동', '가락2동', '문정1동', '문정2동', '장지동', '위례동', '잠실동']}
        }
    },
    'gyeonggi': {
        'name': '경기도',
        'districts': {
            'uiwang': {'name': '의왕시', 'dongs': ['고천동', '이동', '삼동', '왕곡동', '오전동', '학의동', '내손동', '청계동', '포일동', '월암동', '초평동']},
            'suwon_jangan': {'name': '수원시 장안구', 'dongs': ['파장동', '정자1동', '정자2동', '정자3동', '영화동', '송죽동', '조원1동', '조원2동', '율천동']}
        }
    },
    'incheon': {
        'name': '인천광역시',
        'districts': {
            'yeonsu': {'name': '연수구', 'dongs': ['옥련동', '선학동', '연수동', '청학동', '동춘동', '송도1동', '송도2동', '송도3동', '송도4동', '송도5동']}
        }
    }
}

# --- HTML 템플릿들 ---
def render_template(template, **kwargs):
    result = template
    for key, value in kwargs.items():
        result = result.replace(f"{{{key}}}", str(value))
    return result

HTML_HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="format-detection" content="telephone=no">
<meta name="description" content="{meta_description}">
<title>{page_title}</title>
<link rel="canonical" href="{canonical_url}">
<meta property="og:site_name" content="{brand}">
<meta property="og:title" content="{page_title}">
<meta property="og:description" content="{meta_description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical_url}">
<meta name="theme-color" content="#1a202c">

<!-- 전문성 및 신뢰도 향상을 위한 CSS 재정의 -->
<style>
  :root { --bg-dark: #f8fafc; --card-bg: #ffffff; --text-main: #1e293b; --text-muted: #64748b; --accent: #2563eb; --accent-hover: #1d4ed8; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background-color: var(--bg-dark); color: var(--text-main); font-family: "Pretendard", -apple-system, sans-serif; line-height: 1.6; }
  a { color: inherit; text-decoration: none; }
  .wrap { max-width: 1040px; margin: 0 auto; padding: 0 16px; }
  
  header { background: #ffffff; border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 100; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  .header-row { display: flex; align-items: center; justify-content: space-between; height: 64px; }
  .brand { font-size: 1.5rem; font-weight: 800; color: var(--accent); }
  
  .hero { background: #1e293b; color: #fff; padding: 60px 16px; text-align: center; }
  .hero h1 { font-size: 2.2rem; margin-bottom: 15px; line-height: 1.3; font-weight: 800; }
  .hero p { font-size: 1.1rem; color: #cbd5e1; max-width: 600px; margin: 0 auto; }
  
  .finder { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin: -30px auto 30px; max-width: 800px; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); position: relative; z-index: 10; }
  .finder strong { width: 100%; font-size: 1rem; color: var(--text-main); margin-bottom: 8px; }
  .finder select { flex: 1; min-width: 140px; padding: 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; outline: none; background: #f8fafc; cursor: pointer; }
  .finder button { background: var(--accent); color: #fff; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 700; cursor: pointer; font-size: 0.95rem; }
  .finder button:hover { background: var(--accent-hover); }
  
  .page-head { padding: 30px 0 20px; }
  .breadcrumbs { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px; display: flex; gap: 6px; }
  .page-head h1 { font-size: 1.8rem; font-weight: 800; margin-bottom: 10px; }
  .page-head p { font-size: 1rem; color: var(--text-muted); }
  
  .section { margin-bottom: 40px; }
  .section-title { font-size: 1.4rem; font-weight: 700; margin-bottom: 20px; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }
  
  .shop-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; list-style: none; }
  .shop-card { background: var(--card-bg); border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: transform 0.2s; }
  .shop-card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-color: #cbd5e1; }
  .shop-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
  .shop-title { font-size: 1.25rem; font-weight: 800; color: var(--text-main); }
  .shop-score { color: #ea580c; font-weight: bold; font-size: 0.9rem; background: #ffedd5; padding: 2px 8px; border-radius: 12px; }
  .shop-tags { display: flex; gap: 8px; margin-bottom: 12px; }
  .shop-tag { font-size: 0.8rem; background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 4px; font-weight: 600; }
  .shop-desc { font-size: 0.9rem; color: var(--text-muted); margin-bottom: 16px; line-height: 1.5; }
  .shop-contact { background: #f1f5f9; padding: 12px; border-radius: 8px; font-size: 1.1rem; font-weight: 800; color: var(--accent); text-align: center; letter-spacing: 0.5px; border: 1px dashed #cbd5e1; }
  
  /* 문제 해결형 Q&A 섹션 (SEO 최적화) */
  .expert-guide { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
  .qa-item { margin-bottom: 24px; }
  .qa-item:last-child { margin-bottom: 0; }
  .qa-q { font-size: 1.15rem; font-weight: 700; color: #0f172a; margin-bottom: 8px; display: flex; align-items: flex-start; gap: 8px; }
  .qa-q::before { content: 'Q.'; color: var(--accent); font-weight: 900; }
  .qa-a { font-size: 0.95rem; color: #475569; padding-left: 28px; line-height: 1.7; }
  
  .map-container { width: 100%; height: 350px; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; margin-top: 20px; }
  
  footer { background: #0f172a; color: #94a3b8; padding: 40px 16px; margin-top: 60px; text-align: center; }
  .footer-title { color: #fff; font-size: 1.5rem; font-weight: 800; margin-bottom: 16px; }
  .footer-text { font-size: 0.9rem; max-width: 700px; margin: 0 auto 10px; line-height: 1.6; }
  
  @media (max-width: 768px) {
    .finder select, .finder button { min-width: 100%; flex: none; }
  }
</style>

<script type="application/ld+json">
{json_ld}
</script>
</head>
<body>
<header>
  <div class="wrap header-row">
    <a href="/" class="brand">{brand}</a>
  </div>
</header>
<main>
"""

MAIN_PAGE_BODY = """
<section class="hero">
  <h1>실패 없는 출장 홈케어<br>내 주변 검증된 업체 찾기</h1>
  <p>100% 후불제 검증, 투명한 요금표, 실제 고객들의 생생한 후기를 바탕으로 내게 꼭 맞는 테라피를 안전하게 선택하세요.</p>
</section>

<div class="wrap">
  <form class="finder" onsubmit="event.preventDefault(); goToSelectedRegion();">
    <strong>빠른 지역 검색으로 대기 시간 없이 예약하세요</strong>
    <select id="regionSelect" onchange="handleRegionChange()"><option value="">시/도 선택</option></select>
    <select id="districtSelect" onchange="handleDistrictChange()"><option value="">구·시·군 선택</option></select>
    <select id="dongSelect"><option value="">전체 동·읍·면</option></select>
    <button type="submit">검증된 매장 보기</button>
  </form>

  <div class="section">
    <h2 class="section-title">브릿지마사지 추천 프리미엄 제휴점</h2>
    <ul class="shop-grid">
      {shop_cards}
    </ul>
  </div>
</div>
"""

REGION_PAGE_BODY = """
<div class="wrap">
  <div class="page-head">
    <div class="breadcrumbs">
      <a href="/">홈</a> &gt; {breadcrumbs}
    </div>
    <h1>{location_title} 출장마사지 추천: 가격, 코스, 검증된 후기 완벽 정리</h1>
    <p>{meta_description}</p>
  </div>

  <form class="finder" onsubmit="event.preventDefault(); goToSelectedRegion();" style="margin-top:0;">
    <strong>다른 지역의 안전한 매장 검색하기</strong>
    <select id="regionSelect" onchange="handleRegionChange()"><option value="">시/도 선택</option></select>
    <select id="districtSelect" onchange="handleDistrictChange()"><option value="">구·시·군 선택</option></select>
    <select id="dongSelect"><option value="">전체 동·읍·면</option></select>
    <button type="submit">매장 보기</button>
  </form>

  <div class="section">
    <h2 class="section-title">{location_title} 지역 안심 예약 가능 업체</h2>
    <ul class="shop-grid">
        {shop_cards_detail}
    </ul>
  </div>
  
  <div class="section expert-guide">
    <h2 class="section-title" style="border:none; margin-bottom:10px;">💡 {short_dong} 출장 홈케어 실전 가이드 (전문가 & 실제 후기 기반)</h2>
    <p style="color:#64748b; margin-bottom:24px; font-size:0.95rem;">단순한 홍보가 아닌, 이용자분들이 가장 많이 겪는 문제와 궁금증을 명확히 해결해 드립니다.</p>
    
    <div class="qa-item">
        <h3 class="qa-q">{short_dong} 지역에 늦은 새벽이나 비 오는 날에도 정말 30분 내 방문이 가능한가요?</h3>
        <p class="qa-a">네, 가능합니다. {dist} 인근에 대기 중인 기사님과 전문 테라피스트들이 상주하고 있어, 교통 체증이 심한 퇴근 시간대나 새벽 2시 이후에도 <b>자택, 오피스텔, 레지던스, 호텔 등 지정하신 장소로 평균 30분 이내 도착</b>을 원칙으로 합니다. (실제 리뷰: "야근 후 새벽 3시에 불렀는데 20분 만에 오셔서 놀랐어요.")</p>
    </div>
    
    <div class="qa-item">
        <h3 class="qa-q">처음 이용하는데, 내상(불만족)이나 사기 업체를 피하는 뚜렷한 기준이 있나요?</h3>
        <p class="qa-a">가장 중요한 철칙은 <b>'선입금을 요구하는 곳은 무조건 피하는 것'</b>입니다. 브릿지마사지에 등록된 모든 업체는 <b>관리사가 직접 현장에 도착한 후 대면 결제하는 100% 후불제</b>로만 운영됩니다. 또한 통화 상담 시 관리사의 국적(한국인/태국인 등), 코스별 정확한 요금을 투명하게 고지하는 업체를 선택하셔야 실패가 없습니다.</p>
    </div>
    
    <div class="qa-item">
        <h3 class="qa-q">어깨 뭉침이 심한데 스웨디시와 타이 마사지 중 어떤 코스가 더 효과적일까요?</h3>
        <p class="qa-a">목, 어깨의 강한 뭉침과 근육통 해소가 목적이라면 강한 압을 사용하는 <b>건식 타이 마사지</b>를 추천합니다. 반면, 만성적인 스트레스와 불면증 해소, 부드러운 림프 순환을 원하신다면 따뜻한 천연 에센셜 오일을 활용하는 <b>스웨디시 아로마 테라피</b>가 훨씬 효과적입니다. 예약 시 본인의 컨디션을 말씀해주시면 맞춤형 코스를 추천해 드립니다.</p>
    </div>
  </div>

  <div class="section">
    <h2 class="section-title">{location_title} 지역 방문 가능 구역 확인</h2>
    <div class="map-container">
      <iframe width="100%" height="100%" frameborder="0" style="border:0" loading="lazy" allowfullscreen referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={map_query}&output=embed"></iframe>
    </div>
  </div>
</div>
"""

HTML_FOOTER = """
</main>
<footer>
  <div class="wrap">
    <div class="footer-title">{brand}</div>
    <p class="footer-text">{brand}는 고객님들이 안심하고 이용할 수 있도록 투명한 요금과 100% 후불제로 검증된 출장마사지·홈타이 업체 정보만을 제공합니다.</p>
    <p class="footer-text" style="font-size:0.8rem; color:#475569;">※ 본 사이트의 코스, 시간, 요금은 제휴 업소에서 제공한 정보를 바탕으로 작성되었으며, 실제 방문 시점에 따라 차이가 있을 수 있으니 유선 예약 시 최종 확인 부탁드립니다.</p>
    <p style="margin-top:20px; font-size:0.8rem;">&copy; 2026 {brand}. All rights reserved.</p>
  </div>
</footer>
<script>
    const REGION_DATA = {js_region_data};
    
    const regionSelect = document.getElementById('regionSelect');
    const districtSelect = document.getElementById('districtSelect');
    const dongSelect = document.getElementById('dongSelect');

    if (regionSelect) {
        for (const key in REGION_DATA) {
          regionSelect.add(new Option(REGION_DATA[key].name, key));
        }
    }

    function handleRegionChange() {
      if(!districtSelect) return;
      districtSelect.innerHTML = '<option value="">구·시·군 선택</option>';
      if(dongSelect) dongSelect.innerHTML = '<option value="">전체 동·읍·면</option>';
      const regKey = regionSelect.value;
      if (regKey) {
        for (const key in REGION_DATA[regKey].districts) {
          districtSelect.add(new Option(REGION_DATA[regKey].districts[key].name, key));
        }
      }
    }

    function handleDistrictChange() {
      if(!dongSelect) return;
      dongSelect.innerHTML = '<option value="">전체 동·읍·면</option>';
      const regKey = regionSelect.value;
      const distKey = districtSelect.value;
      if (regKey && distKey) {
        const dongs = REGION_DATA[regKey].districts[distKey].dongs;
        dongs.forEach(dong => dongSelect.add(new Option(dong, dong)));
      }
    }

    function goToSelectedRegion() {
      const reg = regionSelect.value;
      const dist = districtSelect.value;
      const dong = dongSelect.value;
      if (dong) window.location.href = `/region/${reg}/${dist}/${encodeURIComponent(dong)}/`;
      else if (dist) window.location.href = `/region/${reg}/${dist}/`;
      else if (reg) window.location.href = `/region/${reg}/`;
      else alert('이동할 지역과 동을 선택해주세요.');
    }
</script>
</body>
</html>
"""

def generate_shop_cards(location_name):
    cards = []
    for shop in SHOPS_DATA:
        card = f"""
        <li class="shop-card">
            <div class="shop-header">
                <h3 class="shop-title">{shop['name']}</h3>
                <span class="shop-score">★ {shop['score']}</span>
            </div>
            <div class="shop-tags">
                <span class="shop-tag">{location_name} 방문</span>
                <span class="shop-tag">{shop['type']}</span>
                <span class="shop-tag">{shop['price']}</span>
            </div>
            <p class="shop-desc">{shop['desc']}</p>
            <div class="shop-contact">
                예약/상담: {shop['phone']}
            </div>
        </li>
        """
        cards.append(card)
    return "".join(cards)

def build_json_ld(brand, page_title_h1, meta_description, canonical_url):
    return f"""{{
      "@context": "https://schema.org",
      "@type": "HealthAndBeautyBusiness",
      "name": "{page_title_h1} - {brand}",
      "description": "{meta_description}",
      "url": "{canonical_url}",
      "priceRange": "60,000원 ~ 180,000원",
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "412",
        "bestRating": "5",
        "worstRating": "1"
      }}
    }}"""

# ---------------------------------------------------------
# 사이트 빌드 실행
# ---------------------------------------------------------
OUTPUT_DIR = "bridge_site_full"
os.makedirs(OUTPUT_DIR, exist_ok=True)

urls = [f"{BASE_URL}/"]
json_region_data_string = json.dumps(REGION_DATA, ensure_ascii=False)

print(f"{BRAND_NAME} SEO(검색의도 기반) 자동화 사이트 생성을 시작합니다...")

# 1. 메인 페이지 생성
main_html = render_template(HTML_HEAD + MAIN_PAGE_BODY + HTML_FOOTER,
    brand=BRAND_NAME,
    page_title=MAIN_TITLE,
    meta_description=MAIN_DESC,
    canonical_url=f"{BASE_URL}/",
    json_ld=build_json_ld(BRAND_NAME, MAIN_TITLE, MAIN_DESC, f"{BASE_URL}/"),
    shop_cards=generate_shop_cards("전국"),
    js_region_data=json_region_data_string
)
with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(main_html)

# 2. 지역별(구, 동) 상세 페이지 생성
for reg_key, reg_val in REGION_DATA.items():
    reg_name = reg_val['name']
    
    for dist_key, dist_val in reg_val['districts'].items():
        dist_name = dist_val['name']
        
        # 구 단위 페이지 생성
        gu_dir = os.path.join(OUTPUT_DIR, "region", reg_key, dist_key)
        os.makedirs(gu_dir, exist_ok=True)
        gu_url = f"{BASE_URL}/region/{reg_key}/{dist_key}/"
        urls.append(gu_url)
        
        full_gu_title = f"{reg_name} {dist_name}"
        t_temp = next(TITLE_TEMPLATES)
        d_temp = next(DESC_TEMPLATES)
        p_title = render_template(t_temp, full_dong=full_gu_title, short_dong=dist_name, brand=BRAND_NAME)
        m_desc = render_template(d_temp, full_dong=full_gu_title, short_dong=dist_name, dist=dist_name, brand=BRAND_NAME)
        
        gu_html = render_template(HTML_HEAD + REGION_PAGE_BODY + HTML_FOOTER,
            brand=BRAND_NAME,
            page_title=p_title,
            meta_description=m_desc,
            canonical_url=gu_url,
            json_ld=build_json_ld(BRAND_NAME, f"{full_gu_title} 출장마사지", m_desc, gu_url),
            breadcrumbs=f'<a href="/region/{reg_key}/">{reg_name}</a> &gt; <span>{dist_name}</span>',
            location_title=full_gu_title,
            short_dong=dist_name,
            dist=dist_name,
            map_query=urllib.parse.quote(full_gu_title),
            shop_cards_detail=generate_shop_cards(full_gu_title),
            js_region_data=json_region_data_string
        )
        with open(os.path.join(gu_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(gu_html)
        
        # 동 단위 페이지 생성
        for dong in dist_val['dongs']:
            dong_dir = os.path.join(OUTPUT_DIR, "region", reg_key, dist_key, dong)
            os.makedirs(dong_dir, exist_ok=True)
            encoded_dong = urllib.parse.quote(dong)
            dong_url = f"{BASE_URL}/region/{reg_key}/{dist_key}/{encoded_dong}/"
            urls.append(dong_url)
            
            full_dong_title = f"{reg_name} {dist_name} {dong}"
            t_temp = next(TITLE_TEMPLATES)
            d_temp = next(DESC_TEMPLATES)
            p_title = render_template(t_temp, full_dong=full_dong_title, short_dong=dong, brand=BRAND_NAME)
            m_desc = render_template(d_temp, full_dong=full_dong_title, short_dong=dong, dist=dist_name, brand=BRAND_NAME)
            
            dong_html = render_template(HTML_HEAD + REGION_PAGE_BODY + HTML_FOOTER,
                brand=BRAND_NAME,
                page_title=p_title,
                meta_description=m_desc,
                canonical_url=dong_url,
                json_ld=build_json_ld(BRAND_NAME, f"{full_dong_title} 출장마사지", m_desc, dong_url),
                breadcrumbs=f'<a href="/region/{reg_key}/">{reg_name}</a> &gt; <a href="/region/{reg_key}/{dist_key}/">{dist_name}</a> &gt; <span>{dong}</span>',
                location_title=full_dong_title,
                short_dong=dong,
                dist=dist_name,
                map_query=urllib.parse.quote(full_dong_title),
                shop_cards_detail=generate_shop_cards(full_dong_title),
                js_region_data=json_region_data_string
            )
            with open(os.path.join(dong_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(dong_html)

# 3. 사이트맵, Robots, Netlify 설정 파일 생성 (404 방지)
sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    sitemap_xml.append(f"  <url><loc>{u}</loc><priority>0.8</priority></url>")
sitemap_xml.append('</urlset>')

with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap_xml))

with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

# ★ Netlify 404 에러 방지용 자동 설정 파일 생성 ★
# 파이썬 스크립트 실행 폴더의 최상단(OUTPUT_DIR 바깥)에 만들어 줍니다.
with open("netlify.toml", "w", encoding="utf-8") as f:
    f.write(f"""[build]
  publish = "{OUTPUT_DIR}"
""")

print(f"작업 완료! {OUTPUT_DIR} 폴더에 브릿지마사지 SEO 적용 완료된 {len(urls)}개 페이지와 netlify.toml 파일이 생성되었습니다.")