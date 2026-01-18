# Staff Scheduling Optimization

**Objective:**
Minimize total staff while meeting daily requirements using linear programming.

---

## 📌 Overview
- **Problem:** Assign workers to shifts to meet daily staffing needs with minimal total staff.
- **Tools:** Python, PuLP, Pandas, Matplotlib, Seaborn.
- **Methods:** Linear programming, data visualization, constraint optimization.

---

## 📊 Results
- **Optimal Staff:** 53 workers (minimum required).
- **Visualizations:**

  ![Heatmap (Shift Coverage)](/results/heatmap.png)
  *Heatmap showing shift coverage.*

  ![Bar Chart (Daily Staffing)](/results/Daily Breakdown.png)
  *Bar chart of daily staffing requirements.*

  ![Stacked Bar (Shift Contributions)](/results/Total Workers per Day.png)
  *Stacked bar chart of shift contributions.*

---

## 📂 Files
   File/Folder       | Description                                      |
 |-------------------|--------------------------------------------------|
 | `main.py`         | Main script to run the optimization model.       |
 | `model.py`        | Contains the linear programming model and logic. |
 | `pyproject.toml`  | Project dependencies and configuration.          |
 | `uv.lock`         | Lock file for dependencies.                      |
 | `README.md`       | Project documentation.                           |

---

## 🛠️ How to Run
1. Clone this repo.
2. Install dependencies:
   ```bash
   pip install -e .
