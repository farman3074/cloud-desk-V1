from flask import Flask,render_template,request,jsonify,redirect,url_for
#import datafile
from datetime import datetime
from database import load_members_from_db,load_member_from_db, commit_member_to_db, load_spaces_from_db, load_space_from_db, commit_space_to_db, commit_booking_to_db,commit_query_to_db,load_bookings_from_db,commit_invoice_to_db,load_invoices_from_db,load_invoiceLI_from_db,load_invoice_from_db,load_active_members_from_db,creat_monthly_invoice

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/logincheck",methods =["POST"])
def check_login():
  user = request.form.get("username") 
  if  user == "farman":
      return render_template("dashboard.html", title="Dash Board")
  else:
    return render_template("home.html")

@app.route("/dashboard")
def show_dashbaord():
  return render_template("dashboard.html", title="Dash Board")

@app.route("/members")
def show_members():
  members = load_members_from_db()
  return render_template("members.html", title="Members", members=members)

@app.route("/viewmember/<id>")
def show_member(id):
  member = load_member_from_db(id)
  return render_template("viewmember.html", title="View Member",member=member)

@app.route("/editmember/<id>")
def edit_member(id):
  member = load_member_from_db(id)
  return render_template("editmember.html", title="Edit Member",member=member)

@app.route("/commitmember",methods =["POST"])
def commit_member():
  query = "update members set name ='" + request.form.get('nameInput') + "', company = '" + request.form.get('companyInput') + "', email ='" + request.form.get('emailInput') + "', phone = '" +  request.form.get('phoneInput') + "', nature = '" + request.form.get('natureInput') + "', address = '" + request.form.get('addressInput') + "' where ID= " + request.form.get('idInput')
  result = commit_member_to_db(query)
  return redirect(f"/viewmember/{request.form.get('idInput')}")

@app.route("/addmember")
def add_member():
  return render_template("addmember.html", title="Add Member")

@app.route("/commitaddmember",methods =["POST"])
def commit_add_member():
  query = "insert into members (`name`, `company`, `email`, `phone`, `nature`, `address`, `membership_date`) VALUES ('" + request.form.get('nameInput') + "', '" + request.form.get('companyInput') + "','" + request.form.get('emailInput') + "','" +  request.form.get('phoneInput') + "','" + request.form.get('natureInput') + "','" + request.form.get('addressInput') + "','" + datetime.now().strftime("%Y-%m-%d") + "')" 
  result = commit_member_to_db(query)
  return redirect("/members")

  
@app.route("/spaces")
def show_spaces():
  spaces = load_spaces_from_db()
  return render_template("spaces.html", title="Spaces", spaces=spaces)

@app.route("/viewspace/<id>")
def show_space(id):
  space = load_space_from_db(id)
  bookings = load_bookings_from_db(id)
  return render_template("viewspace.html", title="View Space",space=space, bookings=bookings)

@app.route("/editspace/<id>")
def edit_space(id):
  space = load_space_from_db(id)
  return render_template("editspace.html", title="Edit space",space=space)

@app.route("/addspace")
def add_space():
  return render_template("addspace.html", title="Add Space")

@app.route("/commitspace",methods =["POST"])
def commit_space():
  query = "update spaces set name ='" + request.form.get('nameInput') + "', type = '" + request.form.get('typeInput') + "', floor ='" + request.form.get('floorInput') + "', seats = " +  request.form.get('seatsInput') + ", area = " + request.form.get('areaInput') + ", isempty = '" + request.form.get('emptyInput') + "', listRate = '"+ request.form.get('rateInput') +"', rateType = '"+ request.form.get('ratetypeInput') +"' where ID= " + request.form.get('idInput')
  result = commit_space_to_db(query)
  return redirect(f"/viewspace/{request.form.get('idInput')}")

@app.route("/commitaddspace",methods =["POST"])
def commit_add_space():
  query = "insert into spaces(`name`, `floor`, `seats`, `area`, `type`, `isempty`, `listRate`, `rateType`) VALUES ('" + request.form.get('nameInput') + "','" + request.form.get('floorInput') + "','" +  request.form.get('seatsInput') + "','" + request.form.get('areaInput') + "','" + request.form.get('typeInput') + "','Yes','" + request.form.get('rateInput') + "','" + request.form.get('ratetypeInput') + "')"
  result = commit_space_to_db(query)
  return redirect("/spaces")


@app.route("/bookspace/<id>")
def book_space(id):
  space = load_space_from_db(id)
  members = load_members_from_db()
  currentdate = datetime.now().date()
  return render_template("bookspace.html", title = "Book " + space['name'], space=space, members=members, currentdate = currentdate)

