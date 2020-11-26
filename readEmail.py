from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


def main():
   
    SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = results.get('messages', [])
    

    if not messages:
        print ("No messages found.")
    else:
        print ("Message snippets:")
        for  message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            for temp in msg['payload'].get('headers'):
                if 'From' in temp.get('name'):
                    a=temp.get('value').split('<')
                    print (a[0])
            #print (msg['payload'].get('headers'))
            print (msg['snippet'])
            print('-------------------------------------------------')


if __name__ == '__main__':
    main()