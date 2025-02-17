import numpy as np
import seaborn as sns
import streamlit as st

from ..AI.GPT import chatbot_GPT
from ..calculs import calculate_mortgage, calculate_savings
from ..config import page_config
from ..plots import plot_mortgage, plot_savings
from .ui_components import display_sidebar, init_page_config, init_session_state

sns.set_theme(style="whitegrid", palette="pastel")


class App:
    def __init__(self):
        self.openai_api_key: str
        init_page_config(page_config)
        self = display_sidebar(self, page_config)
        init_session_state()
        self.run()

    def run(self):
        tab1, tab2 = st.tabs(["Épargne", "Achat"])

        with tab1:
            st.header("[TEST2] Paramètres de l'épargne")
            with st.form("savings_form"):
                P_savings = st.number_input(
                    "Placement de départ (€)", value=10000, step=1000
                )
                E_savings = st.number_input(
                    "Épargne périodique (€)", value=500, step=100
                )
                months_between_savings = st.selectbox(
                    "Fréquence des versements",
                    options=[1, 3, 6, 12],
                    format_func=lambda x: f"{int(12/x)} fois par an",
                )

                col1, col2 = st.columns(2)

                with col1:
                    r_annual_savings = st.number_input(
                        "Taux de rendement annuel", value=0.08, step=0.01
                    )
                with col2:
                    n_years_savings = st.slider(
                        "Durée du placement (années)", 1, 30, 20
                    )

                submit_savings = st.form_submit_button("Calculer")

            if submit_savings:
                (
                    x_savings,
                    capital_accumulated,
                    savings_accumulated,
                    interest_accumulated,
                    final_capital,
                ) = calculate_savings(
                    P_savings,
                    E_savings,
                    n_years_savings,
                    r_annual_savings,
                    months_between_savings,
                )
                plt = plot_savings(
                    x_savings,
                    capital_accumulated,
                    savings_accumulated,
                    interest_accumulated,
                    "Évolution de l'épargne au fil des années",
                    [
                        "Capital Total",
                        "Participation Épargne",
                        "Participation Intérêts",
                    ],
                )
                st.pyplot(plt)
                st.write(
                    f"Capital final après {n_years_savings} ans : {final_capital:,.2f}€".replace(
                        ",", " "
                    )
                )  # Formatting for thousands separator

        with tab2:
            st.header("Paramètres de l'achat")
            with st.form("mortgage_form"):
                P_mortgage = st.number_input(
                    "Montant du prêt (€)",
                    value=316000,
                    step=1000,
                    key="mortgage_amount",
                )
                st.caption(
                    "Pensez à compter les frais de notaire et de garantie dans le montant du prêt. Par exemple pour un bien à 350 000€, comptez 10% de frais soit 35 000€. Vous devrez donc emprunter 350 000€ + 35 000€ = 385 000€. Si vous avez un apport de 20 000€, vous devrez emprunter 365 000€."
                )

                col1, col2 = st.columns(2)

                with col1:
                    annual_interest_rate_mortgage = st.number_input(
                        "Taux d'intérêt annuel",
                        value=0.039,
                        step=0.001,
                        key="mortgage_rate",
                    )
                with col2:
                    years_mortgage = st.slider(
                        "Durée du prêt (années)", 1, 30, 25, key="mortgage_years"
                    )

                submit_mortgage = st.form_submit_button("Calculer")

            if submit_mortgage:
                (
                    monthly_payment,
                    principal_paid,
                    interest_paid,
                    remaining_balance,
                    total_interest,
                    M,
                ) = calculate_mortgage(
                    P_mortgage, annual_interest_rate_mortgage, years_mortgage
                )
                months = np.arange(1, years_mortgage * 12 + 1)

                # Conversion des données mensuelles en annuelles pour le tracé
                years_arr = np.arange(1, years_mortgage + 1)
                annual_interest_paid = np.array(
                    [
                        sum(interest_paid[i * 12 : (i + 1) * 12])
                        for i in range(years_mortgage)
                    ]
                )
                annual_principal_paid = np.array(
                    [
                        sum(principal_paid[i * 12 : (i + 1) * 12])
                        for i in range(years_mortgage)
                    ]
                )

                # Le solde restant à la fin de chaque année (prendre le dernier mois de chaque année)
                annual_remaining_balance = remaining_balance[11::12]
                annual_total_paid = annual_principal_paid + annual_interest_paid

                plt = plot_mortgage(
                    years_arr,
                    annual_remaining_balance,
                    annual_interest_paid,
                    annual_principal_paid,
                    annual_total_paid,
                    "Échéancier du prêt sur 20 ans (Résumé Annuel)",
                )
                st.pyplot(plt)
                st.write(
                    f"Total des intérêts payés sur la période du prêt : {total_interest:,.2f}€".replace(
                        ",", " "
                    )
                )  # Formatting for thousands separator
                st.write(f"Échéance mensuelle : {M:,.2f}€".replace(",", " "))

        kwargs = {
            "P_savings": P_savings,
            "E_savings": E_savings,
            "n_years_savings": n_years_savings,
            "r_annual_savings": r_annual_savings,
            "months_between_savings": months_between_savings,
            "submit_savings": submit_savings,
            "P_mortgage": P_mortgage,
            "annual_interest_rate_mortgage": annual_interest_rate_mortgage,
            "years_mortgage": years_mortgage,
            "submit_mortgage": submit_mortgage,
            "tab1": tab1,
            "tab2": tab2,
        }

        if self.openai_api_key:
            chatbot_GPT(self, st, **kwargs)


if __name__ == "__main__":
    app = App()
