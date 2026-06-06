import pandas as pd

df = pd.read_parquet(r"C:\Users\user\Documents\WBL-EverAI\GroupProject_IoTGuardian\IoTGuradian_Research_Coding\ICUDatasetProcessed\eda_outputs\test.parquet")

print(df.shape)
print(df.columns.tolist())
print("\n--- display cols check ---")
for col in ["ip.src", "ip.dst", "mqtt.topic", "mqtt.clientid"]:
    print(col, "EXISTS" if col in df.columns else "MISSING")

print("\n--- mqtt.clientid in attack rows ---")
attack = df[df["label"] == 1]
print(attack["mqtt.clientid"].value_counts().head(10))
print("null count:", attack["mqtt.clientid"].isna().sum())

print(df["ip.src"].value_counts())
print(df[df["label"]==0]["ip.src"].value_counts())