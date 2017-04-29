from flask import Flask, abort, jsonify, make_response, render_template, request
from flask_cors import CORS, cross_origin
import base64
import zlib
import requests


app = Flask(__name__)
app.config['CORS_HEADERS'] = ['Content-Type']
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}
app.config['CORS_ORIGINS'] = ['*']
cors = CORS(app)


@app.route('/')
def index():
    """
    Check the status of the gateway
    :return: 
    """
    response = {
        'status': 'OK',
    }
    return jsonify(response)



@app.route('/flixster')
def test_flixster():
    """
    Test loading the page to open flixster video
    :return: 
    """
    return render_template('flixster_redirect.html')



@app.route('/auth', methods=['POST'])
def auth():
    print "/auth"
    print request.form['AccountID']
    print request.form['UserID']
    samlAssertion = request.form['SAMLAssertion']
    print "SAML assertion %s" % samlAssertion
    status = request.form['Status']
    print "status %s" % status

    # HTML template to render depending on the result of the authentication
    # a rights creation


    if status == "success":
        '''base64 decode'''
        decodedSamlAssertion = base64.b64decode(samlAssertion)

        #print "Decoded %s" % decodedSamlAssertion

        token = deflate_and_base64_encode(decodedSamlAssertion)

        createRights(token)
    else:
        template = 'flixster_redirect.html'
        return render_template(template)




@app.errorhandler(400)
def bad_request(error):
    print error
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    print error
    return make_response(jsonify({'error': 'Not found'}), 404)


def deflate_and_base64_encode(string_val):
    """
    
    :param string_val: 
    :return: 
    """

    zlibbed_str = zlib.compress(string_val)
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string)

def createRights(token):
    """
    Create the rights of owning the moving with the given token
    :param token: 
    :return: 
    """

    template = 'flixster_redirect.html'

    # Create the rights with the token
    headers = {
        'accept': 'application/xml',
        'authorization': 'UVGS uvgs_clientid=UV_ERICSSON,uvgs_accesskey=kRvoUwPdIqukswRhBXIfwmhd2zmnKIuRR90MC0SuWbUl9ZuGNUlBebZEytpXB506jHM4weYGiMhJOzjHEALkNC1i6N46u84Pl8IV7VkVJsRkjDwsM8iL1B2rcPZsrr7v',
        'content-type': 'application/xml;charset=utf-8',
        'invocation-role': 'urn:dece:role:retailer',
        'SAML-Assertion': token
    }

    data = '<rightsTokenCreationRequest>' \
           '    <rightsToken>' \
           '    <alid>urn:dece:alid:eidr-s:67B0-2137-1A59-BC25-9EC3-3</alid>' \
           '    <contentID>urn:dece:cid:eidr-s:67B0-2137-1A59-BC25-9EC3-3</contentID>' \
           '    <purchaseInfo>' \
           '        <nodeID>urn:dece:org:org:dece:warnerbros:retailer</nodeID>' \
           '        <purchaseAccount>urn:dece:accountid:org:dece:5B23BC19574B4E9B812A128050C942A9</purchaseAccount>' \
           '        <purchaseTime>2017-04-24T18:06:40.379-07:00</purchaseTime>' \
           '        <purchaseUser>urn:dece:userid:org:dece:D940F2F1379842669A3DBFDE5449A82F</purchaseUser>' \
           '        <retailerTransaction>null</retailerTransaction>' \
           '        <transactionType>urn:dece:type:transaction:category1:p</transactionType>' \
           '    </purchaseInfo>' \
           '    <rightsProfiles>' \
           '        <purchaseProfile>' \
           '            <canDownload>true</canDownload>' \
           '            <canStream>true</canStream>' \
           '            <mediaProfile>urn:dece:type:MediaProfile:sd</mediaProfile>' \
           '        </purchaseProfile>' \
           '        <purchaseProfile>' \
           '            <canDownload>true</canDownload>' \
           '            <canStream>true</canStream>' \
           '            <mediaProfile>urn:dece:type:MediaProfile:hd</mediaProfile>' \
           '        </purchaseProfile>' \
           '    </rightsProfiles>' \
           '    <soldAs>' \
           '        <contentID>urn:dece:cid:eidr-s:67B0-2137-1A59-BC25-9EC3-3</contentID>' \
           '            <displayName>Pan</displayName>' \
           '    </soldAs>' \
           '    <streamWebLoc>' \
           '        <location>https://www.flixstervideo.com/swl/' \
           '            urn:dece:cid:eidr-s:67B0-2137-1A59-BC25-9EC3-3</location>' \
           '    </streamWebLoc>' \
           '</rightsToken>' \
           '</rightsTokenCreationRequest>'

    r = requests.post(
        'https://ultraviolet.warnerbros.com/uvservice/resources/Gateway/RightsToken/AccountId/urn:dece:accountid:org:dece:5B23BC19574B4E9B812A128050C942A9',
        headers=headers, data=data)

    print "POST /rightstoken status code: %s" % r.status_code

    if r.status_code == 201:
        template = 'flixster_redirect.html'

    return render_template(template)


if __name__ == '__main__':
    app.run(debug=True)