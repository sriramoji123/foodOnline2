def detectUser(user):
    if user.role == 1:
        redirectUrl =  'vendorDashboard'
        print(user.role)
        return redirectUrl
    elif user.role==2:
        redirectUrl =  'custDashboard'
        print(user.role)
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
    