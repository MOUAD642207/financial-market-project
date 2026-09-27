"""
hello_world_dag.py
------------------
Premier DAG simple pour comprendre la structure Airflow.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


# ============================================================
# FONCTIONS PYTHON
# ============================================================

def say_hello():
    """Affiche un message dans les logs."""
    print("=" * 60)
    print("Bonjour depuis Airflow !")
    print("=" * 60)


def say_goodbye():
    """Affiche un autre message."""
    print("=" * 60)
    print("Au revoir depuis Airflow !")
    print("=" * 60)


# ============================================================
# DÉFINITION DU DAG
# ============================================================

# Paramètres par défaut
default_args = {
    "owner": "admin",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Création du DAG
with DAG(
    dag_id="hello_world",
    default_args=default_args,
    description="Un DAG simple pour dire bonjour",
    schedule="@daily",           # Tous les jours
    start_date=datetime(2026, 9, 25),
    catchup=False,               # Ne pas rattraper les exécutions passées
    tags=["test", "hello"],
) as dag:

    # Task 1 : dire bonjour
    task_hello = PythonOperator(
        task_id="say_hello",
        python_callable=say_hello,
    )

    # Task 2 : dire au revoir
    task_goodbye = PythonOperator(
        task_id="say_goodbye",
        python_callable=say_goodbye,
    )

    # Ordre d'exécution
    task_hello >> task_goodbye