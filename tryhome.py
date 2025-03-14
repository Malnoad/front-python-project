from nicegui import ui
from typing import Dict, List
import json
from dictionary import DictionaryUI  # Assuming this is the correct UI component
from frontendflash import FlashcardStudyPanel  # Correct Flashcard UI component
from backend import FlashcardManager  # Ensure FlashcardManager is imported
from dictation_sql import Dictation  # Ensure Dictation is imported

class DashboardApp:
    def __init__(self):
        # Configuration
        self.menu_items: List[Dict] = [
            {"name": "Dictionary", "icon": "school", "url": "/dictionary", "description": "Look up words and definitions"},
            {"name": "Flashcard", "icon": "style", "url": "/flashcard", "description": "Practice with flashcards"},
            {"name": "Reading", "icon": "menu_book", "url": "/reading", "description": "Read and comprehend texts"},
            {"name": "Dictation", "icon": "record_voice_over", "url": "/dictation", "description": "Practice listening and writing"},
            {"name": "Process", "icon": "insights", "url": "/process", "description": "Track your learning progress"}
        ]

        self.nav_items: List[Dict] = [
            {"name": "Home", "url": "/", "icon": "home"},
            {"name": "Explore", "url": "/explore", "icon": "explore"},
            {"name": "Help", "url": "/help", "icon": "help"}
        ]

        # State management
        self.notifications = []
        self.user_settings = self.load_user_settings()

    def load_user_settings(self) -> Dict:
        try:
            with open('user_settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "notifications_enabled": True,
                "sidebar_collapsed": False
            }

    def save_user_settings(self):
        with open('user_settings.json', 'w') as f:
            json.dump(self.user_settings, f)

    def create_sidebar(self):
        sidebar_style =  '''
        background: linear-gradient(180deg, 
                rgba(255,255,255,0.8) 0%, 
                rgba(249,250,251,0.9) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid rgba(0,0,0,0.1);
            height: 100vh
        '''

        with ui.column().classes('w-64 h-screen').style(sidebar_style):
            # Logo section
            with ui.row().classes('p-6 items-center justify-between w-full'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('auto_stories').classes('text-3xl text-pink-600')
                    ui.label('MYMY').classes('text-2xl font-bold text-pink-600')

            ui.separator().classes('mb-4')

            # Menu items
            for item in self.menu_items:
                with ui.row().classes(
                    'mx-4 p-3 rounded-xl transition-all duration-200 cursor-pointer ' +
                    ('hover:bg-pink-100')
                ):
                    ui.icon(item['icon']).classes('text-xl text-pink-600')
                    with ui.column().classes('ml-3 flex-1'):
                        ui.link(item['name'], item['url']).classes('font-semibold text-gray-700 no-underline')
                        ui.label(item['description']).classes('text-xs text-gray-500')

            # Bottom section
            with ui.row().classes('mt-auto p-4 w-full items-center justify-between'):
                ui.button(icon='settings', color='pink').props('flat')

    def create_header(self):
        header_style = '''
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        '''

        with ui.row().style('width: 156%; height: 80px; padding: 20px;').classes('items-center justify-between').style(header_style):
            # Navigation items
            with ui.row().classes('space-x-6'):
                for item in self.nav_items:
                    with ui.row().classes('items-center gap-2'):
                        ui.icon(item['icon']).classes('text-pink-600')
                        ui.link(item['name'], item['url']).classes(
                            'text-gray-700 hover:text-pink-600 transition-colors duration-200'
                        )

            # Right side elements
            with ui.row().classes('items-center gap-4'):
                with ui.row().classes('relative'):
                    ui.input(placeholder='Search...').props('rounded outlined dense').classes(
                    'w-64 bg-gray-100 border border-pink-500'
                    ).style('border-radius: 20px;')
                    ui.icon('search').classes('absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400')

                ui.button(icon='notifications', color='pink').props('flat round')
                ui.avatar('User').style('background: linear-gradient(135deg, #6366f1, #a855f7);')

    def create_main_content(self):
        
        with ui.column().style('width: 156%; height: 80px; padding: 20px;').classes('p-8 flex-1').style('background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(20px);'):
            # Welcome section
            with ui.row().classes('items-center justify-between mb-8'):
                with ui.column():
                    ui.label('Welcome back, User!').classes('text-3xl font-bold text-gray-800')
                    ui.label("Here's what's happening with your learning progress").classes('text-gray-500 mt-1')
                ui.button('Start Learning', color='pink').props('rounded').classes('px-6')

            # Stats cards
            with ui.row().classes('gap-6 mb-8'):
                stats = [
                    {'label': 'Words Learned', 'value': '1,234', 'icon': 'school', 'trend': '+12%'},
                    {'label': 'Practice Sessions', 'value': '56', 'icon': 'trending_up', 'trend': '+5%'},
                    {'label': 'Study Streak', 'value': '7 days', 'icon': 'local_fire_department', 'trend': '+2 days'},
                    {'label': 'Time Spent', 'value': '48h', 'icon': 'schedule', 'trend': '+3h'}
                ]
                
                for stat in stats:
                    with ui.card().classes('p-6 flex-1').style(
                        'background: rgba(255, 200, 210, 0.9); backdrop-filter: blur(20px);'
                    ):
                        with ui.row().classes('items-center justify-between mb-4'):
                            ui.label(stat['label']).classes('text-gray-500')
                            ui.icon(stat['icon']).classes('text-pink-600')
                        ui.label(stat['value']).classes('text-3xl font-bold mb-2 text-gray-800')
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('arrow_upward').classes('text-green-500 text-sm')
                            ui.label(stat['trend']).classes('text-green-500 text-sm')

            # Recent activity section
            with ui.card().classes('w-full p-6').style(
                'background: rgba(255, 255 ,255, 0.8); backdrop-filter: blur(20px);'
            ):
                with ui.row().classes('items-center justify-between mb-6'):
                    ui.label('Recent Activity').classes('text-xl font-bold text-gray-800')
                    ui.button('View All', color='pink').props('flat')

                columns = [
                    {'name': 'date', 'label': 'Date', 'field': 'date', 'align': 'left'},
                    {'name': 'activity', 'label': 'Activity', 'field': 'activity', 'align': 'left'},
                    {'name': 'progress', 'label': 'Progress', 'field': 'progress', 'align': 'center'},
                    {'name': 'status', 'label': 'Status', 'field': 'status', 'align': 'center'}
                ]
                data = [
                    {'date': '2024-11-18', 'activity': 'Studied Flashcards', 'progress': '50%', 'status': 'In Progress'},
                    {'date': '2024-11-17', 'activity': 'Completed Dictation', 'progress': '100%', 'status': 'Completed'},
                ]
                ui.table(columns=columns, rows=data)

    
