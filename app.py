import streamlit as st
from math import sqrt

st.set_page_config(page_title="玄学投点计算器", page_icon="💻")

if "classInfo" not in st.session_state:
    st.session_state["classInfo"] = []
if "totalPoints" not in st.session_state:
    st.session_state["totalPoints"] = 99
if "classNum" not in st.session_state:
    st.session_state["classNum"] = 3


def errorGen(actual, rounded):
    divisor = sqrt(1.0 if actual < 1.0 else actual)
    return (actual - rounded) ** 2 / divisor


def roundToSum(weights, expectedSum):
    rounded = [int(w) for w in weights]
    rest = int(expectedSum - sum(rounded))
    errors = [
        (errorGen(w, r + 1) - errorGen(w, r), i)
        for w, r, i in zip(weights, rounded, range(len(weights)))
    ]
    rank = sorted(errors, key=lambda x: x[0])
    for i in range(rest):
        rounded[rank[i][1]] += 1
    return rounded


def CalculatePoints() -> list:
    # inflation = selected / limited
    # overhead = sqrt(selected / limited)
    # redundancy = inflation ** 2
    # weight = inflation * overhead + redundancy
    # points = totalPoints * weight / sum(weight)

    weight = [
        ((info[1] / info[0]) * sqrt(info[1] - info[0]) if info[1] > info[0] else 0)
        + ((info[1] / info[0]) ** 2 if info[1] <= info[0] else 0)
        for info in st.session_state["classInfo"]
    ]
    if sum(weight) == 0:
        return [0] * st.session_state["classNum"]
    return roundToSum(
        [
            st.session_state["totalPoints"] * weight[i] / sum(weight)
            for i in range(len(st.session_state["classInfo"]))
        ],
        st.session_state["totalPoints"],
    )


def saveChange() -> None:
    for i in range(int(st.session_state["classNum"])):
        st.session_state["classInfo"].append(
            (
                st.session_state[f"{i}_limit"],
                st.session_state[f"{i}_select"],
            )
        )


HEADER = st.container()
BODY = st.columns([1, 3, 3, 3])
FOOTER = st.container()

with HEADER:
    st.title("玄学投点计算器")
    colLeft, colRight = st.columns(2)
    with colLeft:
        st.number_input("待投点课程数", min_value=1, max_value=30, step=1, key="classNum")
    with colRight:
        st.number_input("可用点数", min_value=1, max_value=99, step=1, key="totalPoints")
    st.markdown("---")

with BODY[0]:
    st.subheader("序号")
with BODY[1]:
    st.subheader("限数")
with BODY[2]:
    st.subheader("已选")
with BODY[3]:
    st.subheader("玄学投点")

for i in range(int(st.session_state["classNum"])):
    with BODY[0]:
        st.markdown(f"# {i + 1}")
    with BODY[1]:
        st.number_input(
            "",
            value=3,
            min_value=1,
            max_value=999,
            step=1,
            key=f"{i}_limit",
        )
    with BODY[2]:
        st.number_input(
            "",
            value=5,
            min_value=1,
            max_value=999,
            step=1,
            key=f"{i}_select",
        )

st.session_state["classInfo"] = []
saveChange()
pts = CalculatePoints()

with BODY[3]:
    for i in range(int(st.session_state["classNum"])):
        st.markdown(f"# {pts[i]}")

with FOOTER:
    st.markdown("---")
    st.markdown(
        'Email:<a href="mailto:huang_nan_2019@pku.edu.cn">huang_nan_2019@pku.edu.cn</a>',
        unsafe_allow_html=True,
    )
