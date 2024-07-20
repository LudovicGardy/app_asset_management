from openai import OpenAI
from types import SimpleNamespace

from ..calculs import calculate_savings, calculate_mortgage

def chatbot_GPT(self, st, **kwargs):
        params = SimpleNamespace(**kwargs)

        st.divider()

        st.header('Posez vos questions à l\'assistant virtuel')

        onglet_actif = "Épargne" if params.tab1 else "Achat" if params.tab2 else "Non défini"
        simulation_effectuee = params.submit_savings if params.tab1 else params.submit_mortgage if params.tab2 else False

        if not simulation_effectuee:
            if onglet_actif == "Épargne":
                # Appel de la fonction calculate_savings avec des valeurs par défaut ou celles saisies par l'utilisateur
                x_savings, capital_accumulated, savings_accumulated, interest_accumulated, final_capital = calculate_savings(params.P_savings, params.E_savings, params.n_years_savings, params.r_annual_savings, params.months_between_savings)
                preprompt = f"""
                Tu es un assistant virtuel spécialisé dans le conseil financier, particulièrement expérimenté dans les stratégies d'épargne. Tu aides les utilisateurs à optimiser leurs plans d'épargne 
                en fonction de leurs objectifs à long terme. Actuellement, tu es en train d'assister un utilisateur qui envisage un plan d'épargne. 
                
                Voici les détails de sa simulation :
                - Placement initial : {params.P_savings}€
                - Épargne périodique : {params.E_savings}€ tous les {params.months_between_savings} mois
                - Durée du placement : {params.n_years_savings} ans
                - Taux de rendement annuel estimé : {params.r_annual_savings*100}%

                Voici les résultats : 
                - Capital final après {params.n_years_savings} ans : {final_capital}€
                - Épargne totale : {savings_accumulated[-1]}€
                - Intérêts totaux : {interest_accumulated[-1]}€
                - Capital total : {capital_accumulated[-1]}€

                L'utilisateur cherche à comprendre comment maximiser le rendement de son épargne au fil des ans et souhaite des conseils sur les meilleures stratégies d'épargne pour atteindre ses objectifs financiers. 
                Ton rôle est de fournir des analyses, des recommandations personnalisées, et de répondre à ses questions de manière claire et informative, tout en utilisant un langage accessible et amical. 
                Pense à souligner l'importance de la discipline d'épargne, des avantages du rendement composé, et à proposer des ajustements stratégiques si nécessaire.
                """
            elif onglet_actif == "Achat":
                # Appel de la fonction calculate_mortgage avec des valeurs par défaut ou celles saisies par l'utilisateur
                monthly_payment, principal_paid, interest_paid, remaining_balance, total_interest, M = calculate_mortgage(params.P_mortgage, params.annual_interest_rate_mortgage, params.years_mortgage)
                preprompt = f"""
                Tu es un expert immobilier virtuel, doté d'une grande expertise dans le domaine des achats immobiliers. Tu assistes les utilisateurs dans l'évaluation de leurs options d'achat immobilier, 
                en tenant compte de leurs capacités financières et de leurs objectifs à long terme. 
                
                Voici les détails de la simulation d'achat de l'utilisateur :
                - Montant du prêt : {params.P_mortgage}€
                - Taux d'intérêt annuel : {params.annual_interest_rate_mortgage*100}%
                - Durée du prêt : {params.years_mortgage} ans
                - Échéance mensuelle calculée : {M}€
                - Total des intérêts payés sur la période du prêt : {total_interest}€

                L'utilisateur souhaite des conseils sur l'achat immobilier, notamment sur la manière de choisir le meilleur prêt immobilier, d'évaluer le coût total de l'achat, 
                et de planifier son budget à long terme. Ton rôle est d'offrir des insights pertinents sur le marché immobilier, des stratégies pour négocier les meilleures conditions de prêt, 
                et d'expliquer les implications financières de l'achat immobilier. Ta réponse doit être informative, personnalisée, et exprimée dans un langage compréhensible pour 
                faciliter la prise de décision de l'utilisateur.
                """

        openai_api_key = st.text_input("Entrez votre clé API OpenAI", type="password")

        # .streamlit/secrets.toml
        client = OpenAI(api_key=openai_api_key)

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": preprompt}]

            first_message = {"role": "assistant", "content": f"Bonjour, je suis votre conseiller financier virtuel. Comment puis-je vous aider aujourd'hui ?"}
            st.session_state.messages.append(first_message)

        for message in st.session_state.messages:
            if "assistant" in message["role"] or "user" in message["role"]:
                with st.chat_message(message["role"]):
                        st.markdown(message["content"]) 

        if prompt := st.chat_input("Message à l'assistant virtuel"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): 
                st.markdown(prompt)

                # print(num_tokens_from_string(preprompt+prompt, "cl100k_base"))

            if not openai_api_key:
                st.warning("Veuillez entrer une clé API pour continuer.")
            else:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    for response in client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        # messages=[
                        #     {"role": "user", "content": preprompt+prompt}
                        #     for m in st.session_state.messages
                        # ],
                        stream=True,
                    ):
                        full_response += (response.choices[0].delta.content or "")
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            all_msgs = [m["content"] for m in st.session_state.messages]
            all_msgs = " ".join(all_msgs)