import csv
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Define the CSV file path
CSV_FILE = 'survey_responses.csv'

# Define the header titles for the CSV
HEADER = [
    'Education', 'Department', 'Seniority', 'AI Experience', 'Business Domain', 'Location', 
    'Is Startup', 'Company Stage', 'Funding Stage', 'AI Experience Level', 'Team Size', 
    'AI Tools', 'AI Usage', 'AI Benefits', 'Success Metrics', 'Improvement Areas', 
    'AI Challenges', 'AI Desired Features', 'AI Replacement', 'Email'
]

# Check if the CSV file exists and if not, create it with headers
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header row with all titles (questions)
            writer.writerow(HEADER)

# Initialize the CSV file with headers when the app starts
init_csv()

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        # Collect form data
        education = request.form.get('education')
        department = request.form.get('department')
        seniority = request.form.get('seniority')
        ai_experience = request.form.get('ai_experience')
        
        business_domain = request.form.get('business_domain')
        location = request.form.get('location')
        is_startup = request.form.get('is_startup')
        company_stage = request.form.get('company_stage') if is_startup == 'Yes' else None
        funding_stage = request.form.get('funding_stage') if is_startup == 'Yes' else None
        ai_experience_level = request.form.get('ai_experience_level')
        team_size = request.form.get('team_size')
        
        # Collect AI Tools (multiple tools allowed)
        ai_tools = request.form.getlist('ai_tools')  # Get list of AI tools selected
        ai_tools_str = ", ".join(ai_tools)  # Convert list to comma-separated string
        
        # Collect AI Tool usage responses (list of tools for each activity)
        ai_usage = {}
        for activity in ['Ideation and brainstorming', 'Roadmap planning and validation', 
                         'Customer feedback analysis and insights', 'Automating repetitive tasks', 
                         'Prioritizing features or roadmapping']:
            ai_usage[activity] = request.form.getlist(f'activity_{activity}')
        
        # Prepare the AI Usage data to be stored in a readable format (semicolon-separated)
        ai_usage_str = "; ".join([f"{activity}: {', '.join(items)}" for activity, items in ai_usage.items() if items])

        # Collect additional form data
        ai_benefits = request.form.get('ai_benefits', '')
        success_metrics = request.form.get('success_metrics', '')
        improvement_areas = request.form.get('improvement_areas', '')
        ai_challenges = request.form.get('ai_challenges', '')
        ai_desired_features = request.form.get('ai_desired_features', '')
        ai_replacement = request.form.get('ai_replacement', '')
        email = request.form.get('email')

        # Prepare data for CSV
        row = [
            education, department, seniority, ai_experience, business_domain, location, 
            is_startup, company_stage, funding_stage, ai_experience_level, team_size, 
            ai_tools_str, ai_usage_str, ai_benefits, success_metrics, 
            improvement_areas, ai_challenges, ai_desired_features, ai_replacement, email
        ]
        
        # Save data to CSV
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(row)
        
        # Redirect to a thank you page
        return redirect(url_for('thank_you'))

    return render_template('survey.html')

@app.route('/thank-you')
def thank_you():
    return "Thank you for completing the survey!"

if __name__ == '__main__':
    app.run(debug=True)
