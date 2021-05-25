# -*- coding: utf-8 -*-
#

"""
Created on Sat Sep  8 21:52:07 2018

@author: arjun
"""

import datetime
import json
import mongoengine
import xetrapal
import pandas
from . import documents, utils
from copy import deepcopy
import requests

from xetrapal import gdastras
from xetrapal import smsastras
a = xetrapal.karma.load_xpal_smriti(
    "/opt/saibot-appdata/saibotxpal.json")
a.save()
a.reload()
saibotxpal = xetrapal.Xetrapal(a)
saibotxpal.dhaarana(gdastras)
saibotxpal.dhaarana(smsastras)
#saibotgd = saibotxpal.gd_get_googledriver()
#sms = saibotxpal.get_sms_astra()
#sconfig = xetrapal.karma.load_config(a.configfile)
#mmiurl = sconfig.get("MapMyIndia", "apiurl")
#mmikey = sconfig.get("MapMyIndia", "apikey")
#mmiurl = mmiurl + mmikey + "/"

# Setting up mongoengine connections
saibotxpal.logger.info("Setting up MongoEngine")
mongoengine.disconnect()
mongoengine.connect('saibot', alias='default')

'''
def validate_vehicle_dict(vehicledict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid vehicle"
    required_keys = []
    if new is True:
        required_keys = ["vehicle_id"]
    string_keys = ["vehicle_id"]
    validation = utils.validate_dict(
        vehicledict, required_keys=required_keys, string_keys=string_keys)
    if validation['status'] is True:
        saibotxpal.logger.info("vehicledict: " + validation['message'])
    else:
        saibotxpal.logger.error("vehicledict: " + validation['message'])
    return validation


def sss(invoicedict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid vehicle"
    required_keys = []
    if new is True:
        required_keys = ["invoicelines", "cust_id", "invoice_date"]
    validation = utils.validate_dict(invoicedict, required_keys=required_keys)
    if validation['status'] is True:
        saibotxpal.logger.info("invoicedict: " + validation['message'])
    else:
        saibotxpal.logger.error("invoicedict: " + validation['message'])
    return validation


def validate_locupdate_dict(locupdatedict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid location update"
    required_keys = []
    if new is True:
        required_keys = ["username", "timestamp"]
    string_keys = ["username"]
    validation = utils.validate_dict(
        locupdatedict, required_keys=required_keys, string_keys=string_keys)
    if validation['status'] is True:
        saibotxpal.logger.info("locupdatedict: " + validation['message'])
    else:
        saibotxpal.logger.error("locupdatedict: " + validation['message'])
    return validation
'''

