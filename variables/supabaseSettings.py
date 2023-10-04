import os
from supabase import create_client, Client
from variables.apiKeys import SUPABASE_API_KEY

url: str = 'https://citeifmttmdotbcsotyh.supabase.co'
key: str = SUPABASE_API_KEY

supabase: Client = create_client(url, key)