@app.route("/commitbooking",methods =["POST"])
def commit_booking():
  query = "insert into bookings (memberID, spaceID, bookFrom, bookTo, bookRate, rateType, bookDate) Values (" + request.form.get('memberInput') +"," + request.form.get('spaceInput')  + ",'" + request.form.get('startInput') + "','" + request.form.get('endInput') + "'," + request.form.get('rateInput') + ",'" + request.form.get('ratetypeInput') + "','" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "')"
  bookingID = commit_booking_to_db(query)
#  query = "insert into ledger (entryDate, bookingID, entryType, entryDesc, entryValue) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'," + str(bookingID['ID']) + ", 'SECURITY','Security Deposit'," + request.form.get('securityInput')+")"
  invAmt = int(request.form.get('securityInput')) + int( request.form.get('advanceInput'))
  query = "insert into invoices (createdon,invoicedate,duedate,memberID,header,footer,invoiceamt,amtwithtax,invoicetype) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "','" + datetime.now().strftime("%Y-%m-%d") + "','" + datetime.now().strftime("%Y-%m-%d") + "'," + request.form.get('memberInput') + ",'Invoice for Security and Advance','Please pay by cheque or bank transfer to A/C # XXXXXX'," + str(invAmt) + ","+ str(invAmt) +",'SECURITYADVANCE')"
  invoiceID = commit_invoice_to_db(query)
  query = "insert into invoiceLI (invoiceID,itemNum,itemDesc,itemRate,itemqty,itemtotal,bookingID) values ('" + str(invoiceID['ID']) + "',1,'Security Deposit',0,1," + request.form.get('securityInput') + ",'" + str(bookingID['ID']) + "')"
  result = commit_query_to_db(query)
  query = "insert into invoiceLI (invoiceID,itemNum,itemDesc,itemRate,itemqty,itemtotal,bookingID) values ('" + str(invoiceID['ID']) + "',2,'Advance Rent',0,1," + request.form.get('advanceInput') + ",'" + str(bookingID['ID']) + "')"
  result = commit_query_to_db(query)
  #query = "insert into ledger (entryDate, bookingID, entryType, entryDesc, entryValue) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'," + str(bookingID['ID']) + ", 'ADVANCE','Advance Deposit'," + request.form.get('advanceInput') +")"
  query = "update spaces set isempty ='No' where ID = " + request.form.get('spaceInput')
  result = commit_space_to_db(query)
  return redirect("/spaces")
  #return request.form.get('ratetypeInput')
  
@app.route("/invoicing")
def show_invoices():
  invoices = load_invoices_from_db()
  query = "SELECT ID,name FROM members where members.ID in (select memberID from bookings where bookings.bookto > '"+ datetime.now().strftime("%Y-%m-%d") + "')"
  result = load_active_members_from_db(query)
  currentdate = datetime.now().date()
  return render_template("invoicing.html", title="Invoicing", invoices=invoices, members = result, currentdate = currentdate)

@app.route("/viewinvoice/<id>")
def show_invoice(id):
  invoice = load_invoice_from_db(id)
  member = load_member_from_db(invoice['memberID'])
  invoiceLIs = load_invoiceLI_from_db(id)
  return render_template("viewinvoice.html", title="Customer Invoice", invoice=invoice,member=member,invoiceLI=invoiceLIs)

# this one is replaced by a Modal now
@app.route("/payinvoice/<id>")
def pay_invoice(id):
  return render_template("payinvoice.html", invoiceID=id)

@app.route("/commitpayment",methods =["POST"])
def commit_invoice():
  query = "Update invoices set ispaid = 'Y', instrumentType ='" + request.form.get('instrumentType') +"',instrumentRef='" + request.form.get('instrumentRef') +"',paydate='" +request.form.get('instrumentDate') +"',paidamt =" +request.form.get('amount') +" where ID = " + request.form.get('invoiceID')
  result = commit_query_to_db(query)
  query = "insert into ledger (entryDate, entryRef, entryType, entryDesc, entryValue) values ('" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "'," + request.form.get('invoiceID') + ",'INVOICE', 'Invoice Payment by Customer'," + request.form.get('amount') + ")"
  result = commit_query_to_db(query)
  return redirect(f"/viewinvoice/{request.form.get('invoiceID')}")

@app.route("/newinvoice",methods =["POST"])
def new_invoice():
  if request.form.get("memberInput") == "0":
    query = "SELECT ID,name FROM members where members.ID in (select memberID from bookings where bookings.bookto > '"+ datetime.now().strftime("%Y-%m-%d") + "')"
    results = load_active_members_from_db(query)

    for result in results:
      creat_monthly_invoice(request.form.get("fromInput"),request.form.get("toInput"), result.get("ID"))       
  else:
    creat_monthly_invoice(request.form.get("fromInput"),request.form.get("toInput"),request.form.get("memberInput"))
  
    
  return redirect("/invoicing")
  



  
@app.route("/reporting")
def show_reporting():
  return render_template("reporting.html", title="Reporting")




print(__name__)
if __name__ == "__main__" :
  app.run(host="0.0.0.0", debug=True)
