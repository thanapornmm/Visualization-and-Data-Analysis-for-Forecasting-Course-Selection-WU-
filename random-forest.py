# นำเข้าไลบรารีที่จำเป็น
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from joblib import dump

# โหลดข้อมูล
df = pd.read_excel("resampled_dataset.xlsx")

# แยกฟีเจอร์และเป้าหมาย
X = df[['S_RANK', 'P_ID', 'R_ID', 'FEE_NAME', 'S_PARENT', 'GPA', 'GPA_MATCH', 'GPA_SCI']]
y = df['BRANCH']

# แบ่งข้อมูลเป็นชุดฝึกฝนและชุดทดสอบ
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=17)

# สร้างและฝึกฝนโมเดล RandomForestClassifier
rf = RandomForestClassifier(bootstrap= False, n_estimators=300, max_depth=30, min_samples_leaf=1, min_samples_split=2, random_state=17)
rf.fit(X_train, y_train)

# ทำนายและประเมินโมเดล
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')  # ปรับสำหรับ multi-class
recall = recall_score(y_test, y_pred, average='weighted')  # ปรับสำหรับ multi-class
f1 = f1_score(y_test, y_pred, average='weighted')

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")

# บันทึกโมเดลโดยใช้ joblib
model_path = "CES_RANDOM_FOREST_MODEL.pkl"  # คุณยังสามารถใช้นามสกุลไฟล์ .pkl กับ joblib ได้
dump(rf, model_path)

print(f"model soved {model_path}")
