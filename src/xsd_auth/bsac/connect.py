import requests
from bs4 import BeautifulSoup

class BSACConnect(object):
  def __init__(self, email, password):
    # Do https://members.bsac.com/membersarea/login/login_user.asp
    # x-www-form-urlencoded
    # reg: email
    # pass: password

    self.session = requests.Session()

    # Build the auth request
    post_data = {
      'reg': email,
      'pass': password,
    }

    auth_req = self.session.post(
      'https://members.bsac.com/membersarea/login/login_user.asp',
      data=post_data,
    )

    if 'Update/View Details' in auth_req.text:
      print "Authenticated as {}".format(email)
    elif 'Login Failed' in auth_req.text:
      print "Authentication for {} failed".format(email)
    else:
      print "Authentication for {} experienced an unknown failure".format(email)

  def request_get(self, url):
    req = self.session.get(url)
    if 'If you have already registered to use BSAC' in req.text:
      raise Exception('Not authenticated')
    else:
      return req

  def member_details(self):
    member_req=self.request_get('https://members.bsac.com/membersarea/updates/Default.asp?')
    soup = BeautifulSoup(member_req.text)
    membership_number = [i for i in soup.findAll('td') if str(i) == """<td class="Text">Membership Number:</td>"""][0].next_sibling.next_sibling.next_element.string
    print "Membership number: {}".format(membership_number)

  def qual_details(self):
    qual_req=self.request_get('https://members.bsac.com/membersarea/updates/attributes1.asp?id=1')
    soup = BeautifulSoup(qual_req.text)


