import serial
import re
import xmlrpc.client


url = 'localhost'
db = 'database'
uid = 2
password = 'password'
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

ser = serial.Serial('COM6', 9600, timeout=None)

def read_from_arduino():
    tag_id_from_arduino = ser.readline()
    return tag_id_from_arduino

def create_worker_entry(tag):
    uid_by_tag = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['tag_id', '=', tag]]], {'limit': 1})
    # get last entry in odoo system of current tag
    last_worker_entry = models.execute_kw(db, uid, password, 'workers.attendance', 'search', [[]] ,{'limit': 1, 'order': 'create_date desc'})
    has_entered = False
    if last_worker_entry:
        # get last entries field "rfid_status" value
        last_worker_entry_status = models.execute_kw(db, uid, password, 'workers.attendance', 'read', [last_worker_entry], {'fields': ['rfid_status']})
        if last_worker_entry_status[0]['rfid_status'] == False:
            has_entered = True
    models.execute_kw(db, uid, password, 'workers.attendance', 'create',
        [
            {
                'tag_id': tag,
                'name': uid_by_tag[0],
                'rfid_status': has_entered
            }
        ]
    )
    print('Worker Entry Created')
    
while True:
    tag_id = read_from_arduino().decode().rstrip()
    create_worker_entry(tag_id)
