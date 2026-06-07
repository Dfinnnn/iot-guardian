import pandas as pd, json
df = pd.read_parquet(r"C:\Users\user\Documents\WBL-EverAI\GroupProject_IoTGuardian\IoTGuradian_Research_Coding\ICUDatasetProcessed\eda_outputs\test.parquet")
b = json.load(open(r"C:\Users\user\Documents\WBL-EverAI\GroupProject_IoTGuardian\IoTGuradian_Research_Coding\Coding\iot-guardian\data\baseline.json"))
num = lambda s: pd.to_numeric(s, errors="coerce").fillna(0.0)
w = pd.DataFrame({"ip": df["ip.src"].astype(str), "td": num(df["frame.time_delta"]),
    "win": num(df["tcp.window_size_value"]), "push": num(df["tcp.flags.push"]), "label": num(df["label"])})
w["fast"] = (w.td < b["normal_td_p05"]).astype(float)
w["malformed"] = ((w.win != 512) | (w.push != 1)).astype(float)
g = w.groupby("ip")
d = pd.DataFrame({"threat": g.fast.mean()*100, "structural": g.malformed.mean()*100, "truth": g.label.mean()*100})
# structural = primary signal (attack-exclusive, both types). threat = secondary (flood intensity).
d["score"] = (0.6*d.structural + 0.4*d.threat).round(1)
out = d.sort_values("score", ascending=False)[["score","structural","threat","truth"]].round(1)
print(out.to_string())
print("\nworst attacker:", d[d.truth==100].score.min(), " | top normal:", d[d.truth==0].score.max())