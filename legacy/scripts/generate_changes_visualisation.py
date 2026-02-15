import os
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import glob


def parse_backup_timestamp(filename):
    """Extracts datetime from 'edt_backup_YYYYMMDD_HHMMSS.csv'"""
    basename = os.path.basename(filename)
    timestamp_part = basename.replace("edt_backup_", "").replace(".csv", "")
    try:
        return datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
    except ValueError:
        return None


def main():
    backup_dir = "backups"
    log_dir = "logs"
    viz_file = "history_viz.html"
    log_file = os.path.join(log_dir, "changes.log")

    # 1. Gather all backups
    backup_files = sorted(glob.glob(os.path.join(backup_dir, "*.csv")))

    if not backup_files:
        print("No backups found in 'backups/' directory. Run backup_edt.py first.")
        return

    history_data = []

    print(f"Analyzing {len(backup_files)} backups...")

    for f in backup_files:
        ts = parse_backup_timestamp(f)
        if ts is None:
            continue

        df = pd.read_csv(f)
        # Calculate some metrics
        # We assume 'delta' column exists for hours
        total_hours = pd.to_numeric(df["delta"], errors="coerce").sum()

        history_data.append(
            {
                "timestamp": ts,
                "total_hours": total_hours,
                "filename": os.path.basename(f),
            }
        )

    if not history_data:
        print("No valid backup data processed.")
        return

    hist_df = pd.DataFrame(history_data).sort_values("timestamp")

    # 2. Generate Visualisation (Plotly)
    fig = go.Figure()

    # Total Hours Trace
    fig.add_trace(
        go.Scatter(
            x=hist_df["timestamp"],
            y=hist_df["total_hours"],
            mode="lines+markers",
            name="Total Hours",
            line=dict(color="firebrick", width=4),
        )
    )

    fig.write_html(viz_file)
    print(f"Visualization saved to: {viz_file}")

    # 3. Generate Log File
    with open(log_file, "w", encoding="utf-8") as lf:
        lf.write(f"TIMETABLE CHANGE HISTORY LOG")
        lf.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lf.write("=" * 50 + "")

        prev_hours = None
        prev_count = None

        for i, row in hist_df.iterrows():
            ts_str = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            lf.write(f"[{ts_str}] File: {row['filename']}")
            lf.write(f"  - Total Hours: {row['total_hours']:.2f}h")

            if prev_hours is not None:
                diff = row["total_hours"] - prev_hours
                lf.write(f" ({'+' if diff >= 0 else ''}{diff:.2f}h change)")

            lf.write("" + "-" * 30 + "")

            prev_hours = row["total_hours"]

    print(f"Change log updated at: {log_file}")


if __name__ == "__main__":
    main()
