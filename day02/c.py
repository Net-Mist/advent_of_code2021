import pandas as pd

df = pd.read_csv("input.txt", header=None, delimiter=" ")
df.columns = ["action", "n"]
position_h = df.query("action == 'forward'").n.sum()
depth = df.query("action == 'down'").n.sum() - df.query("action == 'up'").n.sum()
print("part 1:", position_h * depth)

df["aim"] = (((df.action == "down") - (df.action == "up") * 1) * df.n).cumsum()
df = df.query("action == 'forward'")
print("part 2:", df.n.sum() * (df.n * df.aim).sum())