def validate_customer_dict(customerdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid customer"
    required_keys = []
    if new is True:
        required_keys = ["cust_id", "mobile_num"]
    string_keys = ["cust_id"]
    mobile_nums = ["mobile_num"]
    validation = utils.validate_dict(
        customerdict, required_keys=required_keys, string_keys=string_keys, mobile_nums=mobile_nums)
    if validation['status'] is True:
        saibotxpal.logger.info("customerdict: " + validation['message'])
    else:
        saibotxpal.logger.error("customerdict: " + validation['message'])
    return validation

'''
def validate_product_dict(productdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid product"
    required_keys = []
    if new is True:
        required_keys = ["product_id"]
    string_keys = ["product_id"]
    numbers = ["included_hrs", "included_kms", "extra_hrs_rate",
               "extra_kms_rate"]  # CHANGELOG #11 - AV - For #261
    validation = utils.validate_dict(
        productdict, required_keys=required_keys, string_keys=string_keys, numbers=numbers)
    if validation['status'] is True:
        saibotxpal.logger.info("productdict: " + validation['message'])
    else:
        saibotxpal.logger.error("productdict: " + validation['message'])
    return validation
'''

def validate_member_dict(memberdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid member"
    required_keys = []
    if new is True:
        required_keys = ["username", "mobile_num"]
    string_keys = ["first_name", "last_name",
                   "mobile_num", "name", "username"]
    mobile_nums = ["mobile_num"]
    validation = utils.validate_dict(
        memberdict, required_keys=required_keys, string_keys=string_keys, mobile_nums=mobile_nums)
    if validation['status'] is True:
        saibotxpal.logger.info("memberdict: " + validation['message'])
    else:
        saibotxpal.logger.error("memberdict: " + validation['message'])
    return validation

'''
def validate_dutyslip_dict(dutyslipdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid dutyslip"
    required_keys = []
    if new is True:
        required_keys = ["member", "assignment"]
    string_keys = ["member", "vehicle", "remarks"]
    dates = ['open_time', 'close_time']
    numbers = ['open_kms', 'close_kms',
               'parking_charges', 'toll_charges', 'amount']
    validation = utils.validate_dict(
        dutyslipdict, required_keys=required_keys, string_keys=string_keys, dates=dates, numbers=numbers)

    try:
        if datetime.datetime.strptime(dutyslipdict['open_time'], "%Y-%m-%d %H:%M:%S") > datetime.datetime.strptime(dutyslipdict['close_time'], "%Y-%m-%d %H:%M:%S"):
            validation['status'] = False
            validation['message'] = "Open time cant be after close time"
    except Exception as e:
        validation['status'] = False
        validation['message'] = "ERROR IN TIME VALusernameATION " + str(e)

    try:
        if float(dutyslipdict['open_kms']) > float(dutyslipdict['close_kms']):
            validation['status'] = False
            validation['message'] = "Open kms cant be more than close kms"
    except Exception as e:
        validation['status'] = False
        validation['message'] = "ERROR IN DIST VALusernameATION " + str(e)
    try:
        if "vehicle" in dutyslipdict.keys() and dutyslipdict['vehicle'] != "":
            if len(documents.Vehicle.objects(vehicle_id=dutyslipdict['vehicle'])) == 0:
                validation['status'] = False
                validation['message'] = "Unknown vehicle id"
    except Exception as e:
        validation['status'] = False
        validation['message'] = "ERROR IN VEHICLE VALusernameATION " + str(e)
    if validation['status'] is True:
        saibotxpal.logger.info("dutyslipdict: " + validation['message'])
    else:
        saibotxpal.logger.error("dutyslipdict: " + validation['message'])
    return validation


def validate_assignment_dict(assignmentdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid assignment"

    if assignmentdict['dutyslips'] == []:
        validation['status'] = False
        validation['message'] = "At least one member must be assigned to create an assignment."
    if assignmentdict['assignment']['bookings'] == []:
        validation['status'] = False
        validation['message'] = "At least one booking must be assigned to create an assignment."
    bookings = [documents.Booking.objects.with_id(
        x['_id']['$oid']) for x in assignmentdict['assignment']['bookings']]
    for booking in bookings:
        if booking.assignment is not None:
            validation['status'] = False
            validation['message'] = "Booking is already assigned {}! Please delete the old assignment before creating a new one.".format(
                booking.assignment)
        if booking.cust_id != assignmentdict['assignment']['cust_id']:
            validation['status'] = False
            validation['message'] = "Bookings from different customers cannot be assigned together."
    seenvehicles = []
    for dutyslip in assignmentdict['dutyslips']:
        if "vehicle" in dutyslip.keys():
            if dutyslip['vehicle'] in seenvehicles:
                validation['status'] = False
                validation['message'] = "Can't assign the same vehicle to more than one member in the same assignment."
            seenvehicles.append(dutyslip['vehicle'])
    if validation['status'] is True:
        saibotxpal.logger.info("assignmentdict: " + validation['message'])
    else:
        saibotxpal.logger.error("assignmentdict: " + validation['message'])
    return validation


def new_locationupdate(member, timestamp, checkin=True, location=None, vehicle=None, handoff=None, logger=xetrapal.astra.baselogger, **kwargs):
    """
    Creates a new location update, location updates once created are not deleted as they are equivalent to log entries.
    Returns a LocationUpdate object
    """
    vehicle_id = None
    if checkin is True:
        member.checkedin = True
    if vehicle is not None:
        vehicle.username = member.username
        vehicle.save()
        vehicle_id = vehicle.vehicle_id
    if checkin is False:
        member.checkedin = False
        if len(documents.Vehicle.objects(username=member.username)) > 0:
            v = documents.Vehicle.objects(username=member.username)
            for vh in v:
                del vh.username
                vh.save()
                vehicle_id = vh.vehicle_id
    member.save()
    adjtimestamp = utils.get_utc_ts(timestamp)
    locationupdate = documents.LocationUpdate(
        username=member.username, timestamp=adjtimestamp, location=location, checkin=checkin, handoff=handoff, vehicle_id=vehicle_id)
    if checkin is True:
        logger.info(u"New checkin from member with id {} at {} from {}".format(
            locationupdate.username, locationupdate.timestamp, locationupdate.location))
    else:
        logger.info(u"Checkout from member with id {} at {} from {}".format(
            locationupdate.username, locationupdate.timestamp, locationupdate.location))
    locationupdate.save()
    return locationupdate



Bookings CRUD



def validate_booking_dict(bookingdict, new=True):
    validation = {}
    validation['status'] = True
    validation['message'] = "Valid booking"
    required_keys = []
    if new is True:
        required_keys = ["cust_id", "product_id", "passenger_detail",
                         "pickup_timestamp", "pickup_location", "booking_channel"]
    string_keys = ["cust_id", "product_id",
                   "passenger_detail", "passenger_mobile", "remarks"]
    mobile_nums = ["passenger_mobile"]
    validation = utils.validate_dict(
        bookingdict, required_keys=required_keys, string_keys=string_keys, mobile_nums=mobile_nums)
    if "cust_id" in bookingdict.keys():
        if bookingdict['cust_id'] == "retail":
            if not bookingdict['passenger_mobile'] or bookingdict['passenger_mobile'] is None:
                validation['message'] = "Passenger Mobile Must be provided for retail bookings"
                validation['status'] = False
    if validation['status'] is True:
        saibotxpal.logger.info("bookingdict: " + validation['message'])
    else:
        saibotxpal.logger.error("bookingdict: " + validation['message'])
    return validation


def new_booking(respdict):
    respdict2 = deepcopy(respdict)
    bookingdict = {}
    saibotxpal.logger.info(
        "Creating new booking from dictionary\n{}".format(respdict))
    for key in respdict2.keys():
        if key in ["cust_id", "product_id", "passenger_detail", "passenger_mobile", "pickup_timestamp", "pickup_location", "drop_location", "booking_channel", "num_passengers", "notification_prefs", "remarks", "flight_detail", "payment_mode"]:  # Adding fields for #399
            bookingdict[key] = respdict[key]
            respdict.pop(key)
    if "_id" in respdict2.keys():
        respdict.pop("_id")
    if "created_timestamp" in respdict2.keys():
        respdict.pop("created_timestamp")
    if "passenger_mobile" not in bookingdict.keys() or bookingdict['passenger_mobile'] is None:
        mobile_num = documents.Customer.objects(
            cust_id=bookingdict['cust_id'])[0].mobile_num
        bookingdict['passenger_mobile'] = mobile_num
    try:
        b = documents.Booking(booking_id=utils.new_booking_id(), **bookingdict)
        for key in respdict2.keys():
            key2 = key.replace(".", "").replace("$", "")
            if key2 != key:
                respdict[key2] = respdict[key]
                respdict.pop(key)
        saibotxpal.logger.info("Saving cust-meta as: {}".format(respdict))
        b.cust_meta = respdict
        b.save()
        b.reload()
        notification = "Sakha Cabs Booking {} created \n {}".format(
            b.booking_id, repr(b))

        if b.notification_prefs["new"] != []:
            recipients = []
            for num in b.notification_prefs["new"]:
                recipients.append({"type": "mobile", "value": num})
            sms.send_sms({"message": notification, "recipients": recipients})
        saibotxpal.logger.info("{}".format(notification))
        respdict['booking_id'] = b.booking_id
        return [b]
    except Exception as e:
        respdict['booking_id'] = None
        return "error: {} {}".format(type(e), str(e))


def update_booking_status(booking_id, status):
    if status not in utils.validstatuses:
        saibotxpal.logger.error("Invalid status")
        return False
    booking = documents.Booking.objects(booking_id=booking_id)
    if len(booking) == 0:
        return "No booking by that id"
    else:
        booking = booking[0]
    try:
        if status in ['cancelled', 'new']:
            if booking.assignment is not None:
                saibotxpal.logger.info(
                    "Booking is assigned, checking assignment status")
                assignment = documents.Assignment.objects.with_id(
                    booking.assignment)
                saibotxpal.logger.info("Removing booking {} from assignment {}".format(
                    booking.booking_id, booking.assignment))
                assignment.bookings.remove(booking)
                assignment.save()
                assignment.reload()
                if assignment.bookings == []:
                    update_assignment_status(assignment.id, "cancelled")
                else:
                    saibotxpal.logger.info(
                        "Updating assignment reporting time to first booking!")
                    assignment.reporting_location = assignment.bookings[0].pickup_location
                    assignment.reporting_timestamp = assignment.bookings[0].pickup_timestamp
                    assignment.save()
                booking.assignment = None
        booking.status = status
        booking.save()
        if booking.notification_prefs[status] != []:
            recipients = []
            notification = "Sakha Cabs Booking {} status change to {}".format(
                booking.booking_id, booking.status)
            for num in booking.notification_prefs[status]:
                recipients.append({"type": "mobile", "value": num})
            if status == "assigned":
                assignment = documents.Assignment.objects.with_id(
                    booking.assignment)
                notification = notification + "\n Pickup Time: " + assignment.reporting_timestamp.strftime(
                    "%Y-%m-%d %H:%M") + "\n Pickup Location: " + assignment.reporting_location + "\n Drivers Assigned \n"
                dutyslips = documents.DutySlip.objects(assignment=assignment)
                for dutyslip in dutyslips:
                    member = documents.Member.objects(
                        username=dutyslip.member)[0]
                    notification = notification + \
                        "\n {} {} {}".format(
                            member.username, member.mobile_num, dutyslip.vehicle)
            sms.send_sms({"message": notification, "recipients": recipients})
        return True
    except Exception as e:
        saibotxpal.logger.error(
            "Error occurred updating booking status {}".format(str(e)))
        return False


def update_booking(booking_id, respdict):
    respdict2 = deepcopy(respdict)
    booking = documents.Booking.objects(booking_id=booking_id)
    if len(booking) == 0:
        return "No booking by that id"
    else:
        booking = booking[0]
        saibotxpal.logger.info(
            "Trying to update booking with id {}".format(booking.booking_id))
        if "_id" in respdict2.keys():
            respdict.pop("_id")
        if "created_timestamp" in respdict2.keys():
            respdict.pop("created_timestamp")
        if "status" in respdict2.keys():
            saibotxpal.logger.info(
                "Updated status should be {}".format(respdict['status']))
            if respdict2['status'] != booking.status:
                saibotxpal.logger.info(
                    "original status is {}".format(booking.status))
                if not update_booking_status(booking.booking_id, respdict2['status']):
                    saibotxpal.loggger.error(
                        "Updating booking status failed")
                    return "Updating booking status failed"
        try:
            booking.update(**respdict)
            booking.save()
            booking.reload()
            if booking.assignment is not None:
                assignment = documents.Assignment.objects.with_id(
                    booking.assignment)
                if "pickup_timestamp" in respdict2.keys():
                    assignment.reporting_timestamp = booking.pickup_timestamp
                if "pickup_location" in respdict2.keys():
                    assignment.reporting_location = booking.pickup_location
                assignment.save()

            return [booking]
        except Exception as e:
            return "{} {}".format(type(e), str(e))


def delete_booking(booking_id):
    if len(documents.Booking.objects(booking_id=booking_id)) > 0:
        try:
            update_booking_status(booking_id, "cancelled")
            booking = documents.Booking.objects(booking_id=booking_id)[0]
            booking.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    else:
        return "No booking by that id"
'''

'''
Assignment CRUD



def save_assignment(assignmentdict, assignment_id=None):
    reates a new assignment/Updates an existing assignment with the provided bookings and duty slips
    Input: A dictionary of the format {"assignment": Assignment object,dutyslips: List of member/vehicle pairs}
    Returns: An assignment object

    bookings = [documents.Booking.objects.with_id(
        x['_id']['$oid']) for x in assignmentdict['assignment']['bookings']]
    if assignment_id is None:
        assignment = documents.Assignment(bookings=bookings)
        assignment.status = "new"
        saibotxpal.logger.info("Created new assignment at {}".format(
            assignment.created_timestamp.strftime("%Y-%m-%d %H:%M:%S")))
    else:
        saibotxpal.logger.info(
            "Saving existing assignment {}".format(assignment_id))
        assignment = documents.Assignment.objects.with_id(assignment_id)
        assignment.bookings = bookings
    assignment.bookings = sorted(
        assignment.bookings, key=lambda k: k.pickup_timestamp)
    assignment.reporting_timestamp = assignment.bookings[0].pickup_timestamp
    assignment.reporting_location = assignment.bookings[0].pickup_location
    if assignment.bookings[0].drop_location:
        assignment.drop_location = assignment.bookings[0].drop_location
    assignment.cust_id = assignment.bookings[0].cust_id
    assignment.save()
    existingdutyslips = documents.DutySlip.objects(assignment=assignment)
    saibotxpal.logger.info(
        "Existing duty slips {}".format(existingdutyslips.to_json()))
    existingdutyslips = list(existingdutyslips)
    saibotxpal.logger.info(
        "Submitted duty slips {}".format(assignmentdict['dutyslips']))
    saibotxpal.logger.info("Ignoring unchanged dutyslips")
    for dutyslip in existingdutyslips:
        saibotxpal.logger.info("{}".format(dutyslip.to_json()))
        match = False
        for dutyslipdict in assignmentdict['dutyslips']:
            # saibotxpal.logger.info("{}".format(dutyslipdict))
            if dutyslip.member == dutyslipdict['member'] and dutyslip.vehicle == dutyslipdict['vehicle']:
                saibotxpal.logger.info("Unchanged {}".format(dutyslipdict))
                # assignmentdict['dutyslips'].remove(dutyslipdict)
                # existingdutyslips.remove(dutyslip)
                match = True
        if match is False:
            saibotxpal.logger.info(
                "Removing unmatched dutyslip {}".format(dutyslip.to_json()))
            dutyslip.delete()
    saibotxpal.logger.info("Adding the new dutyslips")
    for dutyslipdict in assignmentdict['dutyslips']:
        if "vehicle" not in dutyslipdict.keys():
            dutyslipdict['vehicle'] = None
        d = documents.DutySlip.objects(
            member=dutyslipdict['member'], vehicle=dutyslipdict['vehicle'], assignment=assignment)
        if len(d) == 0:
            d = documents.DutySlip(
                member=dutyslipdict['member'], vehicle=dutyslipdict['vehicle'], assignment=assignment, status="new")
            saibotxpal.logger.info(
                "Created duty slip {}".format(d.to_json()))
        else:
            d = d[0]
            saibotxpal.logger.info(
                "Duty slip exists {}".format(d.to_json()))
        d.save()
    for booking in assignment.bookings:
        booking.assignment = str(assignment.id)
        booking.save()
        update_booking_status(booking.booking_id, "assigned")
        booking.save()
    saibotxpal.logger.info(
        "Saved assignment {}".format(assignment.to_json()))
    return [assignment]


def search_assignments(cust_id=None, date_frm=None, date_to=None, status=None):
    assignments = documents.Assignment.objects
    if cust_id is not None:
        assignments = assignments.filter(cust_id=cust_id)
    if date_frm is not None:
        assignments = assignments.filter(reporting_timestamp__gt=date_frm)
    if date_to is not None:
        assignments = assignments.filter(reporting_timestamp__lt=date_to)
    if status is not None:
        assignments = assignments.filter(status=status)

    return assignments


def update_assignment_status(assignmentid, status):
    if status not in utils.validstatuses or status in ["new", "assigned"]:
        saibotxpal.logger.error("Invalid status")
        return False
    assignment = documents.Assignment.objects.with_id(assignmentid)
    if assignment:
        dutyslips = documents.DutySlip.objects(assignment=assignment)
        try:
            if status == "cancelled":
                saibotxpal.logger.info(
                    "Removing Assignment reference from  Bookings {}".format(assignment.bookings))
                for booking in assignment.bookings:
                    update_booking_status(booking.booking_id, "new")
                for ds in dutyslips:
                    if ds.status != "cancelled":
                        update_dutyslip_status(ds.id, "cancelled")
            if status in ["open", "closed"]:
                for booking in assignment.bookings:
                    update_booking_status(booking.booking_id, status)

            if status == "verified":
                for booking in assignment.bookings:
                    update_booking_status(booking.booking_id, status)
                for ds in dutyslips:
                    if ds.status != "cancelled":
                        update_dutyslip_status(ds.id, status)
            assignment.status = status
            assignment.save()
            saibotxpal.logger.info("Successfully updated assignment status")
            return True
        except Exception as e:
            saibotxpal.logger.error({}.format(str(e)))
            return False

    else:
        saibotxpal.logger.error("Assignment with that username does not exist")
        return False


def delete_assignment(assignmentid):
    if len(documents.Assignment.objects.with_id(assignmentid)) > 0:
        update_assignment_status(assignmentid, "cancelled")
        assignment = documents.Assignment.objects.with_id(assignmentid)
        documents.DutySlip.objects(assignment=assignment).delete()
        assignment.delete()
        return []
    else:
        return "Assignment with that username does not exist"
'''

'''
Duty Slip CRUD



def get_duties_for_member(username):
    d = documents.DutySlip.objects(member=username, status__ne="verified")
    if len(d) > 0:
        return d


def update_dutyslip_status(dsid, status):
    dutyslip = documents.DutySlip.objects.with_id(dsid)
    if dutyslip is None:
        saibotxpal.logger.error("No dutyslip with that id found")
        return False
    if status not in utils.validstatuses or status in ['assigned']:
        saibotxpal.logger.error("Invalid status")
        return False
    try:

        dutyslip.status = status
        dutyslip.save()
        if status == "open":
            update_assignment_status(dutyslip.assignment.id, "open")
        if status == "cancelled":
            otherds = documents.DutySlip.objects(
                assignment=dutyslip.assignment, status__ne="cancelled")
            if len(otherds) == 0:
                update_assignment_status(dutyslip.assignment.id, "cancelled")
        if status == "closed":
            otherds = documents.DutySlip.objects(
                assignment=dutyslip.assignment, status__ne="closed")
            if len(otherds) == 0:
                update_assignment_status(dutyslip.assignment.id, "closed")
        return True
    except Exception as e:
        saibotxpal.logger.error("{}".format(str(e)))
        return False


def update_dutyslip(dsid, respdict):
    dutyslip = documents.DutySlip.objects.with_id(dsid)
    if dutyslip is None:
        return "No dutyslip with that id found"
    try:
        if "status" in respdict.keys():
            if respdict['status'] != dutyslip.status:
                update_dutyslip_status(dutyslip.id, respdict['status'])
        dutyslip.update(**respdict)
        dutyslip.save()
        dutyslip.reload()
        return [dutyslip]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def delete_dutyslip(dsid):
    if len(documents.DutySlip.objects.with_id(dsid)) > 0:
        update_dutyslip_status(dsid, "cancelled")
        ds = documents.DutySlip.objects.with_id(dsid)
        ds.delete()
    else:
        return "No Dutyslip by that username"
'''

'''
Driver CRUD functionality
'''


def get_member_by_mobile(mobile_num):
    t = documents.Member.objects(mobile_num=mobile_num)
    xetrapal.astra.baselogger.info(
        "Found {} members with Mobile Num {}".format(len(t), mobile_num))
    if len(t) > 0:
        # return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None

def get_member_by_username(username):
    t = documents.Member.objects(username=username)
    xetrapal.astra.baselogger.info(
        "Found {} members with Username{}".format(len(t), username))
    if len(t) > 0:
        # return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None



def get_member_by_tgid(tgid):
    t = documents.Member.objects(tgid=tgid)
    xetrapal.astra.baselogger.info(
        "Found {} members with Telegram username {}".format(len(t), tgid))
    if len(t) > 0:
        # return[User(x['value']) for x in t][0]
        return t[0]
    else:
        return None


def create_member(respdict):
    member = documents.Member.objects(username=respdict['username'])
    if len(member) > 0:
        return "Driver with that username Exists"
    if "_id" in respdict.keys():
        respdict.pop('_id')
    try:
        member = documents.Member(**respdict)
        member.save()
        return [member]
    except Exception as e:
        return "{} {}".format(repr(e), str(e))


def update_member(username, respdict):
    member = documents.Member.objects(username=username)
    if len(member) == 0:
        return "No member by username {}".format(username)
    else:
        member = member[0]
    if "_id" in respdict.keys():
        respdict.pop('_id')
    if "username" in respdict.keys():
        if respdict['username'] != username:
            return "Member username mismatch {} {}".format(username, respdict['username'])
        respdict.pop('username')
    try:
        member.update(**respdict)
        member.save()
        member.reload()
        return [member]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def update_member_repayments(repayments):
    for r in repayments:
        mem = documents.Member.objects(username=r['from'])[0]
        saibotxpal.logger.info(mem.to_json())
        mem['repayments'][r['to']] += r['amount']
        mem.save()
        saibotxpal.logger.info(mem.to_json())
        mem2 = documents.Member.objects(username=r['to'])[0]
        saibotxpal.logger.info(mem2.to_json())
        mem2['repayments'][r['from']] += -r['amount']
        mem2.save()
        saibotxpal.logger.info(mem2.to_json())

def update_member_balance(members):
    for member in members:
        mem = documents.Member.objects(username=member['username']).update(inc__net_balance = member['net_balance'])

def delete_member(username):
    if len(documents.Member.objects(username=username)) > 0:
        try:
            member = documents.Member.objects(username=username)[0]
            member.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    else:
        return "No member by that id"



'''
Customer
'''


def create_customer(respdict):
    customer = documents.Customer.objects(cust_id=respdict['cust_id'])
    if len(customer) > 0:
        return "Customer with that username Exists"
    if len(respdict['cust_id']) < 5:
        return "id should be minimum of 5 characters"
    if "_id" in respdict.keys():
        respdict.pop('_id')
    try:
        customer = documents.Customer(**respdict)
        customer.save()
        return [customer]
    except Exception as e:
        return "{} {}".format(repr(e), str(e))


def update_customer(cust_id, respdict):
    customer = documents.Customer.objects(cust_id=cust_id)
    if len(customer) == 0:
        return "No Customer by username {}".format(cust_id)
    else:
        customer = customer[0]
    if "_id" in respdict.keys():
        respdict.pop('_id')
    if "cust_id" in respdict.keys():
        if respdict['cust_id'] != cust_id:
            return "customer username mismatch {} {}".format(cust_id, respdict['cust_id'])
        respdict.pop('cust_id')
    try:
        customer.update(**respdict)
        customer.save()
        customer.reload()
        return [customer]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def delete_customer(cust_id):
    if len(documents.Customer.objects(cust_id=cust_id)) > 0:
        try:
            customer = documents.Customer.objects(cust_id=cust_id)[0]
            customer.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    else:
        return "No customer by that id"



'''
Xchanges
'''


def get_xchange(xchange_id=None):
    saibotxpal.logger.info((xchange_id))
    if xchange_id is None:
        try:
            xchange = documents.Xchange.objects
            return list(xchange)
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    if len(documents.Xchange.objects(xchange_id=xchange_id)) > 0:
        try:
            xchange = documents.Xchange.objects(xchange_id=xchange_id)
            return [xchange]
        except Exception as e:
            return "{} {}".format(type(e), str(e))
    else:
        return "No such xchange"


def create_xchange(xchangedict):
    saibotxpal.logger.info(utils.new_xchange_id())
    try:
        xchange = documents.Xchange(
            xchange_id=utils.new_xchange_id(), **xchangedict)
        xchange.save()
        update_member_repayments(xchangedict['repayments'])
        update_member_balance(xchangedict['members'])
        return[xchange]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def update_xchange(xchange_id, xchangedict):
    try:
        if "_id" in xchangedict:
            xchangedict.pop("_id")
        xchange = documents.Xchange.objects(xchange_username=xchange_username)[0]
        xchange.update(**xchangedict)
        xchange.save()
        xchange.total = get_xchange_total(xchange.xchange_id)
        return[xchange]
    except Exception as e:
        return "{} {}".format(type(e), str(e))


def delete_xchange(xchange_id):
    if len(documents.Xchange.objects(xchange_id=xchange_id)) == 0:
        return "No Xchange by that username"
    else:
        try:
            xchange = documents.Xchange.objects(xchange_id=xchange_id)
            xchange.delete()
            return []
        except Exception as e:
            return "{} {}".format(type(e), str(e))




'''
Exporting everything
'''


def export_members():
    members = documents.Member.objects.to_json()
    members = json.loads(members)
    for member in members:
        del member['_id']
    memberdf = pandas.DataFrame(members)
    memberdf.to_csv("./dispatcher/reports/members.csv")
    return "reports/members.csv"

'''
Bulk Imports of everything
'''

def import_members(memberlist):
    try:
        for member in memberlist:
            try:
                if validate_member_dict(member)['status'] is True:
                    d = create_member(member)
                    if type(d) == list:
                        d = d[0]
                        d.save()
                        d.reload()
                        member['status'] = d.username
                    else:
                        member['status'] = d
                else:
                    member['status'] = validate_member_dict(member)['message']
            except Exception as e:
                member['status'] = "{} {}".format(type(e), str(e))
        return memberlist
    except Exception as e:
        return "{} {}".format(type(e), str(e))
