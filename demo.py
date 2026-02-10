import subprocess

subprocess.run(["uv", "run", "src/scripts/parse_edt.py"])
subprocess.run(["uv", "run", "src/scripts/draw_df.py"])
subprocess.run(["uv", "run", "src/calcul/draw_stat_sheet.py"])


p1 = subprocess.Popen(
    [
        "uv",
        "run",
        "src/scripts/display_prof_edt.py",
        "--prof",
        "Marc Lang",
    ]
)


p2 = subprocess.Popen(
    [
        "uv",
        "run",
        "src/scripts/display_prof_edt.py",
        "--prof",
        "Séraphine Grellier",
    ]
)

p1.wait()
p2.wait()
