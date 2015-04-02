from SteamScout.models import Preferences, User
from SteamScout.helpers import get_price_info, send_mail
from SteamScout import app
from flask import render_template
from celery import Celery

celery = Celery("tasks", broker='redis://localhost')

@celery.task
def send_game_alerts():
    user_preferences = Preferences.query.all()
    user_email = User.query.filter
    
    for user in User.query.all():
        user_id = user.id
        user_email = user.email
        user_preferences = Preferences.query.filter_by(user_id=user_id)

        if user_preferences.first():
            game_alerts = []
            for preference in user_preferences:
                current_game_info = get_price_info(preference.game_id)
                if preference.threshold_amount >= current_game_info["current_price"]/100.0:
                    game_alerts.append([preference.game_name, "${:.2f}".format(preference.threshold_amount)])
            if game_alerts:
                with app.app_context():
                # find_template = Environment(loader=PackageLoader("SteamScout", "templates/email"))
                # template = find_template.get_template("scout_alert.html")
                # preferences_url = url_for('settings', _external=True)
                # html = template.render(game_alerts=game_alerts)
                    html = render_template("email/scout_alert.html", game_alerts=game_alerts)
                    subject = "Scout Report"
                    send_mail(user_email, subject, html)
