"""API 端点常量

定义薄荷健康开放平台所有 API 端点路径常量,
避免在业务代码中硬编码字符串,便于统一维护。
"""

# ===== 认证 =====
ENDPOINT_ACCESS_TOKEN = "/open-apis/v1/access_token"

# ===== 食物相关 =====
ENDPOINT_FOOD_SEARCH = "/open-apis/v1/food/search"
ENDPOINT_FOOD_DETAIL = "/open-apis/v1/food/detail"
ENDPOINT_FOOD_CATEGORIES = "/open-apis/v1/food/categories"
ENDPOINT_FOOD_LIST = "/open-apis/v1/food/list"
ENDPOINT_FOOD_UNITS = "/open-apis/v1/food/units"
ENDPOINT_FOOD_INGREDIENTS = "/open-apis/v1/food/ingredients"
ENDPOINT_FOOD_RANKS = "/open-apis/v1/food/ranks"
ENDPOINT_FOOD_IMAGE_RECOGNIZE = "/open-apis/v1/food/image_recognize"
ENDPOINT_FOOD_IMAGE_RECOGNIZE_DETAIL = "/open-apis/v1/food/image_recognize_detail"
ENDPOINT_FOOD_TEXT_RECOGNIZE = "/open-apis/v1/food/text_recognize"

# ===== 体重相关 =====
ENDPOINT_WEIGHT_RECORD = "/open-apis/v1/weight/record"
ENDPOINT_WEIGHT_RECORDS = "/open-apis/v1/weight/records"
ENDPOINT_WEIGHT_LATEST = "/open-apis/v1/weight/latest"
ENDPOINT_WEIGHT_DELETE = "/open-apis/v1/weight/delete"
ENDPOINT_WEIGHT_LINE = "/open-apis/v1/weight/line"
ENDPOINT_WEIGHT_SCALE = "/open-apis/v1/weight/scale"

# ===== 饮食相关 =====
ENDPOINT_EATING_RECORD = "/open-apis/v1/eating/record"
ENDPOINT_EATING_RECORD_SINGLE = "/open-apis/v1/eating/record_single"
ENDPOINT_EATING_UPDATE = "/open-apis/v1/eating/update"
ENDPOINT_EATING_DELETE = "/open-apis/v1/eating/delete"
ENDPOINT_EATING_RECORDS = "/open-apis/v1/eating/records"
ENDPOINT_EATING_LATEST = "/open-apis/v1/eating/latest"
ENDPOINT_EATING_NUTRITION_RECOMMEND = "/open-apis/v1/eating/nutrition_recommend"

# ===== GLP-1 用药相关 =====
ENDPOINT_MEDICINE_RECORD = "/open-apis/v1/glp1/medicine_record"
ENDPOINT_MEDICINE_RECORD_DEL = "/open-apis/v1/glp1/medicine_record_del"
ENDPOINT_MEDICINE_RECORD_UPDATE = "/open-apis/v1/glp1/medicine_record_update"
ENDPOINT_MEDICINES = "/open-apis/v1/glp1/medicines"
ENDPOINT_MEDICINE_RECORDS = "/open-apis/v1/glp1/medicine_records"
ENDPOINT_MEDICINE_RECORD_DETAIL = "/open-apis/v1/glp1/medicine_record"
ENDPOINT_MEDICINE_RECORD_LATEST = "/open-apis/v1/glp1/medicine_record_latest"
ENDPOINT_GLP1_NUTRITION_RECOMMEND = "/open-apis/v1/glp1/nutrition_recommend"

# ===== 副作用(感受)相关 =====
ENDPOINT_FEELINGS = "/open-apis/v1/glp1/feels"
ENDPOINT_FEEL_CREATE = "/open-apis/v1/glp1/feels"
ENDPOINT_FEEL_UPDATE = "/open-apis/v1/glp1/feels_update"
ENDPOINT_FEEL_DELETE = "/open-apis/v1/glp1/feels_delete"
ENDPOINT_FEEL_LATEST = "/open-apis/v1/glp1/feels_latest"
ENDPOINT_FEEL_LIST = "/open-apis/v1/glp1/list_user_feels"

# ===== 运动相关 =====
ENDPOINT_SPORT_CATEGORIES = "/open-apis/v1/sport/categories"
ENDPOINT_SPORT_SEARCH = "/open-apis/v1/sport/search"
ENDPOINT_SPORT_RECORD = "/open-apis/v1/sport/record"
ENDPOINT_SPORT_RECORDS = "/open-apis/v1/sport/records"
ENDPOINT_SPORT_RECORD_DELETE = "/open-apis/v1/sport/record/delete"

# ===== 睡眠相关 =====
ENDPOINT_SLEEP_RECORD = "/open-apis/v1/sleep/record"
ENDPOINT_SLEEP_DELETE = "/open-apis/v1/sleep/delete"
ENDPOINT_SLEEP_RECORDS = "/open-apis/v1/sleep/records"
ENDPOINT_SLEEP_RECORDS_WITH_NAP = "/open-apis/v1/sleep/records_with_nap"
ENDPOINT_SLEEP_NAP = "/open-apis/v1/sleep/nap"
ENDPOINT_SLEEP_NAP_DELETE = "/open-apis/v1/sleep/nap/delete"

