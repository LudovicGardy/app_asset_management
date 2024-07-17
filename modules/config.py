import os
from dotenv import load_dotenv, find_dotenv

def load_configurations():
    """
    Charge uniquement les variables du fichier .env si celui-ci est présent.
    Si le fichier .env n'existe pas, charge toutes les variables d'environnement du système.
    """
    dotenv_path = find_dotenv('.env')

    if dotenv_path:
        # The .env file exists, load only its variables
        load_dotenv(dotenv_path)
        # Return the variables loaded from the .env
        return {key: os.environ[key] for key in os.environ if key in open(dotenv_path).read()}
    else:
        # The .env file does not exist, return all the system environment variables
        return dict(os.environ)

def page_config():
    '''
    Set the page configuration (title, favicon, layout, etc.)
    '''
    env_variables = load_configurations()

    page_dict = {
        'page_title': '# Pro Actifs',
        'page_subtitle': '### Gestion patrimoniale',
        'author': 'Sotis AI',
        'base': 'dark',
        'page_icon': f'{env_variables["AWS_S3_URL"]}/Sotis_AI_pure_darkbg_240px.ico',
        'page_logo': f'{env_variables["AWS_S3_URL"]}/Sotis_AI_pure_darkbg_240px.png',
        'layout': 'wide',
        'initial_sidebar_state': 'auto',
        'markdown': '''<style>.css-10pw50 {visibility:hidden;}</style>''',
        'page_description': '''
        Cette application de gestion patrimoniale permet aux utilisateurs de simuler des plans d'épargne et des scénarios d'achat immobilier.
        Fonctionnalités proposées :
        - Simulation de l'évolution de l'épargne avec des contributions périodiques et des taux de rendement.
        - Calcul des remboursements hypothécaires, y compris le principal et les intérêts payés au fil du temps.
        - Visualisation graphique des résultats pour une compréhension claire et rapide.
        
        Développée en 2024 par L. Gardy, Data Scientist indépendant chez [Sotis A.I.](https://www.sotisanalytics.com), cette application offre une interface conviviale pour l'analyse financière personnelle.
        '''
    }

    return page_dict

def AWS_credentials():
    keys_list = [
        'AWS_S3_URL'
    ]

    cred_dict = {}
    env_variables = load_configurations()

    # Check if all required keys exist and have a non-empty value
    try:
        for key in keys_list:
            value = env_variables.get(key.upper())
            if not value:
                raise ValueError(f'Missing or empty value for key: {key}')
            cred_dict[key] = value
    except ValueError as e:
        print(f'Configuration error: {e}')
        cred_dict = {}  # Reset cred_dict if any key is missing or empty

    return cred_dict