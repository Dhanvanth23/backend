"""
Translation Module for Budget Tracker
Provides bilingual support for English and Tamil
"""

TRANSLATIONS = {
    'en': {
        # Navigation
        'app_name': 'BudgetTracker',
        'app_tagline': 'Smart Finance Manager',
        'dashboard': 'Dashboard',
        'budget': 'Budget',
        'income': 'Income',
        'expenses': 'Expenses',
        'logout': 'Logout',
        
        # Dashboard
        'your_tracks': 'Your Tracks',
        'financial_overview': 'Financial Overview',
        'current_financial_status': 'Your current financial status',
        'total_available': 'Total Available',
        'budget_income': 'Budget + Income',
        'total_spent': 'Total Spent',
        'this_month': 'This month',
        'remaining': 'Remaining',
        'available_to_spend': 'Available to spend',
        'budget_progress': 'Budget Progress',
        'spent_of': 'spent of',
        'quick_actions': 'Quick Actions',
        'manage_finances': 'Manage your finances',
        'add_expense': 'Add Expense',
        'record_spending': 'Record your spending',
        'add_income': 'Add Income',
        'log_earnings': 'Log your earnings',
        'set_budget': 'Set Budget',
        'plan_spending': 'Plan your spending',
        'transactions': 'Transactions',
        'available_to_spend_text': 'Available to spend',
        
        # Budget Management
        'budget_management': 'Budget Management',
        'set_track_limits': 'Set and track your monthly spending limits',
        'month': 'Month',
        'select_month': 'Select Month',
        'year': 'Year',
        'budget_amount': 'Budget Amount',
        
        # Income Management
        'income_management': 'Income Management',
        'track_manage_income': 'Track and manage your income sources',
        'amount': 'Amount',
        'income_source': 'Income Source',
        'date': 'Date',
        'description_optional': 'Description (Optional)',
        'additional_details': 'Additional details...',
        'income_history': 'Income History',
        
        # Expense Management
        'expense_management': 'Expense Management',
        'track_categorize_spending': 'Track and categorize your spending',
        'category': 'Category',
        'select_category': 'Select Category',
        'description': 'Description',
        'what_spent_on': 'What did you spend on?',
        'expense_history': 'Expense History',
        'all_categories': 'All Categories',
        'clear': 'Clear',
        
        # Categories
        'food': 'Food & Dining',
        'transportation': 'Transportation',
        'shopping': 'Shopping',
        'entertainment': 'Entertainment',
        'utilities': 'Utilities',
        'healthcare': 'Healthcare',
        'education': 'Education',
        'travel': 'Travel',
        'lend': 'Lend',
        'other': 'Other',
        
        # Months
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'april': 'April',
        'may': 'May',
        'june': 'June',
        'july': 'July',
        'august': 'August',
        'september': 'September',
        'october': 'October',
        'november': 'November',
        'december': 'December',
        
        # Actions
        'save': 'Save',
        'cancel': 'Cancel',
        'update': 'Update',
        'delete': 'Delete',
        'edit': 'Edit',
        
        # Modal
        'edit_item': 'Edit Item',
        'edit_expense': 'Edit Expense',
        'edit_income': 'Edit Income',
        
        # Messages
        'no_expense_entries': 'No expense entries',
        'no_income_entries': 'No income entries',
        'no_entries_found': 'No entries found for this month.',
        'loading': 'Loading Budget Tracker...',
        'please_wait': 'Please wait while we verify your session.',
        'success': 'Success',
        'error': 'Error',
        
        # Login/Register
        'login': 'Login',
        'register': 'Register',
        'welcome_back': 'Welcome Back',
        'sign_in_manage': 'Sign in to manage your finances',
        'username': 'Username',
        'enter_username': 'Enter your username',
        'pin': 'PIN',
        'enter_pin': 'Enter your PIN',
        'sign_in': 'Sign In',
        'no_account': "Don't have an account?",
        'create_one': 'Create one',
        'create_account': 'Create Account',
        'start_tracking': 'Start tracking your expenses today',
        'choose_username': 'Choose a username',
        'email_address': 'Email Address',
        'your_email': 'your.email@example.com',
        'create_pin': 'Create a PIN',
        'confirm_pin': 'Confirm PIN',
        'confirm_your_pin': 'Confirm your PIN',
        'already_account': 'Already have an account?',
        'username_hint': 'At least 3 characters, letters, numbers, hyphens and underscores only',
        'email_hint': "We'll send your budget reports to this email",
        'pin_hint': 'At least 4 characters',
        
        # Features
        'track_expenses_feature': 'Track Expenses',
        'monitor_spending': 'Monitor your spending across categories',
        'set_budgets_feature': 'Set Budgets',
        'plan_monthly_limits': 'Plan your monthly spending limits',
        'email_reports_feature': 'Email Reports',
        'get_detailed_reports': 'Get detailed reports via email',
        
        # Navigation Labels
        'overview_stats': 'Overview & Stats',
        'set_your_limits': 'Set Your Limits',
        'track_earnings': 'Track Earnings',
        'track_spending': 'Track Spending',
        'navigation': 'Navigation',

        # Email Reports
        'budget_report_title': 'Budget Report',
        'hello': 'Hello',
        'monthly_financial_summary': "here's your monthly financial summary",
        'reports_scheduled_for': 'Your reports are scheduled for day',
        'of_each_month': 'of each month',
        'allocated_budget': 'Allocated Budget',
        'additional_income': 'Additional Income',
        'category_breakdown': 'Category Breakdown',
        'count': 'Count',
        'total_amount': 'Total Amount',
        'top_income_sources': 'Top Income Sources',
        'source': 'Source',
        'top_expenses': 'Top Expenses',
        'generated_on': 'This report was generated on',
        'change_schedule': 'Change your report schedule',
        'manage_finances_wisely': 'Manage your finances wisely',
        'complete_transaction_history': 'Complete Transaction History',
        'here_are_all_transactions': 'here are all your transactions',
        'all_expenses': 'All expenses',
        'type': 'Type',
        'category_source': 'Category/Source',

        # View Toggles
        'monthly_view': 'Monthly View',
        'lifetime_view': 'Lifetime View',
        
        # Email Report Buttons
        'send_monthly_report': 'Send Monthly Report',
        'send_transaction_history': 'Send Transaction History',
        'language': 'Language',
        'email_reports': 'Email Reports',
        
        # Progress Section
        'budget_progress_title': 'Budget Progress',
    },

    'ta': {
        # Navigation
        'app_name': 'பண மேலாளர்',
        'app_tagline': 'சிறந்த நிதி மேலாளர்',
        'dashboard': 'முகப்பு',
        'budget': 'பட்ஜெட்',
        'income': 'வருமானம்',
        'expenses': 'செலவுகள்',
        'logout': 'வெளியேறு',
        
        # Dashboard
        'your_tracks': 'உங்கள் பட்ஜெட்',
        'financial_overview': 'நிதி கண்ணோட்டம்',
        'current_financial_status': 'உங்கள் தற்போதைய நிதி நிலை',
        'total_available': 'மொத்த கிடைக்கும் தொகை',
        'budget_income': 'பட்ஜெட் + வருமானம்',
        'total_spent': 'மொத்த செலவு',
        'this_month': 'இந்த மாதம்',
        'remaining': 'மீதமுள்ளது',
        'available_to_spend': 'செலவழிக்க கிடைக்கும்',
        'budget_progress': 'பட்ஜெட் முன்னேற்றம்',
        'spent_of': 'செலவு',
        'quick_actions': 'விரைவு செயல்கள்',
        'manage_finances': 'உங்கள் நிதியை நிர்வகிக்கவும்',
        'add_expense': 'செலவு சேர்க்க',
        'record_spending': 'உங்கள் செலவை பதிவு செய்யவும்',
        'add_income': 'வருமானம் சேர்க்க',
        'log_earnings': 'உங்கள் வருவாயை பதிவு செய்யவும்',
        'set_budget': 'பட்ஜெட் அமை',
        'plan_spending': 'உங்கள் செலவை திட்டமிடுங்கள்',
        'transactions': 'பரிவர்த்தனைகள்',
        'available_to_spend_text': 'செலவழிக்க கிடைக்கும்',
        
        # Budget Management
        'budget_management': 'பட்ஜெட் மேலாண்மை',
        'set_track_limits': 'உங்கள் மாதாந்திர செலவு வரம்புகளை அமைத்து கண்காணிக்கவும்',
        'month': 'மாதம்',
        'select_month': 'மாதத்தை தேர்ந்தெடுக்கவும்',
        'year': 'ஆண்டு',
        'budget_amount': 'பட்ஜெட் தொகை',
        
        # Income Management
        'income_management': 'வருமான மேலாண்மை',
        'track_manage_income': 'உங்கள் வருமான ஆதாரங்களை கண்காணித்து நிர்வகிக்கவும்',
        'amount': 'தொகை',
        'income_source': 'வருமான ஆதாரம்',
        'date': 'தேதி',
        'description_optional': 'விவரம் (விருப்பம்)',
        'additional_details': 'கூடுதல் விவரங்கள்...',
        'income_history': 'வருமான வரலாறு',
        
        # Expense Management
        'expense_management': 'செலவு மேலாண்மை',
        'track_categorize_spending': 'உங்கள் செலவை கண்காணித்து வகைப்படுத்துங்கள்',
        'category': 'வகை',
        'select_category': 'வகையை தேர்ந்தெடுக்கவும்',
        'description': 'விவரம்',
        'what_spent_on': 'நீங்கள் எதற்கு செலவு செய்தீர்கள்?',
        'expense_history': 'செலவு வரலாறு',
        'all_categories': 'அனைத்து வகைகள்',
        'clear': 'அழி',
        
        # Categories
        'food': 'உணவு மற்றும் உணவகம்',
        'transportation': 'போக்குவரத்து',
        'shopping': 'கொள்முதல்',
        'entertainment': 'பொழுதுபோக்கு',
        'utilities': 'பயன்பாடுகள்',
        'healthcare': 'சுகாதாரம்',
        'education': 'கல்வி',
        'travel': 'பயணம்',
        'lend': 'கடன் கொடுத்தல்',
        'other': 'மற்றவை',
        
        # Months
        'january': 'ஜனவரி',
        'february': 'பிப்ரவரி',
        'march': 'மார்ச்',
        'april': 'ஏப்ரல்',
        'may': 'மே',
        'june': 'ஜூன்',
        'july': 'ஜூலை',
        'august': 'ஆகஸ்ட்',
        'september': 'செப்டம்பர்',
        'october': 'அக்டோபர்',
        'november': 'நவம்பர்',
        'december': 'டிசம்பர்',
        
        # Actions
        'save': 'சேமி',
        'cancel': 'ரத்து',
        'update': 'புதுப்பி',
        'delete': 'நீக்கு',
        'edit': 'திருத்து',
        
        # Modal
        'edit_item': 'உருப்படியை திருத்து',
        'edit_expense': 'செலவை திருத்து',
        'edit_income': 'வருமானத்தை திருத்து',
        
        # Messages
        'no_expense_entries': 'செலவு பதிவுகள் இல்லை',
        'no_income_entries': 'வருமான பதிவுகள் இல்லை',
        'no_entries_found': 'இந்த மாதத்திற்கான பதிவுகள் இல்லை.',
        'loading': 'பட்ஜெட் ட்ராக்கரை ஏற்றுகிறது...',
        'please_wait': 'உங்கள் அமர்வை சரிபார்க்கும் வரை காத்திருக்கவும்.',
        'success': 'வெற்றி',
        'error': 'பிழை',
        
        # Login/Register
        'login': 'உள்நுழை',
        'register': 'பதிவு செய்',
        'welcome_back': 'மீண்டும் வருக',
        'sign_in_manage': 'உங்கள் நிதியை நிர்வகிக்க உள்நுழையவும்',
        'username': 'பயனர் பெயர்',
        'enter_username': 'உங்கள் பயனர் பெயரை உள்ளிடவும்',
        'pin': 'பின்',
        'enter_pin': 'உங்கள் பின்னை உள்ளிடவும்',
        'sign_in': 'உள்நுழை',
        'no_account': 'கணக்கு இல்லையா?',
        'create_one': 'ஒன்றை உருவாக்கு',
        'create_account': 'கணக்கை உருவாக்கு',
        'start_tracking': 'இன்று உங்கள் செலவுகளை கண்காணிக்க தொடங்குங்கள்',
        'choose_username': 'பயனர் பெயரை தேர்வு செய்யவும்',
        'email_address': 'மின்னஞ்சல் முகவரி',
        'your_email': 'your.email@example.com',
        'create_pin': 'பின் உருவாக்கு',
        'confirm_pin': 'பின்னை உறுதிப்படுத்து',
        'confirm_your_pin': 'உங்கள் பின்னை உறுதிப்படுத்தவும்',
        'already_account': 'ஏற்கனவே கணக்கு உள்ளதா?',
        'username_hint': 'குறைந்தது 3 எழுத்துக்கள், எழுத்துக்கள், எண்கள், கோடுகள் மற்றும் அடிக்கோடுகள் மட்டும்',
        'email_hint': 'உங்கள் பட்ஜெட் அறிக்கைகளை இந்த மின்னஞ்சலுக்கு அனுப்புவோம்',
        'pin_hint': 'குறைந்தது 4 எழுத்துக்கள்',
        
        # Features
        'track_expenses_feature': 'செலவுகளை கண்காணிக்கவும்',
        'monitor_spending': 'வகைகள் முழுவதும் உங்கள் செலவை கண்காணிக்கவும்',
        'set_budgets_feature': 'பட்ஜெட்டுகளை அமைக்கவும்',
        'plan_monthly_limits': 'உங்கள் மாதாந்திர செலவு வரம்புகளை திட்டமிடுங்கள்',
        'email_reports_feature': 'மின்னஞ்சல் அறிக்கைகள்',
        'get_detailed_reports': 'மின்னஞ்சல் வழியாக விரிவான அறிக்கைகளைப் பெறுங்கள்',
        
        # Navigation Labels
        'overview_stats': 'கண்ணோட்டம் மற்றும் புள்ளிவிவரங்கள்',
        'set_your_limits': 'உங்கள் வரம்புகளை அமைக்கவும்',
        'track_earnings': 'வருவாயை கண்காணிக்கவும்',
        'track_spending': 'செலவை கண்காணிக்கவும்',
        'navigation': 'வழிசெலுத்தல்',

        # Email Reports
        'budget_report_title': 'பட்ஜெட் அறிக்கை',
        'hello': 'வணக்கம்',
        'monthly_financial_summary': 'உங்கள் மாதாந்திர நிதி சுருக்கம் இதோ',
        'reports_scheduled_for': 'உங்கள் அறிக்கைகள் திட்டமிடப்பட்டுள்ளன',
        'of_each_month': 'ஒவ்வொரு மாதமும்',
        'allocated_budget': 'ஒதுக்கப்பட்ட பட்ஜெட்',
        'additional_income': 'கூடுதல் வருமானம்',
        'category_breakdown': 'வகை பிரிவு',
        'count': 'எண்ணிக்கை',
        'total_amount': 'மொத்த தொகை',
        'top_income_sources': 'முதல் வருமான ஆதாரங்கள்',
        'source': 'ஆதாரம்',
        'top_expenses': 'முதல் செலவுகள்',
        'generated_on': 'இந்த அறிக்கை உருவாக்கப்பட்டது',
        'change_schedule': 'உங்கள் அறிக்கை அட்டவணையை மாற்றவும்',
        'manage_finances_wisely': 'உங்கள் நிதியை புத்திசாலித்தனமாக நிர்வகிக்கவும்',
        'complete_transaction_history': 'முழுமையான பரிவர்த்தனை வரலாறு',
        'here_are_all_transactions': 'உங்கள் அனைத்து பரிவர்த்தனைகளும் இதோ',
        'all_expenses': 'அனைத்து செலவுகளும்',
        'type': 'வகை',
        'category_source': 'வகை/ஆதாரம்',

        # View Toggles
        'monthly_view': 'மாதாந்திர காட்சி',
        'lifetime_view': 'வாழ்நாள் காட்சி',
        
        # Email Report Buttons
        'send_monthly_report': 'மாதாந்திர அறிக்கை அனுப்பு',
        'send_transaction_history': 'பரிவர்த்தனை வரலாறு அனுப்பு',
        'language': 'மொழி',
        'email_reports': 'மின்னஞ்சல் அறிக்கைகள்',
        
        # Progress Section
        'budget_progress_title': 'பட்ஜெட் முன்னேற்றம்',
    }
}


def get_translations(key, lang='en'):
    """Get translation for a given key and language"""
    return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['en'].get(key, key))

def get_all_translations(lang='en'):
    """Get all translations for a given language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['en'])