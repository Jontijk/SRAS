
import streamlit as st
import math
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import io

from sras.utils.response_formatter import format_response, show_synthesis_progress

# Safe evaluation for basic expressions
def safe_eval(expr):
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    try:
        return eval(expr, {"__builtins__": {}}, allowed_names)
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Symbolic math using sympy
def symbolic_simplify(expr):
    try:
        symbolic_expr = sp.sympify(expr)
        return sp.simplify(symbolic_expr)
    except Exception as e:
        return f"⚠️ SymPy Error: {str(e)}"

# Unit conversion (simple)
def unit_convert(expr):
    try:
        parts = expr.split(" to ")
        if len(parts) != 2:
            return "⚠️ Format should be like '100 cm to m'"
        value, from_unit = parts[0].strip().split()
        value = float(value)
        to_unit = parts[1].strip()

        conversion_factors = {
            ("cm", "m"): 0.01,
            ("m", "cm"): 100,
            ("kg", "g"): 1000,
            ("g", "kg"): 0.001,
            ("inch", "cm"): 2.54,
            ("cm", "inch"): 1 / 2.54,
        }

        factor = conversion_factors.get((from_unit, to_unit))
        if factor:
            return f"{value * factor} {to_unit}"
        else:
            return "⚠️ Conversion not supported."
    except Exception as e:
        return f"⚠️ Conversion Error: {str(e)}"

# Plotting function
def plot_expression(expr):
    x = sp.symbols('x')
    try:
        symbolic_expr = sp.sympify(expr)
        f = sp.lambdify(x, symbolic_expr, "numpy")
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=f"${{sp.latex(symbolic_expr)}}$")
        ax.set_title("📈 Graph of Expression")
        ax.legend()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"⚠️ Plot Error: {str(e)}")

# Streamlit UI
def calculation_ui():
    st.subheader("🔢 Calculation Agent")

    expr = st.text_input("🧮 Enter a math expression or conversion (e.g., `2 + 3 * sqrt(16)`, `100 cm to m`, `x**2 + 3*x + 2`)")

    if "history" not in st.session_state:
        st.session_state.history = []

    if st.button("🧠 Evaluate"):
        if not expr.strip():
            st.warning("Please enter a valid expression.")
            return

        show_synthesis_progress()

        result = safe_eval(expr)
        if "to" in expr:
            result = unit_convert(expr)
        elif "x" in expr or "^" in expr or "**" in expr:
            simplified = symbolic_simplify(expr)
            result = f"Simplified: {simplified}"
            plot_expression(expr)

        try:
            st.latex(sp.latex(sp.sympify(expr)))
        except:
            pass

        format_response("calculation", result)
        st.session_state.history.append((expr, result))

    # History and download
    if st.checkbox("📜 Show History"):
        for i, (e, r) in enumerate(st.session_state.history, 1):
            st.markdown(f"**{i}.** `{e}` → `{r}`")

    if st.session_state.history:
        if st.download_button("💾 Download History",
                              data="\n".join([f"{e} = {r}" for e, r in st.session_state.history]),
                              file_name="calculation_history.txt"):
            st.success("📥 History downloaded!")
