import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "SUPABASE_URL and SUPABASE_KEY are missing from the .env file."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def sign_up(email: str, password: str):
    return supabase.auth.sign_up(
        {
            "email": email,
            "password": password,
        }
    )


def sign_in(email: str, password: str):
    return supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
    )


def sign_out():
    supabase.auth.sign_out()


def get_current_user():
    return supabase.auth.get_user()


def save_analysis_history(
    user_id: str,
    analysis_type: str,
    result: str
):
    return supabase.table("analysis_history").insert({
        "user_id": user_id,
        "analysis_type": analysis_type,
        "result": result
    }).execute()


def get_analysis_history(user_id: str):
    return (
        supabase
        .table("analysis_history")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

def delete_analysis_history(user_id: str, record_id: str):
    return (
        supabase
        .table("analysis_history")
        .delete()
        .eq("id", record_id)
        .eq("user_id", user_id)
        .execute()
    )


def delete_all_analysis_history(user_id: str):
    return (
        supabase
        .table("analysis_history")
        .delete()
        .eq("user_id", user_id)
        .execute()
    )