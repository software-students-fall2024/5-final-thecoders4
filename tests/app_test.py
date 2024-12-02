"""
This module contains unit tests for ml-client.
"""

import os
import pytest
from flask import session
from pymongo import MongoClient
from app import create_app

