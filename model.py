import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    ### Prepare your parameters
    """)
    return


@app.cell
def _():
    import pandas as pd
    from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpInteger, LpStatus, value
    import matplotlib.pyplot as plt
    from itertools import chain, repeat

    def ncycles(iterable, n):
        "Returns the sequence elements n times"
        return chain.from_iterable(repeat(tuple(iterable), n))

    # Staff needs per Day
    n_staff = [31, 45, 40, 40, 48, 30, 25]
    # Days of the week
    jours = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Create circular list of days
    n_days = [i for i in range(7)]
    n_days_c = list(ncycles(n_days, 3))

    # Working days
    list_in = [[n_days_c[j] for j in range(i, i + 5)] for i in n_days_c]

    # Workers off by shift for each day
    list_excl = [[n_days_c[j] for j in range(i + 1, i + 3)] for i in n_days_c]
    return (
        LpMinimize,
        LpProblem,
        LpStatus,
        LpVariable,
        jours,
        list_excl,
        list_in,
        lpSum,
        n_days,
        n_staff,
        pd,
        plt,
        value,
    )


@app.cell
def _(mo):
    mo.md(r"""
    ### Initialise the model, define the objective and add constraints
    """)
    return


@app.cell
def _(
    LpMinimize,
    LpProblem,
    LpVariable,
    jours,
    list_excl,
    lpSum,
    n_days,
    n_staff,
):
    # Initialize Model
    model = LpProblem("Minimize Staffing", LpMinimize)

    # Create Variables
    start_jours = ['Shift: ' + i for i in jours]
    x = LpVariable.dicts('shift_', n_days, lowBound=0, cat='Integer')

    # Define Objective
    model += lpSum([x[i] for i in n_days])

    # Add constraints
    for d, l_excl, staff in zip(n_days, list_excl, n_staff):
        model += lpSum([x[i] for i in n_days if i not in l_excl]) >= staff
    return model, start_jours


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solve your model and analyse the results
    """)
    return


@app.cell
def _(LpStatus, jours, list_in, model, n_days, pd, start_jours, value):
    # Solve Model
    model.solve()

    # The status of the solution is printed to the screen
    print("Status:", LpStatus[model.status])

    # How many workers per day?
    dct_work = {}
    for v in model.variables():
        dct_work[int(v.name[-1])] = int(v.varValue)

    # Show Detailed Sizing per Day
    dict_sch = {}
    for day in dct_work.keys():
        dict_sch[day] = [dct_work[day] if i in list_in[day] else 0 for i in n_days]
    df_sch = pd.DataFrame(dict_sch).T
    df_sch.columns = jours
    df_sch.index = start_jours

    # The optimized objective function value is printed to the screen
    print("Total number of Staff = ", value(model.objective))
    return (df_sch,)


@app.cell
def _(df_sch):
    print(df_sch)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Heatmap Visualization (Patterns)
    """)
    return


@app.cell
def _(df_sch):
    def _():
        import seaborn as sns
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 6))
        sns.heatmap(df_sch, annot=True, fmt="d", cmap="YlGnBu", cbar_kws={'label': 'Number of Workers'})
        plt.title("Weekly Staff Schedule Heatmap")
        plt.xlabel("Day of Week")
        plt.ylabel("Shift Start Day")
        plt.xticks(rotation=45)
        plt.tight_layout()
        return plt.show()
    _()
    return


@app.cell
def _(mo):
    mo.md(r"""
    - **Shift: Monday** starts 14 workers, covering Monday to Friday.
    - **Shift: Tuesday** starts 14 workers, covering Tuesday to Saturday.
    - **Shift: Wednesday** starts 8 workers, covering Wednesday to Sunday.
    - **Shift: Thursday** has no workers starting.
    - **Shift: Friday** starts 13 workers, covering Friday to Sunday.
    - **Shift: Saturday** has no workers starting.
    - **Shift: Sunday** starts 4 workers, covering Monday to Thursday and Sunday.
    - **Highest staffing** occurs on Monday, Tuesday, and Friday (14 workers each).
    - **Lowest staffing** on Saturday and Sunday, except for Sunday shifts starting on Wednesday and Sunday.
    - **Wednesday and Friday** shifts cover the weekend (Saturday and Sunday).
    - **No overlap** from Thursday starting shifts.
    - **Sunday starting shifts** only cover Monday to Thursday and Sunday.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Daily Breakdown
    """)
    return


@app.cell
def _(df_sch, plt):
    df_sch.T.plot(kind='bar', stacked=True, figsize=(12, 6), colormap="tab20c")
    plt.title("Daily Staffing Breakdown by Shift Start Day")
    plt.xlabel("Day of Week")
    plt.ylabel("Number of Workers")
    plt.xticks(rotation=45)
    plt.legend(title="Shift Start Day", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    return


@app.cell
def _(mo):
    mo.md(r"""
    - **Monday staffing** is primarily covered by workers starting on Monday and Sunday, with smaller contributions from Friday.
    - **Tuesday staffing** is highest, with major contributions from Monday, Tuesday, and Friday starting shifts.
    - **Wednesday staffing** is evenly distributed among Monday, Tuesday, Wednesday, and Sunday starting shifts.
    - **Thursday staffing** is mainly covered by Monday, Tuesday, and Wednesday starting shifts.
    - **Friday staffing** peaks, with large contributions from Monday, Tuesday, Wednesday, and Friday starting shifts.
    - **Saturday staffing** is mostly covered by Tuesday and Friday starting shifts, with no contribution from Monday or Thursday.
    - **Sunday staffing** is mainly covered by Wednesday and Friday starting shifts, with a notable contribution from Sunday.
    - **Shift: Monday** workers consistently cover Monday to Friday.
    - **Shift: Tuesday** workers cover Tuesday to Saturday, with the highest impact on Tuesday and Friday.
    - **Shift: Wednesday** workers cover Wednesday to Sunday, with a significant presence on Wednesday, Thursday, and Friday.
    - **Shift: Friday** workers significantly contribute to Friday, Saturday, and Sunday staffing.
    - **Shift: Sunday** workers only appear on Monday and Sunday.
    - **Shift: Thursday** workers do not appear to contribute to any day in this chart.
    - **Shift: Saturday** workers do not appear to contribute to any day in this chart.
    - **Friday** has the highest total staffing level across the week.
    - **Sunday** has the lowest total staffing level, with only Wednesday and Friday starting shifts contributing.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Total Workers per Day
    """)
    return


@app.cell
def _(df_sch, plt):
    df_sch.sum(axis=0).plot(kind='bar', figsize=(10, 5), color='skyblue')
    plt.title("Total Workers per Day")
    plt.xlabel("Day of Week")
    plt.ylabel("Number of Workers")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(mo):
    mo.md(r"""
    - **Monday** has the lowest staffing level, with around 30 workers.
    - **Tuesday** sees a significant increase in staffing, reaching approximately 45 workers.
    - **Wednesday and Thursday** maintain a consistent staffing level of around 40 workers each.
    - **Friday** has the highest staffing level, peaking at about 50 workers.
    - **Saturday** experiences a drop in staffing, with around 35 workers.
    - **Sunday** has the second-lowest staffing level, with just over 25 workers.
    - Staffing levels increase from Monday to Friday, indicating higher demand or workload towards the end of the workweek.
    - There is a noticeable decline in staffing levels during the weekend, with Sunday having the least number of workers.
    - The staffing pattern suggests a focus on weekdays, especially Friday, likely due to higher business or operational needs.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
