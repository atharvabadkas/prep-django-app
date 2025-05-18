#!/usr/bin/env python
"""
Script to run Django migrations.
"""
import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_prepapp.settings')
django.setup()

# Run migrations
from django.core.management import call_command
print("Making migrations...")
call_command('makemigrations')
print("Applying migrations...")
call_command('migrate')
print("Migrations complete!") 