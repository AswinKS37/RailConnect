"""
routes.py

Registers the Flask routes for the Railway Booking System.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from graph import network, get_stations, find_routes
from booking import validate_seats, book_route
from train_api import get_train_status
import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    stations = get_stations()
    return render_template('index.html', stations=stations)

@bp.route('/status_check', methods=['GET', 'POST'])
def status_check():
    """Renders the status check form and processes it."""
    if request.method == 'POST':
        train_number = request.form.get('train_number')
        # Form date represents 'YYYY-MM-DD'. Our API needs 'YYYYMMDD'
        form_date = request.form.get('date')
        
        if not train_number or not form_date:
            flash("Please provide Train Number and Date.")
            return redirect(url_for('main.status_check'))
            
        try:
             # Parse 'YYYY-MM-DD' and reformat to 'YYYYMMDD'
             parsed_date = datetime.datetime.strptime(form_date, '%Y-%m-%d')
             formatted_date = parsed_date.strftime('%Y%m%d')
        except ValueError:
             flash("Invalid Date format.")
             return redirect(url_for('main.status_check'))
             
        # Call the API wrapper
        api_response = get_train_status(train_number, formatted_date)
        
        return render_template('status_result.html', response=api_response, train_num=train_number, date=form_date)

    return render_template('status.html')

@bp.route('/search', methods=['POST'])
def search():
    source = request.form.get('source')
    destination = request.form.get('destination')
    date = request.form.get('date') # simple UI element, not used in BFS directly as graph is simplified
    
    if source == destination:
        flash('Source and Destination cannot be the same.')
        return redirect(url_for('main.home'))
        
    # Get all possible paths
    all_paths = find_routes(source, destination)
    
    # Filter valid seated paths
    valid_paths = [path for path in all_paths if validate_seats(path)]
    
    # Sort paths by length (number of segments) so direct routes (length 1) appear first
    valid_paths.sort(key=len)
    
    return render_template('results.html', paths=valid_paths, source=source, dest=destination, date=date)

@bp.route('/book', methods=['POST'])
def book():
    import json
    # path is passed as a JSON string from the button value
    path_json = request.form.get('path')
    if not path_json:
        flash("Invalid booking request.")
        return redirect(url_for('main.home'))
        
    try:
        path = json.loads(path_json)
    except json.JSONDecodeError:
        flash("Malformed booking data.")
        return redirect(url_for('main.home'))

    success, updated_path = book_route(path)
    
    if success:
        return render_template('confirmation.html', updated_path=updated_path)
    else:
        # One or more segments didn't have seats available
        flash("Booking failed. One or more connections do not have available seats.")
        return redirect(url_for('main.home'))
