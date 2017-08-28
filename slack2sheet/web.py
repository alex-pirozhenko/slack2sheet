import json
import gspread
from flask import Flask, request, jsonify
from oauth2client.service_account import ServiceAccountCredentials


scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]


def get_row_count(worksheet):
    col_values = worksheet.col_values(1)
    return len(list(filter(None, col_values)))


def refresh_worksheet(credentials, sheet_url):
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(sheet_url)
    return sheet.sheet1

active_fields = ['message_ts', 'channel', 'user', 'action_id', 'action_name', 'action_value']


def create_app(cred_path, sheet_url):
    app = Flask("slack2sheet")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
    worksheet = refresh_worksheet(credentials, sheet_url)
    if get_row_count(worksheet) == 0:
        print('Resizing the empty worksheet to 1x{} and inserting the header'.format(len(active_fields)))
        worksheet.resize(rows=1, cols=len(active_fields))
        worksheet.append_row(active_fields)
        worksheet.delete_row(1)

    @app.route("/slack/annotate", methods=['POST'])
    def log():
        payload = json.loads(request.form['payload'])
        original_message = payload['original_message']
        del payload['original_message']
        print(payload)
        data = {
            'message_ts': payload['message_ts'],
            'channel': payload['channel']['name'],
            'channel_id': payload['channel']['id'],
            'user': payload['user']['name'],
            'user_id': payload['user']['id'],
            'action_id': payload['callback_id'],
            'action_name': payload['actions'][0]['name'],
            'action_value': payload['actions'][0]['value'],
        }
        refresh_worksheet(credentials, sheet_url).append_row([data.get(_) for _ in active_fields])

        original_message['attachments'].append({
            'text': "{} answered '{}'".format(data['user'], data['action_value']),
            'attachment_type': 'default'
        })
        return jsonify(original_message)

    return app
