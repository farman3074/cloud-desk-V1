# invoice types
# field in invoices table
# SECURITYADVANCE - Inserted at booking
# MONTHLYMMYYYY - Monthly customer invoice MM and YYYY
# SPECIAL - Invoices generated for clearances or other mid month billing

# billing types
# selected while booking - applied on booking rates
# MONTHLY - Monthly billing starting 1st of every month
# WEEKLY - for 7 days
# DAILY - Daily billing
# HOURLY - mainly for resources (board rooms, projectors etc)

# scans DB and create invoice entries for billing between startdate and enddate for a member
# returns a list of dictionary entries for invoices created 

#SQL queries
# Get members whose bookings need to be invoiced
# SELECT * FROM clouddesk.members where clouddesk.members.ID in (select memberID from clouddesk.bookings where clouddesk.bookings.bookFrom <= '2023-04-01' and clouddesk.bookings.bookto > '2023-03-02') ----dates need to be the current invoice run date
# Loop for each member and get all valid bookings and then create one invoice lineitem entry for each booking