# ===== 喝水相关 =====
ENDPOINT_WATER_RECORD = "/open-apis/v1/water/record"
ENDPOINT_WATER_UPDATE = "/open-apis/v1/water/update"
ENDPOINT_WATER_DELETE = "/open-apis/v1/water/delete"
ENDPOINT_WATER_DETAIL = "/open-apis/v1/water/detail"
ENDPOINT_WATER_RECORDS = "/open-apis/v1/water/records"
ENDPOINT_WATER_LATEST = "/open-apis/v1/water/latest"

# ===== 食谱相关 =====
ENDPOINT_RECIPE_GENERATE = "/open-apis/v1/recipe/generate"
ENDPOINT_RECIPE_DETAILS = "/open-apis/v1/recipe/details"
ENDPOINT_RECIPE_REPLACE_FOODS = "/open-apis/v1/recipe/replace_foods"
ENDPOINT_RECIPE_REPLACE_FOOD = "/open-apis/v1/recipe/replace_food"
ENDPOINT_RECIPE_REPLACE_MEAL = "/open-apis/v1/recipe/replace_meal"
ENDPOINT_RECIPE_MODE_LIST = "/open-apis/v1/recipe/mode_list"
ENDPOINT_RECIPE_MODE_DETAIL = "/open-apis/v1/recipe/mode_detail"
ENDPOINT_RECIPE_SUMMARY = "/open-apis/v1/recipe/summary"

__all__ = [
    # 认证
    'ENDPOINT_ACCESS_TOKEN',
    # 食物
    'ENDPOINT_FOOD_SEARCH',
    'ENDPOINT_FOOD_DETAIL',
    'ENDPOINT_FOOD_CATEGORIES',
    'ENDPOINT_FOOD_LIST',
    'ENDPOINT_FOOD_UNITS',
    'ENDPOINT_FOOD_INGREDIENTS',
    'ENDPOINT_FOOD_RANKS',
    'ENDPOINT_FOOD_IMAGE_RECOGNIZE',
    'ENDPOINT_FOOD_IMAGE_RECOGNIZE_DETAIL',
    'ENDPOINT_FOOD_TEXT_RECOGNIZE',
    # 体重
    'ENDPOINT_WEIGHT_RECORD',
    'ENDPOINT_WEIGHT_RECORDS',
    'ENDPOINT_WEIGHT_LATEST',
    'ENDPOINT_WEIGHT_DELETE',
    'ENDPOINT_WEIGHT_LINE',
    'ENDPOINT_WEIGHT_SCALE',
    # 饮食
    'ENDPOINT_EATING_RECORD',
    'ENDPOINT_EATING_RECORD_SINGLE',
    'ENDPOINT_EATING_UPDATE',
    'ENDPOINT_EATING_DELETE',
    'ENDPOINT_EATING_RECORDS',
    'ENDPOINT_EATING_LATEST',
    'ENDPOINT_EATING_NUTRITION_RECOMMEND',
    # GLP-1 用药
    'ENDPOINT_MEDICINE_RECORD',
    'ENDPOINT_MEDICINE_RECORD_DEL',
    'ENDPOINT_MEDICINE_RECORD_UPDATE',
    'ENDPOINT_MEDICINES',
    'ENDPOINT_MEDICINE_RECORDS',
    'ENDPOINT_MEDICINE_RECORD_DETAIL',
    'ENDPOINT_MEDICINE_RECORD_LATEST',
    'ENDPOINT_GLP1_NUTRITION_RECOMMEND',
    # 副作用(感受)
    'ENDPOINT_FEELINGS',
    'ENDPOINT_FEEL_CREATE',
    'ENDPOINT_FEEL_UPDATE',
    'ENDPOINT_FEEL_DELETE',
    'ENDPOINT_FEEL_LATEST',
    'ENDPOINT_FEEL_LIST',
    # 运动
    'ENDPOINT_SPORT_CATEGORIES',
    'ENDPOINT_SPORT_SEARCH',
    'ENDPOINT_SPORT_RECORD',
    'ENDPOINT_SPORT_RECORDS',
    'ENDPOINT_SPORT_RECORD_DELETE',
    # 睡眠
    'ENDPOINT_SLEEP_RECORD',
    'ENDPOINT_SLEEP_DELETE',
    'ENDPOINT_SLEEP_RECORDS',
    'ENDPOINT_SLEEP_RECORDS_WITH_NAP',
    'ENDPOINT_SLEEP_NAP',
    'ENDPOINT_SLEEP_NAP_DELETE',
    # 喝水
    'ENDPOINT_WATER_RECORD',
    'ENDPOINT_WATER_UPDATE',
    'ENDPOINT_WATER_DELETE',
    'ENDPOINT_WATER_DETAIL',
    'ENDPOINT_WATER_RECORDS',
    'ENDPOINT_WATER_LATEST',
    # 食谱
    'ENDPOINT_RECIPE_GENERATE',
    'ENDPOINT_RECIPE_DETAILS',
    'ENDPOINT_RECIPE_REPLACE_FOODS',
    'ENDPOINT_RECIPE_REPLACE_FOOD',
    'ENDPOINT_RECIPE_REPLACE_MEAL',
    'ENDPOINT_RECIPE_MODE_LIST',
    'ENDPOINT_RECIPE_MODE_DETAIL',
    'ENDPOINT_RECIPE_SUMMARY',
]
